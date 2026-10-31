#!/usr/bin/env python3
"""Fill assets/explanation.html and write explanations/<slug>.html.

    python scripts/render_explanation.py CONTENT.json [--no-state]

CONTENT.json (text fields accept light Markdown: paragraphs, - lists, 1. lists,
`code`, **bold**, *italic*, ```python fences):

    {
      "slug": "pair-with-target",
      "plain_words": "...",
      "intuition": "...",
      "brute_force": {"idea": "...", "time": "O(n^2)", "space": "O(1)", "code": "optional python"},
      "optimal":     {"idea": "...", "time": "O(n)",   "space": "O(n)"},
      "trace": {"intro": "...", "columns": ["step", "i", "seen", "note"], "rows": [["1", "0", "{}", "..."]],
                "outro": "..."},                    # or a Markdown string
      "complexity": {"time": "O(n)", "space": "O(n)", "why": "..."},
      "solution": "python source with comments",
      "pitfalls": ["...", "..."]
    }

Title, topic and difficulty come from the problem's meta.json. The page is
self-contained (inline CSS, no JavaScript) and follows the system light/dark
setting. Unless --no-state is given, an open attempt on the problem is marked
as having viewed the explanation (so a later solve counts as "with hints").
"""
from __future__ import annotations

import argparse
import builtins
import html
import io
import json
import keyword
import re
import sys
import tokenize
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (  # noqa: E402
    ASSETS_DIR, EXPLANATIONS_DIR, TutorError, atomic_write_text, emit, find_problem, load_json,
    load_meta, now_iso, rel, run_main, topic_map,
)

REQUIRED = ("slug", "plain_words", "intuition", "brute_force", "optimal", "trace", "complexity",
            "solution", "pitfalls")
BUILTINS = set(dir(builtins))


# ---------------------------------------------------------------- markdown (small subset)

def inline(text: str) -> str:
    parts = re.split(r"(`[^`]*`)", text)
    out = []
    for part in parts:
        if len(part) >= 2 and part.startswith("`") and part.endswith("`"):
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        s = html.escape(part, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
        out.append(s)
    return "".join(out)


def markdown(text: str) -> str:
    if not isinstance(text, str):
        raise TutorError(f"expected Markdown text, got {type(text).__name__}")
    out: list[str] = []
    chunks = re.split(r"^```[ \t]*(\w*)[ \t]*\n(.*?)^```[ \t]*$", text.strip("\n") + "\n", flags=re.M | re.S)
    # re.split with 2 groups yields: text, lang, code, text, lang, code, ...
    for i in range(0, len(chunks), 3):
        out.extend(_blocks(chunks[i]))
        if i + 2 < len(chunks):
            lang, code = chunks[i + 1], chunks[i + 2]
            out.append(code_block(code, lang or "python"))
    return "\n".join(out)


def _blocks(text: str) -> list[str]:
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [ln.rstrip() for ln in block.strip("\n").splitlines() if ln.strip()]
        if not lines:
            continue
        if lines[0].startswith("### "):
            out.append(f"<h3>{inline(lines[0][4:])}</h3>")
            lines = lines[1:]
            if not lines:
                continue
        if all(re.match(r"\s*[-*] ", ln) or (i and ln.startswith("  ")) for i, ln in enumerate(lines)):
            out.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in _items(lines, r"\s*[-*] ")) + "</ul>")
        elif all(re.match(r"\s*\d+[.)] ", ln) or (i and ln.startswith("  ")) for i, ln in enumerate(lines)):
            out.append("<ol>" + "".join(f"<li>{inline(item)}</li>" for item in _items(lines, r"\s*\d+[.)] ")) + "</ol>")
        else:
            out.append(f"<p>{inline(' '.join(ln.strip() for ln in lines))}</p>")
    return out


def _items(lines: list[str], marker: str) -> list[str]:
    items: list[str] = []
    for ln in lines:
        m = re.match(marker, ln)
        if m:
            items.append(ln[m.end():].strip())
        else:
            items[-1] += " " + ln.strip()
    return items


# ---------------------------------------------------------------- code highlighting

def highlight_python(code: str) -> str:
    """Wrap Python tokens in spans. Falls back to plain escaped text on tokenize errors."""
    code = code.expandtabs(4).rstrip() + "\n"
    lines = code.splitlines(keepends=True)
    offsets = [0]
    for ln in lines:
        offsets.append(offsets[-1] + len(ln))
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return html.escape(code.rstrip("\n"))
    out, pos, prev = [], 0, None
    for tok in tokens:
        start = offsets[tok.start[0] - 1] + tok.start[1] if tok.start[0] <= len(lines) else len(code)
        end = offsets[tok.end[0] - 1] + tok.end[1] if tok.end[0] <= len(lines) else len(code)
        if start < pos:
            continue
        out.append(html.escape(code[pos:start]))
        text = code[start:end]
        cls = None
        if tok.type == tokenize.COMMENT:
            cls = "com"
        elif tok.type == tokenize.STRING or tok.type in _fstring_types():
            cls = "str"
        elif tok.type == tokenize.NUMBER:
            cls = "num"
        elif tok.type == tokenize.NAME:
            if keyword.iskeyword(text) or text in ("self", "cls", "match", "case"):
                cls = "kw"
            elif prev is not None and prev.type == tokenize.NAME and prev.string in ("def", "class"):
                cls = "fn"
            elif text in BUILTINS:
                cls = "bi"
        out.append(f'<span class="tok-{cls}">{html.escape(text)}</span>' if cls else html.escape(text))
        pos = end
        if tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
            prev = tok
    out.append(html.escape(code[pos:]))
    return "".join(out).rstrip("\n")


