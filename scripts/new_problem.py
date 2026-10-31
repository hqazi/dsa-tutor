#!/usr/bin/env python3
"""Create problems and scaffold workspaces.

    python scripts/new_problem.py create SPEC.json [--curated] [--force] [--no-workspace]
    python scripts/new_problem.py workspace SLUG [--force]
    python scripts/new_problem.py validate SLUG | --all

`create` builds problems/generated/<slug>/ (or problems/curated/<topic>/<slug>/)
from a spec described in references/problem_spec.md. Expected outputs missing
from the spec are computed with the spec's brute_force solution. The
reference solution must then pass every test (the self-check); if it does
not, nothing is written and the failures are returned so the spec can be fixed.
"""
from __future__ import annotations

import argparse
import json
import keyword
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    CURATED_DIR, DIFFICULTIES, GENERATED_DIR, SCHEMA_VERSION, SLUG_RE, TutorError,
    atomic_write_json, atomic_write_text, emit, find_problem, iter_problems, load_json,
    load_meta, now_iso, rel, run_main, topic_map, workspace_solution,
)
import run_tests  # noqa: E402

COMPARE_MODES = ("exact", "unordered", "unordered_deep", "float")
BRUTE_TIMEOUT = 60.0
MIN_VISIBLE, MIN_HIDDEN = 2, 3
MAX_VISIBLE_INPUT_CHARS = 1500

NODE_CLASSES = {
    "ListNode": (
        "class ListNode:\n"
        "    def __init__(self, val=0, next=None):\n"
        "        self.val = val\n"
        "        self.next = next\n"
    ),
    "TreeNode": (
        "class TreeNode:\n"
        "    def __init__(self, val=0, left=None, right=None):\n"
        "        self.val = val\n"
        "        self.left = left\n"
        "        self.right = right\n"
    ),
}


# ---------------------------------------------------------------- validation

def _ident(name) -> bool:
    return isinstance(name, str) and name.isidentifier() and not keyword.iskeyword(name)


def validate_spec(spec: dict, curated: bool) -> list[str]:
    errors: list[str] = []
    need = ("slug", "title", "topic", "difficulty", "statement", "signature",
            "expected_complexity", "tests", "reference_solution")
    for key in need:
        if key not in spec:
            errors.append(f"missing field {key!r}")
    if errors:
        return errors
    if not SLUG_RE.match(str(spec["slug"])):
        errors.append("slug must be lowercase words joined by hyphens")
    if spec["topic"] not in topic_map():
        errors.append(f"unknown topic {spec['topic']!r}; see references/topics.md")
    if spec["difficulty"] not in DIFFICULTIES:
        errors.append(f"difficulty must be one of {DIFFICULTIES}")
    if curated and spec["difficulty"] == "hard":
        errors.append("curated problems are easy or medium")
    if not str(spec["statement"]).strip():
        errors.append("statement is empty")
    if not isinstance(spec.get("constraints", []), list):
        errors.append("constraints must be a list of strings")

    sig = spec["signature"]
    params = sig.get("params") if isinstance(sig, dict) else None
    if not isinstance(sig, dict) or not _ident(sig.get("function")) or not isinstance(params, list):
        errors.append("signature needs function (identifier), params (list) and returns")
        return errors
    names = []
    for p in params:
        if not isinstance(p, dict) or not _ident(p.get("name")) or not isinstance(p.get("type"), str):
            errors.append(f"bad param {p!r}: needs name and type")
        else:
            names.append(p["name"])
    if len(set(names)) != len(names):
        errors.append("param names must be unique")
    if not isinstance(sig.get("returns"), str):
        errors.append("signature.returns must be a type string")

    ec = spec["expected_complexity"]
    if not isinstance(ec, dict) or not ec.get("time") or not ec.get("space"):
        errors.append("expected_complexity needs time and space")
    mode = spec.get("compare", {}).get("mode", "exact")
    if mode not in COMPARE_MODES:
        errors.append(f"compare.mode must be one of {COMPARE_MODES}")

    tests = spec["tests"]
    if not isinstance(tests, list) or not tests:
        errors.append("tests must be a non-empty list")
        return errors
    has_brute = bool(str(spec.get("brute_force", "")).strip())
    counts = {"visible": 0, "hidden": 0}
    for i, t in enumerate(tests):
        where = f"tests[{i}]"
        vis = t.get("visibility")
        if vis not in counts:
            errors.append(f"{where}: visibility must be 'visible' or 'hidden'")
            continue
        counts[vis] += 1
        if not isinstance(t.get("input"), dict) or set(t["input"]) != set(names):
            errors.append(f"{where}: input must be an object with exactly the keys {names}")
        if vis == "hidden" and not str(t.get("category", "")).strip():
            errors.append(f"{where}: hidden tests need a category such as 'empty input'")
        by = t.get("expected_by")
        if "expected" not in t:
            if by == "reference":
                if not has_brute:
                    errors.append(f"{where}: expected_by 'reference' requires a brute_force solution in the spec")
                if vis == "visible":
                    errors.append(f"{where}: visible tests need an explicit or brute-force expected value")
            elif not has_brute:
                errors.append(f"{where}: no expected value and no brute_force to compute it")
        if vis == "visible" and len(json.dumps(t.get("input"))) > MAX_VISIBLE_INPUT_CHARS:
            errors.append(f"{where}: visible inputs must stay small (they are shown in problem.md)")
    if counts["visible"] < MIN_VISIBLE:
        errors.append(f"need at least {MIN_VISIBLE} visible tests")
    if counts["hidden"] < MIN_HIDDEN:
        errors.append(f"need at least {MIN_HIDDEN} hidden tests")
    return errors


