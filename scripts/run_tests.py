#!/usr/bin/env python3
"""Run a solution against a problem's tests.

    python scripts/run_tests.py SLUG                 # your workspace solution
    python scripts/run_tests.py SLUG --only visible  # just the examples
    python scripts/run_tests.py SLUG --solution path/to/file.py
    python scripts/run_tests.py SLUG --reference     # self-check the reference

Each case runs in a subprocess with a per-test timeout (default 2 s). Visible
cases report input / expected / actual; hidden cases report only their
category. Output is JSON when piped and text in a terminal (--json / --text
force either). Exit code: 0 all passed, 1 some failed, 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import queue
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    RUNNERS_DIR, TutorError, emit, find_problem, load_meta, load_tests, rel,
    run_main, runner_config, workspace_solution,
)

PREFIX = "@@dsa "
DEFAULT_TIMEOUT = 2.0
STARTUP_GRACE = 10.0  # seconds allowed for interpreter start + import + loading tests


# ---------------------------------------------------------------- execution

def _reader(stream, sink: queue.Queue) -> None:
    for line in stream:
        if line.startswith(PREFIX):
            try:
                sink.put(json.loads(line[len(PREFIX):]))
            except json.JSONDecodeError:
                pass
    sink.put(None)  # EOF


def _command(language: str, solution: Path, tests_path: Path, meta_path: Path, start: int) -> list[str]:
    config = runner_config(language)
    values = {
        "python": sys.executable,
        "runner_dir": str(RUNNERS_DIR / language),
        "solution": str(solution),
        "tests": str(tests_path),
        "meta": str(meta_path),
        "start": str(start),
    }
    return [part.format(**values) for part in config["command"]]


def execute(solution: Path, tests_path: Path, meta_path: Path, count: int,
            timeout: float = DEFAULT_TIMEOUT, language: str = "python") -> list[dict]:
    """Run every case; return one raw result per case (no comparison).

    Raw statuses: ok (has actual, time_ms), error, timeout, crash.
    A timeout or crash kills the process and restarts at the next case.
    """
    results: list[dict | None] = [None] * count
    start = 0
    while start < count:
        proc = subprocess.Popen(
            _command(language, solution, tests_path, meta_path, start),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
            text=True, encoding="utf-8", errors="replace", cwd=str(solution.parent),
        )
        events: queue.Queue = queue.Queue()
        stderr_lines: list[str] = []
        threading.Thread(target=_reader, args=(proc.stdout, events), daemon=True).start()
        threading.Thread(target=lambda: stderr_lines.extend(proc.stderr), daemon=True).start()

        def next_event(wait: float):
            try:
                return events.get(timeout=wait)
            except queue.Empty:
                return "timeout"

        def stop():
            if proc.poll() is None:
                proc.kill()
            proc.wait()

        event = next_event(STARTUP_GRACE + timeout)
        if event == "timeout" or event is None:
            stop()
            reason = "timeout" if event == "timeout" else "crash"
            message = ("solution took too long to load" if reason == "timeout"
                       else "".join(stderr_lines)[-500:].strip() or "runner exited unexpectedly")
            for i in range(start, count):
                results[i] = {"status": reason, "message": message}
            break
        if event.get("event") == "import_error":
            stop()
            for i in range(start, count):
                results[i] = {"status": "error", **{k: event.get(k) for k in ("error_type", "message", "line")},
                              "at_import": True}
            break

        restart_at = None
        index = start
        while index < count:
            begin = next_event(STARTUP_GRACE)
            if begin == "timeout" or begin is None or begin.get("event") != "begin":
                restart_at = index
                results[index] = {"status": "crash",
                                  "message": "".join(stderr_lines)[-500:].strip() or "runner exited unexpectedly"}
                break
            t0 = time.monotonic()
            result = next_event(timeout + 0.25)
            if result == "timeout":
                results[index] = {"status": "timeout", "time_ms": round((time.monotonic() - t0) * 1000, 1)}
                restart_at = index
                break
            if result is None:
                time.sleep(0.05)
                results[index] = {"status": "crash",
                                  "message": "".join(stderr_lines)[-500:].strip() or "process died (out of memory or stack?)"}
                restart_at = index
                break
            raw = {k: v for k, v in result.items() if k not in ("event", "index")}
            if raw.get("status") == "ok" and raw.get("time_ms", 0) > timeout * 1000:
                raw = {"status": "timeout", "time_ms": raw["time_ms"]}
            results[index] = raw
            index += 1
        stop()
        start = count if restart_at is None else restart_at + 1
    return [r or {"status": "crash", "message": "not run"} for r in results]


# ---------------------------------------------------------------- comparison

def _is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def values_equal(a, b, tol: float | None = None) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if _is_num(a) and _is_num(b):
        if tol is not None:
            return abs(a - b) <= tol * max(1.0, abs(b))
        return a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(values_equal(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(values_equal(a[k], b[k], tol) for k in a)
    return a == b


def _canon(x, deep: bool):
    if isinstance(x, list):
        items = [_canon(v, deep) for v in x] if deep else x
        return sorted(items, key=lambda v: json.dumps(v, sort_keys=True))
    return x


def compare(actual, expected, spec: dict | None) -> bool:
    mode = (spec or {}).get("mode", "exact")
    tol = (spec or {}).get("tolerance", 1e-6) if mode == "float" else None
    if mode == "unordered" and isinstance(actual, list) and isinstance(expected, list):
        return values_equal(_canon(actual, False), _canon(expected, False))
    if mode == "unordered_deep" and isinstance(actual, list) and isinstance(expected, list):
        return values_equal(_canon(actual, True), _canon(expected, True))
    return values_equal(actual, expected, tol)


def grade(tests: list[dict], raw: list[dict], compare_spec: dict | None, reveal_hidden: bool = False) -> list[dict]:
    cases = []
    for test, r in zip(tests, raw):
        hidden = test.get("visibility") == "hidden" and not reveal_hidden
        status = r["status"]
        if status == "ok":
            status = "pass" if compare(r.get("actual"), test["expected"], compare_spec) else "fail"
        case = {"id": test["id"], "visibility": test.get("visibility", "visible"),
                "category": test.get("category", ""), "status": status}
        if "time_ms" in r:
            case["time_ms"] = r["time_ms"]
        if status == "error":
            case["error_type"] = r.get("error_type")
            if r.get("line"):
                case["line"] = r["line"]
            if r.get("at_import"):
                case["at_import"] = True
        if not hidden and status != "pass":
            case["input"] = test["input"]
            case["expected"] = test["expected"]
            if status == "fail":
                case["actual"] = r.get("actual")
            if r.get("message"):
                case["message"] = r["message"]
            if r.get("stdout"):
                case["stdout"] = r["stdout"]
        cases.append(case)
    return cases


# ---------------------------------------------------------------- reporting

def _short(value, limit: int = 160) -> str:
    text = json.dumps(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def text_report(report: dict) -> str:
    lines = [f"{report['slug']}: {report['passed']}/{report['total']} passed"
             + ("  ✓ all tests pass" if report["all_passed"] else "")]
    labels = {"pass": "PASS", "fail": "FAIL", "error": "ERROR", "timeout": "TIMEOUT", "crash": "CRASH"}
    for c in report["cases"]:
        name = c["id"] if c["visibility"] == "visible" else f"hidden: {c['category'] or c['id']}"
        timing = f"{c['time_ms']:.1f} ms" if "time_ms" in c and c["status"] != "timeout" else ""
        if c["status"] == "timeout":
            timing = f"> {report['timeout_s']} s"
        lines.append(f"  {labels[c['status']]:<7} {name:<36} {timing}")
        if c["status"] == "error":
            where = f" at line {c['line']}" if c.get("line") else ""
            msg = f": {c['message']}" if c.get("message") else ""
            lines.append(f"          {c.get('error_type')}{where}{msg}")
        if "input" in c:
            lines.append(f"          input:    {_short(c['input'])}")
            lines.append(f"          expected: {_short(c['expected'])}")
            if "actual" in c:
                lines.append(f"          actual:   {_short(c['actual'])}")
        if c.get("stdout"):
            lines.append(f"          printed:  {_short(c['stdout'].strip())}")
    return "\n".join(lines)


def run(slug: str, solution: Path | None = None, reference: bool = False, only: str | None = None,
        timeout: float = DEFAULT_TIMEOUT, language: str = "python") -> dict:
    problem_dir = find_problem(slug)
    meta = load_meta(problem_dir)
    tests = load_tests(problem_dir)
    if reference:
        solution = problem_dir / runner_config(language)["reference_file"]
    elif solution is None:
        solution = workspace_solution(slug, language)
    solution = Path(solution).resolve()
    if not solution.exists():
        raise TutorError(f"no solution at {rel(solution)}; scaffold it with: "
                         f"python scripts/new_problem.py workspace {slug}")
    if only:
        tests = [t for t in tests if t.get("visibility", "visible") == only]
        raw = execute_cases(solution, tests, problem_dir / "meta.json", timeout, language)
    else:
        raw = execute(solution, problem_dir / "tests.json", problem_dir / "meta.json", len(tests), timeout, language)
    cases = grade(tests, raw, meta.get("compare"))
    passed = sum(c["status"] == "pass" for c in cases)
    return {"ok": True, "slug": slug, "solution": rel(solution), "passed": passed, "total": len(cases),
            "all_passed": passed == len(cases), "timeout_s": timeout, "cases": cases}


def execute_cases(solution: Path, tests: list[dict], meta_path: Path,
                  timeout: float = DEFAULT_TIMEOUT, language: str = "python") -> list[dict]:
    """Like execute(), for an in-memory list of cases (written to a temp tests.json)."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "tests.json"
        path.write_text(json.dumps({"schema_version": 1, "tests": tests}), encoding="utf-8")
        return execute(solution, path, meta_path, len(tests), timeout, language)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--solution", type=Path, help="solution file (default: workspace/<slug>/solution.py)")
    ap.add_argument("--reference", action="store_true", help="run the reference solution (self-check)")
    ap.add_argument("--only", choices=("visible", "hidden"))
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="seconds per test (default 2)")
    ap.add_argument("--language", default="python")
    fmt = ap.add_mutually_exclusive_group()
    fmt.add_argument("--json", action="store_true")
    fmt.add_argument("--text", action="store_true")
    args = ap.parse_args()
    report = run(args.slug, args.solution, args.reference, args.only, args.timeout, args.language)
    use_text = args.text or (not args.json and sys.stdout.isatty())
    if use_text:
        print(text_report(report))
    else:
        emit(report)
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    run_main(main)
