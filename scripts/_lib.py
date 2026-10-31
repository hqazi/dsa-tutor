"""Shared helpers for the DSA tutor scripts. Standard library only, Python 3.10+."""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
PROBLEMS_DIR = ROOT / "problems"
CURATED_DIR = PROBLEMS_DIR / "curated"
GENERATED_DIR = PROBLEMS_DIR / "generated"
WORKSPACE_DIR = ROOT / "workspace"
EXPLANATIONS_DIR = ROOT / "explanations"
REFERENCES_DIR = ROOT / "references"
RUNNERS_DIR = ROOT / "runners"
ASSETS_DIR = ROOT / "assets"

SCHEMA_VERSION = 1
DIFFICULTIES = ("easy", "medium", "hard")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class TutorError(Exception):
    """An error reported to the caller as {"ok": false, "error": ...}."""


# ---------------------------------------------------------------- output

def emit(obj: Any) -> None:
    """Print compact JSON (the scripts' contract with the agent)."""
    print(json.dumps(obj, separators=(",", ":"), ensure_ascii=False))


def run_main(main) -> None:
    """Run a script's main(), turning TutorError into a JSON error and exit 2."""
    try:
        code = main()
    except TutorError as exc:
        emit({"ok": False, "error": str(exc)})
        sys.exit(2)
    sys.exit(code or 0)


def rel(path: Path | str) -> str:
    """Path relative to the repo root, with forward slashes."""
    p = Path(path).resolve()
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


# ---------------------------------------------------------------- time

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


# ---------------------------------------------------------------- files

def load_json(path: Path, default: Any = None) -> Any:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as exc:
        raise TutorError(f"{rel(path)} is not valid JSON: {exc}") from exc


def atomic_write_text(path: Path, text: str) -> None:
    """Write via a temp file in the same folder, then rename over the target."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def check_schema(data: dict, path: Path) -> dict:
    version = data.get("schema_version")
    if not isinstance(version, int):
        raise TutorError(f"{rel(path)} has no schema_version")
    if version > SCHEMA_VERSION:
        raise TutorError(
            f"{rel(path)} uses schema_version {version}, newer than these scripts "
            f"({SCHEMA_VERSION}); update the scripts from upstream"
        )
    return data


# ---------------------------------------------------------------- topics

def load_topics() -> list[dict]:
    """Parse the topic table in references/topics.md, in teaching order."""
    path = REFERENCES_DIR / "topics.md"
    topics: list[dict] = []
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            if in_table:
                break
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if cells[0] == "id":
            in_table = True
            continue
        if not in_table or set(cells[0]) <= set("-: "):
            continue
        tid, name, group, prereqs = cells[0], cells[1], cells[2], cells[3]
        if not SLUG_RE.match(tid):
            continue
        req = [] if prereqs in ("", "-", "—") else [p.strip() for p in prereqs.split(",") if p.strip()]
        topics.append({"id": tid, "name": name, "group": group, "prerequisites": req})
    if not topics:
        raise TutorError("no topics found in references/topics.md")
    return topics


def topic_map() -> dict[str, dict]:
    return {t["id"]: t for t in load_topics()}


def topic_groups() -> list[str]:
    seen: list[str] = []
    for t in load_topics():
        if t["group"] not in seen:
            seen.append(t["group"])
    return seen


# ---------------------------------------------------------------- problems

def iter_problems() -> Iterator[tuple[Path, dict]]:
    """Yield (problem_dir, meta) for every curated and generated problem."""
    metas = sorted(CURATED_DIR.glob("*/*/meta.json")) + sorted(GENERATED_DIR.glob("*/meta.json"))
    for meta_path in metas:
        meta = load_json(meta_path)
        if isinstance(meta, dict):
            yield meta_path.parent, meta


def find_problem(slug: str) -> Path:
    if not SLUG_RE.match(slug or ""):
        raise TutorError(f"invalid slug {slug!r}")
    generated = GENERATED_DIR / slug
    if (generated / "meta.json").exists():
        return generated
    for meta_path in CURATED_DIR.glob(f"*/{slug}/meta.json"):
        return meta_path.parent
    raise TutorError(f"no problem with slug {slug!r}")


def load_meta(problem_dir: Path) -> dict:
    return check_schema(load_json(problem_dir / "meta.json"), problem_dir / "meta.json")


def load_tests(problem_dir: Path) -> list[dict]:
    data = check_schema(load_json(problem_dir / "tests.json"), problem_dir / "tests.json")
    return data["tests"]


def workspace_solution(slug: str, language: str = "python") -> Path:
    return WORKSPACE_DIR / slug / runner_config(language)["solution_file"]


def runner_config(language: str) -> dict:
    path = RUNNERS_DIR / language / "runner.json"
    config = load_json(path)
    if not config:
        raise TutorError(f"no runner for language {language!r} (expected {rel(path)})")
    return config