# ---------------------------------------------------------------- rendering

def py_literal(value) -> str:
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(py_literal(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(f"{json.dumps(k)}: {py_literal(v)}" for k, v in value.items()) + "}"
    return repr(value)


def signature_line(sig: dict) -> str:
    params = ", ".join(f"{p['name']}: {p['type']}" for p in sig["params"])
    return f"def {sig['function']}({params}) -> {sig['returns']}:"


def node_classes(sig: dict) -> list[str]:
    types = " ".join([p["type"] for p in sig["params"]] + [sig["returns"]])
    return [name for name in NODE_CLASSES if name in types]


def render_problem_md(meta: dict, statement: str, constraints: list[str], tests: list[dict],
                      notes: str = "") -> str:
    topic = topic_map().get(meta["topic"], {"name": meta["topic"]})["name"]
    sig = meta["signatures"]["python"]
    slug = meta["slug"]
    out = [f"# {meta['title']}", "",
           f"**Topic:** {topic} · **Difficulty:** {meta['difficulty'].capitalize()}", "",
           statement.strip(), "", "## Examples", ""]
    n = 0
    for t in tests:
        if t["visibility"] != "visible":
            continue
        n += 1
        args = ", ".join(f"{p['name']} = {py_literal(t['input'][p['name']])}" for p in sig["params"])
        out += [f"**Example {n}**", "", "```text", f"Input:  {args}",
                f"Output: {py_literal(t['expected'])}", "```", ""]
        if t.get("explanation"):
            out += [t["explanation"].strip(), ""]
    if constraints:
        out += ["## Constraints", ""] + [f"- {c}" for c in constraints] + [""]
    if notes.strip():
        out += ["## Notes", "", notes.strip(), ""]
    classes = node_classes(sig)
    out += ["## Signature", "", "```python"]
    for name in classes:
        out += [NODE_CLASSES[name]]
    out += [signature_line(sig), "```", ""]
    if classes:
        out += [f"`{'` and `'.join(classes)}` values are given to you already built; "
                "in the examples they are written as lists (trees in level order, `None` for a missing child).", ""]
    if meta.get("compare", {}).get("mode") in ("unordered", "unordered_deep"):
        out += ["The order of the returned items does not matter.", ""]
    if meta.get("compare", {}).get("mode") == "float":
        out += [f"Answers within {meta['compare'].get('tolerance', 1e-6)} (relative) are accepted.", ""]
    out += ["## Your solution", "",
            f"Write it in `workspace/{slug}/solution.py`, then run the tests:", "",
            "```bash", f"python scripts/run_tests.py {slug}", "```", ""]
    return "\n".join(out)


def scaffold_source(meta: dict, problem_dir: Path) -> str:
    sig = meta["signatures"]["python"]
    topic = topic_map().get(meta["topic"], {"name": meta["topic"]})["name"]
    lines = [f'"""{meta["title"]} ({topic}, {meta["difficulty"]})', "",
             f"Problem: {rel(problem_dir / 'problem.md')}",
             f"Test:    python scripts/run_tests.py {meta['slug']}", '"""']
    for name in node_classes(sig):
        lines += ["", "# Provided: the tests build inputs with this class. Do not change it.",
                  NODE_CLASSES[name].rstrip()]
    lines += ["", "", signature_line(sig), "    # Your code here", "    raise NotImplementedError", ""]
    return "\n".join(lines)


def scaffold_workspace(slug: str, force: bool = False) -> tuple[Path, bool]:
    problem_dir = find_problem(slug)
    meta = load_meta(problem_dir)
    path = workspace_solution(slug)
    if path.exists() and not force:
        return path, False
    atomic_write_text(path, scaffold_source(meta, problem_dir))
    return path, True


# ---------------------------------------------------------------- create

def build_meta(spec: dict, source: str) -> dict:
    sig = spec["signature"]
    return {
        "schema_version": SCHEMA_VERSION,
        "slug": spec["slug"],
        "title": spec["title"],
        "topic": spec["topic"],
        "difficulty": spec["difficulty"],
        "source": source,
        "created_at": now_iso(),
        "expected_complexity": spec["expected_complexity"],
        "compare": spec.get("compare", {"mode": "exact"}),
        "signatures": {"python": {"function": sig["function"], "params": sig["params"], "returns": sig["returns"]}},
    }


def assign_ids(tests: list[dict]) -> None:
    counters = {"visible": 0, "hidden": 0}
    used = {t["id"] for t in tests if t.get("id")}
    for t in tests:
        if t.get("id"):
            continue
        prefix = "example" if t["visibility"] == "visible" else "hidden"
        while True:
            counters[t["visibility"]] += 1
            candidate = f"{prefix}-{counters[t['visibility']]}"
            if candidate not in used:
                break
        t["id"] = candidate
        used.add(candidate)


def _failure(test: dict, raw: dict, expected=None) -> dict:
    item = {"id": test["id"], "category": test.get("category", ""), "status": raw["status"],
            "input": _clip(test["input"])}
    if expected is not None:
        item["expected"] = _clip(expected)
    if raw["status"] == "ok":
        item["actual"] = _clip(raw.get("actual"))
    for key in ("error_type", "message", "line", "time_ms"):
        if raw.get(key) is not None:
            item[key] = raw[key]
    return item


def _clip(value, limit=300):
    text = json.dumps(value)
    return value if len(text) <= limit else text[:limit] + "...(truncated)"


def create(spec: dict, curated: bool = False, force: bool = False, workspace: bool = True) -> dict:
    errors = validate_spec(spec, curated)
    if errors:
        return {"ok": False, "error": "invalid spec", "problems": errors}
    slug = spec["slug"]
    try:
        existing = find_problem(slug)
    except TutorError:
        existing = None
    if existing and not force:
        return {"ok": False, "error": f"slug {slug!r} already exists at {rel(existing)}; choose another slug"}
    target = (CURATED_DIR / spec["topic"] / slug) if curated else (GENERATED_DIR / slug)
    meta = build_meta(spec, "curated" if curated else "generated")
    tests = [dict(t) for t in spec["tests"]]
    assign_ids(tests)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        meta_path = tmp / "meta.json"
        meta_path.write_text(json.dumps(meta), encoding="utf-8")
        reference = tmp / "reference.py"
        reference.write_text(spec["reference_solution"].rstrip() + "\n", encoding="utf-8")

        # 1. Fill in expected values from the brute force.
        brute_idx = [i for i, t in enumerate(tests) if "expected" not in t and t.get("expected_by") != "reference"]
        if brute_idx:
            brute = tmp / "brute.py"
            brute.write_text(spec["brute_force"].rstrip() + "\n", encoding="utf-8")
            raws = run_tests.execute_cases(brute, [tests[i] for i in brute_idx], meta_path, BRUTE_TIMEOUT)
            bad = [_failure(tests[i], r) for i, r in zip(brute_idx, raws) if r["status"] != "ok"]
            if bad:
                return {"ok": False, "error": "brute_force failed on some tests", "failures": bad}
            for i, r in zip(brute_idx, raws):
                tests[i]["expected"] = r["actual"]

        # 2. Self-check: the reference must pass everything within the time limit.
        raws = run_tests.execute_cases(reference, tests, meta_path, run_tests.DEFAULT_TIMEOUT)
        failures = []
        for t, r in zip(tests, raws):
            if t.get("expected_by") == "reference":
                if r["status"] == "ok":
                    t["expected"] = r["actual"]
                else:
                    failures.append(_failure(t, r))
            elif r["status"] != "ok" or not run_tests.compare(r.get("actual"), t["expected"], meta["compare"]):
                failures.append(_failure(t, r, t["expected"]))
        if failures:
            return {"ok": False, "error": "self-check failed: the reference solution does not pass every test; "
                    "fix the reference or the expected values and run create again",
                    "failures": failures}

        # 3. Write the problem folder.
        clean_tests = []
        for t in tests:
            category = t.get("category") or ("example" if t["visibility"] == "visible" else "")
            item = {"id": t["id"], "visibility": t["visibility"], "category": category}
            item["input"], item["expected"] = t["input"], t["expected"]
            if t.get("explanation"):
                item["explanation"] = t["explanation"]
            clean_tests.append(item)
        if existing and existing != target:
            shutil.rmtree(existing)
        target.mkdir(parents=True, exist_ok=True)
        atomic_write_json(target / "meta.json", meta)
        atomic_write_text(target / "tests.json",
                          json.dumps({"schema_version": SCHEMA_VERSION, "tests": clean_tests},
                                     separators=(",", ":")) + "\n")
        atomic_write_text(target / "reference.py", reference.read_text(encoding="utf-8"))
        atomic_write_text(target / "problem.md",
                          render_problem_md(meta, spec["statement"], spec.get("constraints", []),
                                            clean_tests, spec.get("notes", "")))

    result = {"ok": True, "slug": slug, "problem": rel(target / "problem.md"),
              "tests": {"visible": sum(t["visibility"] == "visible" for t in clean_tests),
                        "hidden": sum(t["visibility"] == "hidden" for t in clean_tests)},
              "self_check": "passed"}
    if workspace:
        path, created = scaffold_workspace(slug, force=force)
        result["workspace"] = rel(path)
        result["workspace_created"] = created
    return result


def validate_existing(slug: str) -> dict:
    report = run_tests.run(slug, reference=True)
    bad = [c for c in report["cases"] if c["status"] != "pass"]
    return {"slug": slug, "passed": report["passed"], "total": report["total"], "ok": not bad,
            **({"failures": bad} if bad else {})}


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create", help="build a problem from a spec JSON file ('-' for stdin)")
    c.add_argument("spec")
    c.add_argument("--curated", action="store_true", help="write to problems/curated/<topic>/ (maintainers)")
    c.add_argument("--force", action="store_true", help="replace an existing problem with the same slug")
    c.add_argument("--no-workspace", action="store_true")
    w = sub.add_parser("workspace", help="scaffold workspace/<slug>/solution.py")
    w.add_argument("slug")
    w.add_argument("--force", action="store_true", help="overwrite an existing solution file")
    v = sub.add_parser("validate", help="re-run the self-check on existing problems")
    v.add_argument("slug", nargs="?")
    v.add_argument("--all", action="store_true")
    args = ap.parse_args()

    if args.cmd == "create":
        if args.spec == "-":
            spec = json.load(sys.stdin)
        else:
            spec = load_json(Path(args.spec))
            if spec is None:
                raise TutorError(f"spec file not found: {args.spec}")
        result = create(spec, curated=args.curated, force=args.force, workspace=not args.no_workspace)
        emit(result)
        return 0 if result["ok"] else 1
    if args.cmd == "workspace":
        path, created = scaffold_workspace(args.slug, force=args.force)
        emit({"ok": True, "slug": args.slug, "workspace": rel(path), "created": created})
        return 0
    if args.all:
        slugs = [meta["slug"] for _, meta in iter_problems()]
    elif args.slug:
        slugs = [args.slug]
    else:
        raise TutorError("give a slug or --all")
    reports = [validate_existing(s) for s in slugs]
    failed = [r for r in reports if not r["ok"]]
    emit({"ok": not failed, "checked": len(reports), "failed": failed})
    return 0 if not failed else 1


if __name__ == "__main__":
    run_main(main)
