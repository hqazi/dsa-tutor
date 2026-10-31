#!/usr/bin/env python3
"""Learner state: the only way the agent reads or changes state/.

    python scripts/state.py status                       # onboarded? focus, levels, open attempts
    python scripts/state.py profile show
    python scripts/state.py profile set goal=interview interview_date=2026-12-15 comfort.basics=some
    python scripts/state.py profile defaults             # "skip" during onboarding
    python scripts/state.py focus TOPIC | --clear
    python scripts/state.py next [--topic T] [--difficulty D] [--dry-run]
    python scripts/state.py start SLUG                   # open an attempt + scaffold workspace
    python scripts/state.py hint SLUG                    # count a hint; returns the ladder level to give
    python scripts/state.py explained SLUG               # note that the explanation was viewed
    python scripts/state.py record SLUG --passed N --total M [--gave-up] [--notes TEXT]
    python scripts/state.py attempts [--slug S] [--last N]
    python scripts/state.py rebuild                      # recompute progress.json from attempts.jsonl

Files: state/profile.json, state/progress.json, state/attempts.jsonl. Every
write is atomic and every file carries schema_version. progress.json is
derived from attempts.jsonl (plus open attempts) and can always be rebuilt.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    SCHEMA_VERSION, STATE_DIR, TutorError, atomic_write_json, atomic_write_text, check_schema,
    emit, find_problem, iter_problems, load_json, load_meta, load_topics, now_iso, rel,
    run_main, topic_groups, topic_map,
)

PROFILE = STATE_DIR / "profile.json"
PROGRESS = STATE_DIR / "progress.json"
ATTEMPTS = STATE_DIR / "attempts.jsonl"

COMFORTABLE_AFTER = 3      # unaided solves (distinct problems) for "comfortable"
MEDIUM_AFTER = 2           # unaided solves before medium problems are recommended
MAX_HINT_LEVEL = 4
OUTCOMES = ("unaided", "with_hints", "gave_up")
COMFORT = ("none", "some", "solid")
CHOICES = {
    "goal": ("interview", "general"),
    "experience": ("beginner", "intermediate", "advanced"),
    "hint_preference": ("early", "struggle"),
}
LEVEL_RANK = {"new": 0, "learning": 1, "comfortable": 2}


# ---------------------------------------------------------------- profile

def default_profile() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "goal": "general",
        "interview_date": None,
        "experience": "beginner",
        "comfort": {g: "none" for g in topic_groups()},
        "hint_preference": "early",
        "focus_topic": None,
    }


def load_profile() -> dict | None:
    data = load_json(PROFILE)
    return check_schema(data, PROFILE) if data is not None else None


def save_profile(profile: dict) -> None:
    profile["updated_at"] = now_iso()
    atomic_write_json(PROFILE, profile)


def set_profile_value(profile: dict, key: str, raw: str) -> None:
    value: str | None = raw.strip()
    if value.lower() in ("", "null", "none") and key in ("interview_date", "focus_topic"):
        value = None
    if key in CHOICES:
        if value not in CHOICES[key]:
            raise TutorError(f"{key} must be one of {CHOICES[key]}")
        profile[key] = value
    elif key == "interview_date":
        if value is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise TutorError("interview_date must look like YYYY-MM-DD (or null)")
        profile[key] = value
    elif key == "focus_topic":
        if value is not None and value not in topic_map():
            raise TutorError(f"unknown topic {value!r}; topics: {', '.join(topic_map())}")
        profile[key] = value
    elif key.startswith("comfort."):
        group = key.split(".", 1)[1]
        if group == "all":
            groups = topic_groups()
        elif group in topic_groups():
            groups = [group]
        else:
            raise TutorError(f"unknown group {group!r}; groups: {', '.join(topic_groups())}")
        if value not in COMFORT:
            raise TutorError(f"comfort must be one of {COMFORT}")
        for g in groups:
            profile.setdefault("comfort", {})[g] = value
    else:
        raise TutorError(f"unknown profile key {key!r}; keys: goal, interview_date, experience, "
                         "comfort.<group>|comfort.all, hint_preference, focus_topic")


# ---------------------------------------------------------------- attempts & progress

def read_attempts() -> list[dict]:
    if not ATTEMPTS.exists():
        return []
    out = []
    for n, line in enumerate(ATTEMPTS.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TutorError(f"state/attempts.jsonl line {n} is not valid JSON: {exc}") from exc
        check_schema(rec, ATTEMPTS)
        out.append(rec)
    return out


def append_attempt(record: dict) -> None:
    existing = ATTEMPTS.read_text(encoding="utf-8") if ATTEMPTS.exists() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    atomic_write_text(ATTEMPTS, existing + json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def load_progress() -> dict:
    data = load_json(PROGRESS)
    if data is None:
        return {"schema_version": SCHEMA_VERSION, "updated_at": now_iso(), "topics": {}, "active": {}}
    check_schema(data, PROGRESS)
    data.setdefault("topics", {})
    data.setdefault("active", {})
    return data


def level_for(stats: dict) -> str:
    if stats.get("solved_unaided", 0) >= COMFORTABLE_AFTER:
        return "comfortable"
    if stats.get("attempted", 0) > 0:
        return "learning"
    return "new"


def compute_topics(attempts: list[dict], active: dict) -> dict:
    sets: dict[str, dict[str, set]] = {}
    last: dict[str, str] = {}

    def bucket(topic):
        return sets.setdefault(topic, {"attempted": set(), "solved": set(), "solved_unaided": set()})

    for a in attempts:
        b = bucket(a["topic"])
        b["attempted"].add(a["slug"])
        if a["outcome"] in ("unaided", "with_hints"):
            b["solved"].add(a["slug"])
        if a["outcome"] == "unaided":
            b["solved_unaided"].add(a["slug"])
        stamp = a.get("ended_at") or a.get("started_at")
        if stamp and stamp > last.get(a["topic"], ""):
            last[a["topic"]] = stamp
    for slug, info in active.items():
        bucket(info["topic"])["attempted"].add(slug)
        if info.get("started_at", "") > last.get(info["topic"], ""):
            last[info["topic"]] = info["started_at"]
    topics = {}
    for topic, b in sets.items():
        stats = {k: len(v) for k, v in b.items()}
        stats["last_practised"] = last.get(topic)
        stats["level"] = level_for(stats)
        topics[topic] = stats
    return topics


def save_progress(progress: dict, attempts: list[dict] | None = None) -> dict:
    attempts = read_attempts() if attempts is None else attempts
    progress["topics"] = compute_topics(attempts, progress.get("active", {}))
    progress["schema_version"] = SCHEMA_VERSION
    progress["updated_at"] = now_iso()
    atomic_write_json(PROGRESS, progress)
    return progress


def topic_stats(progress: dict, topic: str) -> dict:
    stats = progress["topics"].get(topic) or {"attempted": 0, "solved": 0, "solved_unaided": 0,
                                               "last_practised": None}
    stats = dict(stats)
    stats["level"] = level_for(stats)
    return stats


def problem_info(slug: str) -> tuple[Path, dict]:
    problem_dir = find_problem(slug)
    return problem_dir, load_meta(problem_dir)


# ---------------------------------------------------------------- recommendation

def attempted_slugs(progress: dict, attempts: list[dict]) -> set[str]:
    return {a["slug"] for a in attempts} | set(progress.get("active", {}))


def pick_problem(topic: str, difficulty: str, seen: set[str]) -> tuple[Path, dict] | None:
    curated, generated = [], []
    for problem_dir, meta in iter_problems():
        if meta.get("topic") != topic or meta.get("difficulty") != difficulty or meta["slug"] in seen:
            continue
        (curated if meta.get("source") == "curated" else generated).append((problem_dir, meta))
    pool = curated or generated
    return pool[0] if pool else None


def recommend(profile: dict, progress: dict, attempts: list[dict], topic: str | None,
              difficulty: str | None) -> dict:
    topics = load_topics()
    tmap = {t["id"]: t for t in topics}
    comfort = profile.get("comfort", {})
    rank = {"none": 0, "some": 1, "solid": 2}

    def level(tid):
        return topic_stats(progress, tid)["level"]

    def prereq_met(tid):
        t = tmap[tid]
        return level(tid) == "comfortable" or comfort.get(t["group"]) == "solid"

    focus = profile.get("focus_topic")
    focus_changed = False
    if topic:
        if topic not in tmap:
            raise TutorError(f"unknown topic {topic!r}; topics: {', '.join(tmap)}")
        chosen, reason = topic, "you asked for this topic"
    elif focus in tmap and level(focus) != "comfortable":
        u = topic_stats(progress, focus)["solved_unaided"]
        chosen = focus
        reason = (f"staying on your focus topic, {tmap[focus]['name']}, until it is comfortable "
                  f"({u}/{COMFORTABLE_AFTER} unaided solves)")
    else:
        candidates = [t for t in topics if level(t["id"]) != "comfortable"
                      and all(prereq_met(p) for p in t["prerequisites"] if p in tmap)]
        prefix = f"{tmap[focus]['name']} is comfortable now; " if focus in tmap else ""
        if candidates:
            order = {t["id"]: i for i, t in enumerate(topics)}
            best = min(candidates, key=lambda t: (rank.get(comfort.get(t["group"], "none"), 0),
                                                  topic_stats(progress, t["id"])["solved_unaided"],
                                                  order[t["id"]]))
            chosen = best["id"]
            reason = prefix + f"{best['name']} is your weakest topic whose prerequisites you have covered"
        else:
            # Everything comfortable: revisit the topic practised longest ago.
            chosen = min(topics, key=lambda t: topic_stats(progress, t["id"])["last_practised"] or "")["id"]
            reason = prefix + f"every topic is comfortable; {tmap[chosen]['name']} is the one practised longest ago"
        if chosen != focus:
            focus_changed = True

    unaided = topic_stats(progress, chosen)["solved_unaided"]
    if difficulty:
        diff = difficulty
    else:
        diff = "easy" if unaided < MEDIUM_AFTER else "medium"
        reason += (f"; easy until {MEDIUM_AFTER} unaided solves here ({unaided} so far)" if diff == "easy"
                   else f"; medium now that you have {unaided} unaided solves here")

    result = {"ok": True, "topic": chosen, "topic_name": tmap[chosen]["name"], "difficulty": diff,
              "focus_changed": focus_changed}
    unfinished = sorted(progress.get("active", {}))
    if unfinished:
        result["unfinished"] = unfinished
    picked = pick_problem(chosen, diff, attempted_slugs(progress, attempts))
    if picked:
        problem_dir, meta = picked
        result.update({"action": "solve", "slug": meta["slug"], "title": meta["title"],
                       "source": meta.get("source"), "problem": rel(problem_dir / "problem.md"),
                       "reason": reason})
    else:
        result.update({"action": "generate", "reason": reason + "; no unattempted problem left here, "
                       "so generate one (references/problem_spec.md)"})
    return result


# ---------------------------------------------------------------- commands

def require_profile() -> dict:
    profile = load_profile()
    if profile is None:
        raise TutorError("not onboarded yet: run the questionnaire (references/questionnaire.md), "
                         "or `state.py profile defaults` to skip it")
    return profile


def cmd_status(args) -> dict:
    profile = load_profile()
    progress = load_progress()
    attempts = read_attempts()
    tmap = topic_map()
    levels = []
    for tid, t in tmap.items():
        s = topic_stats(progress, tid)
        if s["attempted"] or tid == (profile or {}).get("focus_topic"):
            levels.append({"topic": tid, "level": s["level"], "attempted": s["attempted"],
                           "solved": s["solved"], "solved_unaided": s["solved_unaided"],
                           "last_practised": s["last_practised"]})
    out = {"ok": True, "onboarded": profile is not None}
    if profile:
        out["profile"] = {k: profile.get(k) for k in ("goal", "interview_date", "experience",
                                                      "hint_preference", "focus_topic", "comfort")}
    out["topics"] = levels
    out["untouched_topics"] = sum(1 for tid in tmap if not progress["topics"].get(tid, {}).get("attempted"))
    out["active"] = [{"slug": s, **{k: v for k, v in a.items() if k in ("topic", "hints_used", "started_at")}}
                     for s, a in progress["active"].items()]
    out["recent"] = [{k: a.get(k) for k in ("slug", "outcome", "ended_at")} for a in attempts[-3:]]
    return out


def cmd_profile(args) -> dict:
    if args.action == "show":
        return {"ok": True, "profile": require_profile()}
    if args.action == "defaults":
        profile = load_profile() or default_profile()
        if args.pairs:
            raise TutorError("profile defaults takes no key=value pairs")
        save_profile(profile)
        return {"ok": True, "profile": profile, "note": "defaults saved; any answer can be changed later"}
    profile = load_profile() or default_profile()
    if not args.pairs:
        raise TutorError("give key=value pairs, e.g. goal=interview")
    for pair in args.pairs:
        if "=" not in pair:
            raise TutorError(f"expected key=value, got {pair!r}")
        key, value = pair.split("=", 1)
        set_profile_value(profile, key.strip(), value)
    if profile.get("goal") == "general":
        profile["interview_date"] = None
    save_profile(profile)
    return {"ok": True, "profile": profile}


def cmd_focus(args) -> dict:
    profile = require_profile()
    if args.clear:
        profile["focus_topic"] = None
    elif args.topic:
        set_profile_value(profile, "focus_topic", args.topic)
    else:
        raise TutorError("give a topic or --clear")
    save_profile(profile)
    return {"ok": True, "focus_topic": profile["focus_topic"]}


def cmd_next(args) -> dict:
    profile = require_profile()
    progress = load_progress()
    attempts = read_attempts()
    result = recommend(profile, progress, attempts, args.topic, args.difficulty)
    if result["focus_changed"] and not args.dry_run:
        profile["focus_topic"] = result["topic"]
        save_profile(profile)
    return result


def cmd_start(args) -> dict:
    import new_problem  # local import: only needed here
    problem_dir, meta = problem_info(args.slug)
    progress = load_progress()
    active = progress["active"]
    resumed = args.slug in active
    if not resumed:
        active[args.slug] = {"topic": meta["topic"], "difficulty": meta["difficulty"],
                             "source": meta.get("source"), "started_at": now_iso(),
                             "hints_used": 0, "explanation_viewed": False}
        save_progress(progress)
    path, created = new_problem.scaffold_workspace(args.slug)
    return {"ok": True, "slug": args.slug, "resumed": resumed, "problem": rel(problem_dir / "problem.md"),
            "workspace": rel(path), "workspace_created": created,
            "hints_used": active[args.slug]["hints_used"]}


def _active(progress: dict, slug: str) -> dict:
    if slug not in progress["active"]:
        _, meta = problem_info(slug)
        progress["active"][slug] = {"topic": meta["topic"], "difficulty": meta["difficulty"],
                                    "source": meta.get("source"), "started_at": now_iso(),
                                    "hints_used": 0, "explanation_viewed": False}
    return progress["active"][slug]


def cmd_hint(args) -> dict:
    profile = load_profile() or default_profile()
    progress = load_progress()
    attempt = _active(progress, args.slug)
    if attempt["hints_used"] >= MAX_HINT_LEVEL:
        save_progress(progress)
        return {"ok": True, "slug": args.slug, "level": None, "hints_used": attempt["hints_used"],
                "note": "all four hint levels used; offer the full explanation (render_explanation.py)"}
    attempt["hints_used"] += 1
    save_progress(progress)
    return {"ok": True, "slug": args.slug, "level": attempt["hints_used"], "max_level": MAX_HINT_LEVEL,
            "hint_preference": profile.get("hint_preference"), "guide": "references/hint_ladder.md"}


def cmd_explained(args) -> dict:
    progress = load_progress()
    attempt = _active(progress, args.slug)
    attempt["explanation_viewed"] = True
    save_progress(progress)
    return {"ok": True, "slug": args.slug, "explanation_viewed": True}


def cmd_record(args) -> dict:
    progress = load_progress()
    attempts = read_attempts()
    _, meta = problem_info(args.slug)
    if args.passed < 0 or args.total <= 0 or args.passed > args.total:
        raise TutorError("need 0 <= passed <= total and total > 0")
    attempt = progress["active"].pop(args.slug, None) or {
        "started_at": None, "hints_used": 0, "explanation_viewed": False}
    if args.outcome:
        outcome = args.outcome
    elif args.gave_up or args.passed < args.total:
        outcome = "gave_up"
    elif attempt["hints_used"] or attempt.get("explanation_viewed"):
        outcome = "with_hints"
    else:
        outcome = "unaided"
    if outcome != "gave_up" and args.passed < args.total:
        raise TutorError("only a run where every test passes counts as solved; use outcome gave_up")
    before = topic_stats(progress, meta["topic"])["level"]
    record = {
        "schema_version": SCHEMA_VERSION,
        "slug": args.slug,
        "topic": meta["topic"],
        "difficulty": meta["difficulty"],
        "source": meta.get("source"),
        "started_at": attempt.get("started_at"),
        "ended_at": now_iso(),
        "hints_used": attempt.get("hints_used", 0),
        "explanation_viewed": bool(attempt.get("explanation_viewed")),
        "tests_passed": args.passed,
        "tests_total": args.total,
        "outcome": outcome,
        "notes": (args.notes or "").strip()[:600],
    }
    append_attempt(record)
    attempts.append(record)
    save_progress(progress, attempts)
    after = topic_stats(progress, meta["topic"])
    return {"ok": True, "recorded": {k: record[k] for k in ("slug", "outcome", "hints_used", "tests_passed",
                                                            "tests_total")},
            "topic": meta["topic"], "level": after["level"], "level_changed": after["level"] != before,
            "solved_unaided": after["solved_unaided"]}


def cmd_attempts(args) -> dict:
    attempts = read_attempts()
    if args.slug:
        attempts = [a for a in attempts if a["slug"] == args.slug]
    return {"ok": True, "attempts": attempts[-args.last:] if args.last else attempts}


def cmd_rebuild(args) -> dict:
    progress = load_progress()
    save_progress(progress)
    return {"ok": True, "topics": progress["topics"]}


def cmd_init(args) -> dict:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not PROGRESS.exists():
        save_progress(load_progress(), [])
    return {"ok": True, "onboarded": PROFILE.exists()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    p = sub.add_parser("profile")
    p.add_argument("action", choices=("show", "set", "defaults"))
    p.add_argument("pairs", nargs="*")
    f = sub.add_parser("focus")
    f.add_argument("topic", nargs="?")
    f.add_argument("--clear", action="store_true")
    n = sub.add_parser("next")
    n.add_argument("--topic")
    n.add_argument("--difficulty", choices=("easy", "medium", "hard"))
    n.add_argument("--dry-run", action="store_true", help="do not move the focus topic")
    for name in ("start", "hint", "explained"):
        sub.add_parser(name).add_argument("slug")
    r = sub.add_parser("record")
    r.add_argument("slug")
    r.add_argument("--passed", type=int, required=True)
    r.add_argument("--total", type=int, required=True)
    r.add_argument("--gave-up", action="store_true")
    r.add_argument("--outcome", choices=OUTCOMES, help="override the derived outcome")
    r.add_argument("--notes", help="short reviewer notes (kept to 600 characters)")
    a = sub.add_parser("attempts")
    a.add_argument("--slug")
    a.add_argument("--last", type=int, default=10)
    sub.add_parser("rebuild")
    args = ap.parse_args()
    handler = {"init": cmd_init, "status": cmd_status, "profile": cmd_profile, "focus": cmd_focus,
               "next": cmd_next, "start": cmd_start, "hint": cmd_hint, "explained": cmd_explained,
               "record": cmd_record, "attempts": cmd_attempts, "rebuild": cmd_rebuild}[args.cmd]
    emit(handler(args))
    return 0


if __name__ == "__main__":
    run_main(main)
