#!/usr/bin/env python3
"""Python runner: call a solution function on each case in tests.json.

Usage:
    harness.py --solution PATH --tests PATH --meta PATH [--start N]

The harness never compares results; run_tests.py does that, so every runner
only has to turn JSON inputs into native values and native results back into
JSON. Protocol: one line per event on stdout, each prefixed with "@@dsa ":

    {"event": "ready", "count": N}
    {"event": "begin", "index": i}
    {"event": "result", "index": i, "status": "ok", "actual": ..., "time_ms": t, "stdout": "..."}
    {"event": "result", "index": i, "status": "error", "error_type": ..., "message": ..., "line": n, "stdout": "..."}
    {"event": "import_error", "error_type": ..., "message": ..., "line": n}
    {"event": "done"}

Linked lists and binary trees travel as JSON lists (trees in level order with
nulls) and are converted when the signature's type names ListNode or TreeNode.
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import math
import sys
import threading
import time
import traceback
from collections import deque
from pathlib import Path

PREFIX = "@@dsa "


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------- conversion

def build_list(values, cls):
    head = None
    for v in reversed(values or []):
        head = cls(v, head)
    return head


def build_tree(values, cls):
    if not values or values[0] is None:
        return None
    root = cls(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = cls(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = cls(values[i])
            queue.append(node.right)
        i += 1
    return root


def list_to_json(node, limit=1_000_000):
    out = []
    while node is not None:
        out.append(node.val)
        node = node.next
        if len(out) > limit:
            raise ValueError("linked list is too long (cycle?)")
    return out


def tree_to_json(root):
    if root is None:
        return []
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def convert_in(value, type_str, module):
    t = (type_str or "").replace(" ", "")
    if "ListNode" in t:
        cls = getattr(module, "ListNode", ListNode)
        if t.startswith("list[list") or t.startswith("list[ListNode"):
            return [build_list(v, cls) for v in value]
        return build_list(value, cls)
    if "TreeNode" in t:
        cls = getattr(module, "TreeNode", TreeNode)
        return build_tree(value, cls)
    return value


def to_json(value, type_str=""):
    t = (type_str or "").replace(" ", "")
    if "ListNode" in t and not t.startswith("list["):
        return list_to_json(value)
    if "TreeNode" in t and not t.startswith("list["):
        return tree_to_json(value)
    return plain(value)


def plain(value):
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return str(value)
        return value
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, (set, frozenset)):
        items = [plain(v) for v in value]
        try:
            return sorted(items)
        except TypeError:
            return sorted(items, key=lambda v: json.dumps(v, sort_keys=True))
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if hasattr(value, "next") and hasattr(value, "val"):
        return list_to_json(value)
    if hasattr(value, "left") and hasattr(value, "right") and hasattr(value, "val"):
        return tree_to_json(value)
    raise TypeError(f"return value of type {type(value).__name__} cannot be turned into JSON")


# ---------------------------------------------------------------- running

def error_info(exc, solution_path):
    """Exception type, message, and the last line in the solution file it passed through."""
    line = None
    for frame in traceback.extract_tb(exc.__traceback__):
        if Path(frame.filename).resolve() == solution_path:
            line = frame.lineno
    if isinstance(exc, SyntaxError) and exc.lineno and line is None:
        line = exc.lineno
    return {"error_type": type(exc).__name__, "message": str(exc)[:500], "line": line}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solution", required=True)
    ap.add_argument("--tests", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--start", type=int, default=0)
    args = ap.parse_args()

    out = sys.stdout

    def send(obj):
        out.write(PREFIX + json.dumps(obj, separators=(",", ":")) + "\n")
        out.flush()

    with open(args.meta, encoding="utf-8") as f:
        meta = json.load(f)
    with open(args.tests, encoding="utf-8") as f:
        tests = json.load(f)["tests"]
    sig = meta["signatures"]["python"]
    param_types = {p["name"]: p.get("type", "") for p in sig["params"]}
    solution_path = Path(args.solution).resolve()

    captured = io.StringIO()
    sys.stdout = captured
    try:
        spec = importlib.util.spec_from_file_location("solution", solution_path)
        module = importlib.util.module_from_spec(spec)
        module.ListNode = ListNode
        module.TreeNode = TreeNode
        sys.path.insert(0, str(solution_path.parent))
        spec.loader.exec_module(module)
        func = getattr(module, sig["function"], None)
        if not callable(func):
            raise AttributeError(f"solution does not define a function named {sig['function']!r}")
    except BaseException as exc:  # noqa: BLE001 - report anything, including SystemExit
        sys.stdout = out
        send({"event": "import_error", **error_info(exc, solution_path)})
        return
    sys.stdout = out
    send({"event": "ready", "count": len(tests)})

    for index in range(args.start, len(tests)):
        case = tests[index]
        send({"event": "begin", "index": index})
        captured = io.StringIO()
        sys.stdout = captured
        try:
            kwargs = {name: convert_in(case["input"][name], param_types.get(name, ""), module)
                      for name in param_types}
            t0 = time.perf_counter()
            result = func(**kwargs)
            elapsed = (time.perf_counter() - t0) * 1000
            actual = to_json(result, sig.get("returns", ""))
            json.dumps(actual)
            record = {"status": "ok", "actual": actual, "time_ms": round(elapsed, 3)}
        except RecursionError as exc:
            record = {"status": "error", **error_info(exc, solution_path)}
            record["message"] = "maximum recursion depth exceeded"
        except BaseException as exc:  # noqa: BLE001
            record = {"status": "error", **error_info(exc, solution_path)}
        sys.stdout = out
        record["stdout"] = captured.getvalue()[-2000:]
        send({"event": "result", "index": index, **record})
    send({"event": "done"})


if __name__ == "__main__":
    sys.setrecursionlimit(200_000)
    try:
        threading.stack_size(512 * 1024 * 1024)
    except (ValueError, RuntimeError):
        try:
            threading.stack_size(64 * 1024 * 1024)
        except (ValueError, RuntimeError):
            pass
    worker = threading.Thread(target=main)
    worker.start()
    worker.join()