def _fstring_types() -> set[int]:
    return {getattr(tokenize, n) for n in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END") if hasattr(tokenize, n)}


def code_block(code: str, lang: str = "python") -> str:
    body = highlight_python(code) if lang in ("python", "py", "") else html.escape(code.rstrip("\n"))
    return f"<pre><code>{body}</code></pre>"


# ---------------------------------------------------------------- sections

def badges(time: str | None, space: str | None) -> str:
    parts = []
    if time:
        parts.append(f'<span class="badge">time {html.escape(time)}</span>')
    if space:
        parts.append(f'<span class="badge">space {html.escape(space)}</span>')
    return f"<p>{''.join(parts)}</p>" if parts else ""


def approach(data) -> str:
    if isinstance(data, str):
        return markdown(data)
    if not isinstance(data, dict) or "idea" not in data:
        raise TutorError("brute_force / optimal need an object with at least 'idea'")
    out = markdown(data["idea"]) + badges(data.get("time"), data.get("space"))
    if data.get("code"):
        out += code_block(data["code"])
    return out


def trace(data) -> str:
    if isinstance(data, str):
        return markdown(data)
    if not isinstance(data, dict):
        raise TutorError("trace must be Markdown text or an object with columns and rows")
    out = markdown(data["intro"]) if data.get("intro") else ""
    columns, rows = data.get("columns") or [], data.get("rows") or []
    if columns and rows:
        head = "".join(f"<th>{inline(str(c))}</th>" for c in columns)
        body = "".join("<tr>" + "".join(f"<td>{inline(str(cell))}</td>" for cell in row) + "</tr>" for row in rows)
        out += f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
    if data.get("outro"):
        out += markdown(data["outro"])
    return out


def complexity(data) -> str:
    if isinstance(data, str):
        return markdown(data)
    return badges(data.get("time"), data.get("space")) + (markdown(data["why"]) if data.get("why") else "")


def pitfalls(data) -> str:
    if isinstance(data, str):
        return markdown(data)
    if not isinstance(data, list) or not data:
        raise TutorError("pitfalls must be a non-empty list")
    return '<ul class="pitfalls">' + "".join(f"<li>{inline(str(p))}</li>" for p in data) + "</ul>"


def render(content: dict) -> tuple[str, Path]:
    missing = [k for k in REQUIRED if k not in content]
    if missing:
        raise TutorError(f"content is missing: {', '.join(missing)}")
    slug = content["slug"]
    meta = load_meta(find_problem(slug))
    topic = topic_map().get(meta["topic"], {"name": meta["topic"]})["name"]
    values = {
        "title": html.escape(meta["title"]),
        "meta": f"<span>{html.escape(topic)}</span><span>{html.escape(meta['difficulty'].capitalize())}</span>",
        "slug": html.escape(slug),
        "generated": now_iso()[:10],
        "plain_words": markdown(content["plain_words"]),
        "intuition": markdown(content["intuition"]),
        "brute_force": approach(content["brute_force"]),
        "optimal": approach(content["optimal"]),
        "trace": trace(content["trace"]),
        "complexity": complexity(content["complexity"]),
        "solution": code_block(content["solution"]),
        "pitfalls": pitfalls(content["pitfalls"]),
    }
    template = (ASSETS_DIR / "explanation.html").read_text(encoding="utf-8")
    page = re.sub(r"\{\{(\w+)\}\}", lambda m: values.get(m.group(1), m.group(0)), template)
    path = EXPLANATIONS_DIR / f"{slug}.html"
    atomic_write_text(path, page)
    return page, path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("content", help="content JSON file, or '-' for stdin")
    ap.add_argument("--no-state", action="store_true", help="do not mark the attempt as explained")
    args = ap.parse_args()
    content = json.load(sys.stdin) if args.content == "-" else load_json(Path(args.content))
    if not isinstance(content, dict):
        raise TutorError(f"content file not found or not a JSON object: {args.content}")
    _, path = render(content)
    result = {"ok": True, "slug": content["slug"], "explanation": rel(path)}
    if not args.no_state:
        import state
        progress = state.load_progress()
        if content["slug"] in progress["active"]:
            progress["active"][content["slug"]]["explanation_viewed"] = True
            state.save_progress(progress)
            result["attempt_marked_explained"] = True
    emit(result)
    return 0


if __name__ == "__main__":
    run_main(main)
