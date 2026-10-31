"""End-to-end tests for the tutor scripts.

Each test class works on a throwaway copy of the repo, so real state is never
touched. Run with:  python -m unittest discover -s tests
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class RepoCopy(unittest.TestCase):
    root: Path

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls._tmp.name) / "repo"
        shutil.copytree(REPO, cls.root, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", "state", "workspace", "explanations", "generated"))
        for d in ("state", "workspace", "explanations", "problems/generated"):
            (cls.root / d).mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def setUp(self):
        for d in ("state", "workspace", "explanations", "problems/generated"):
            shutil.rmtree(self.root / d, ignore_errors=True)
            (self.root / d).mkdir(parents=True)

    def run_script(self, script, *args, stdin=None, expect_ok=True):
        proc = subprocess.run([sys.executable, f"scripts/{script}", *args], cwd=self.root,
                              capture_output=True, text=True, input=stdin, timeout=300)
        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail(f"{script} {args} did not print JSON:\n{proc.stdout}\n{proc.stderr}")
        if expect_ok is not None:
            self.assertEqual(out.get("ok"), expect_ok, out)
        return out

    def write_solution(self, slug, code):
        path = self.root / "workspace" / slug / "solution.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code, encoding="utf-8")
        return path


class TestRunTests(RepoCopy):
    def test_reference_passes(self):
        for slug in ("pair-with-target", "reverse-chain", "valid-search-tree", "group-by-letters"):
            out = self.run_script("run_tests.py", slug, "--reference", "--json")
            self.assertTrue(out["all_passed"], (slug, out))

    def test_scaffold_fails_and_hides_hidden_data(self):
        self.run_script("new_problem.py", "workspace", "first-unique-char")
        out = self.run_script("run_tests.py", "first-unique-char", "--json")
        self.assertFalse(out["all_passed"])
        for case in out["cases"]:
            self.assertEqual(case["status"], "error")
            self.assertEqual(case["error_type"], "NotImplementedError")
            if case["visibility"] == "hidden":
                self.assertNotIn("input", case)
                self.assertNotIn("expected", case)
                self.assertTrue(case["category"])
            else:
                self.assertIn("input", case)

    def test_wrong_answer_and_timeout(self):
        self.write_solution("rotate-playlist", (
            "def shift_playlist(tracks, k):\n"
            "    if k == 0:\n"
            "        while True:\n"
            "            pass\n"
            "    return tracks\n"))
        out = self.run_script("run_tests.py", "rotate-playlist", "--json", "--timeout", "0.5")
        statuses = {c["category"]: c["status"] for c in out["cases"]}
        self.assertEqual(statuses["zero presses"], "timeout")
        visible_fail = [c for c in out["cases"] if c["visibility"] == "visible" and c["status"] == "fail"]
        self.assertTrue(visible_fail and "actual" in visible_fail[0])
        # the run continues after a timeout
        self.assertEqual(len(out["cases"]), out["total"])
        self.assertGreater(out["passed"], 0)

    def test_syntax_error_reports_line(self):
        self.write_solution("tree-depth", "def max_depth(root):\n    return (\n")
        out = self.run_script("run_tests.py", "tree-depth", "--json")
        self.assertTrue(all(c["status"] == "error" for c in out["cases"]))
        self.assertTrue(out["cases"][0].get("at_import"))

    def test_print_does_not_break_protocol(self):
        self.write_solution("count-ways", (
            "print('loading')\n"
            "def count_ways(steps):\n"
            "    print('debug', steps)\n"
            "    a, b = 1, 1\n"
            "    for _ in range(steps):\n"
            "        a, b = b, a + b\n"
            "    return a\n"))
        out = self.run_script("run_tests.py", "count-ways", "--json")
        self.assertTrue(out["all_passed"], out)

    def test_only_visible(self):
        out = self.run_script("run_tests.py", "balanced-brackets", "--reference", "--only", "visible", "--json")
        self.assertTrue(all(c["visibility"] == "visible" for c in out["cases"]))
        self.assertTrue(out["all_passed"])


SPEC = {
    "slug": "tiny-max", "title": "Tiny Max", "topic": "arrays-strings", "difficulty": "easy",
    "statement": "Return the largest value.", "constraints": ["1 <= len(nums) <= 10^5"],
    "signature": {"function": "tiny_max", "params": [{"name": "nums", "type": "list[int]"}], "returns": "int"},
    "expected_complexity": {"time": "O(n)", "space": "O(1)"},
    "tests": [
        {"visibility": "visible", "input": {"nums": [1, 5, 2]}, "expected": 5},
        {"visibility": "visible", "input": {"nums": [-3]}},
        {"visibility": "hidden", "category": "negatives", "input": {"nums": [-5, -2]}},
        {"visibility": "hidden", "category": "duplicates", "input": {"nums": [4, 4]}},
        {"visibility": "hidden", "category": "large input", "input": {"nums": list(range(20000))},
         "expected_by": "reference"},
    ],
    "reference_solution": "def tiny_max(nums):\n    best = nums[0]\n    for x in nums:\n        best = max(best, x)\n    return best\n",
    "brute_force": "def tiny_max(nums):\n    return sorted(nums)[-1]\n",
}


class TestNewProblem(RepoCopy):
    def test_create_and_scaffold(self):
        out = self.run_script("new_problem.py", "create", "-", stdin=json.dumps(SPEC))
        self.assertEqual(out["tests"], {"visible": 2, "hidden": 3})
        folder = self.root / "problems" / "generated" / "tiny-max"
        for name in ("problem.md", "meta.json", "tests.json", "reference.py"):
            self.assertTrue((folder / name).exists(), name)
        tests = json.loads((folder / "tests.json").read_text())["tests"]
        self.assertEqual(tests[1]["expected"], -3)          # from brute force
        self.assertEqual(tests[4]["expected"], 19999)       # from reference
        self.assertIn("python scripts/run_tests.py tiny-max", (folder / "problem.md").read_text())
        solution = (self.root / "workspace" / "tiny-max" / "solution.py").read_text()
        self.assertIn("def tiny_max(nums: list[int]) -> int:", solution)
        again = self.run_script("new_problem.py", "create", "-", stdin=json.dumps(SPEC), expect_ok=False)
        self.assertIn("already exists", again["error"])

    def test_self_check_rejects_wrong_expected(self):
        spec = dict(SPEC, slug="tiny-max-bad")
        spec["tests"] = [dict(t) for t in SPEC["tests"]]
        spec["tests"][0]["expected"] = 6
        out = self.run_script("new_problem.py", "create", "-", stdin=json.dumps(spec), expect_ok=False)
        self.assertIn("self-check", out["error"])
        self.assertEqual(out["failures"][0]["id"], "example-1")
        self.assertFalse((self.root / "problems" / "generated" / "tiny-max-bad").exists())

    def test_invalid_spec(self):
        spec = dict(SPEC, slug="Bad Slug", topic="nope")
        spec["tests"] = SPEC["tests"][:2]
        out = self.run_script("new_problem.py", "create", "-", stdin=json.dumps(spec), expect_ok=False)
        joined = " ".join(out["problems"])
        self.assertIn("slug", joined)
        self.assertIn("unknown topic", joined)
        self.assertIn("hidden", joined)


class TestState(RepoCopy):
    def solve(self, slug, hints=0):
        self.run_script("state.py", "start", slug)
        for _ in range(hints):
            self.run_script("state.py", "hint", slug)
        return self.run_script("state.py", "record", slug, "--passed", "5", "--total", "5")

    def test_learning_loop(self):
        status = self.run_script("state.py", "status")
        self.assertFalse(status["onboarded"])
        self.run_script("state.py", "next", expect_ok=False)  # must onboard first
        self.run_script("state.py", "profile", "set", "goal=interview", "interview_date=2026-12-15",
                        "comfort.all=some", "hint_preference=struggle", "focus_topic=hashing")
        self.run_script("state.py", "profile", "set", "comfort.basics=great", expect_ok=False)

        first = self.run_script("state.py", "next")
        self.assertEqual((first["topic"], first["difficulty"], first["action"]), ("hashing", "easy", "solve"))
        self.assertIn("focus", first["reason"])

        started = self.run_script("state.py", "start", first["slug"])
        self.assertTrue((self.root / started["workspace"]).exists())
        hint = self.run_script("state.py", "hint", first["slug"])
        self.assertEqual(hint["level"], 1)
        rec = self.run_script("state.py", "record", first["slug"], "--passed", "3", "--total", "3",
                              "--notes", "used the complement map")
        self.assertEqual(rec["recorded"]["outcome"], "with_hints")
        self.assertEqual(rec["level"], "learning")

        # Two unaided easy solves, then medium is recommended.
        nxt = self.run_script("state.py", "next")
        self.assertNotEqual(nxt["slug"], first["slug"])
        self.solve(nxt["slug"])
        nxt = self.run_script("state.py", "next")
        self.assertEqual(nxt["difficulty"], "easy")      # only 1 unaided so far
        # the remaining hashing easy problem was attempted with hints; next easy must be generated
        self.assertEqual(nxt["action"], "generate")
        medium = self.run_script("state.py", "next", "--topic", "hashing", "--difficulty", "medium")
        rec = self.solve(medium["slug"])
        self.assertEqual(rec["solved_unaided"], 2)
        nxt = self.run_script("state.py", "next")
        self.assertEqual(nxt["difficulty"], "medium")
        rec = self.solve(nxt["slug"])
        self.assertEqual(rec["level"], "comfortable")
        self.assertTrue(rec["level_changed"])

        # Focus is comfortable: move to the weakest topic with prerequisites met.
        moved = self.run_script("state.py", "next")
        self.assertTrue(moved["focus_changed"])
        self.assertNotEqual(moved["topic"], "hashing")
        self.assertEqual(self.run_script("state.py", "profile", "show")["profile"]["focus_topic"], moved["topic"])

        # Failing submission with --gave-up, and a failed record that claims a solve.
        self.run_script("state.py", "start", moved["slug"])
        self.run_script("state.py", "record", moved["slug"], "--passed", "1", "--total", "4",
                        "--outcome", "unaided", expect_ok=False)
        gave = self.run_script("state.py", "record", moved["slug"], "--passed", "1", "--total", "4", "--gave-up")
        self.assertEqual(gave["recorded"]["outcome"], "gave_up")

        attempts = (self.root / "state" / "attempts.jsonl").read_text().strip().splitlines()
        self.assertEqual(len(attempts), 5)
        self.assertTrue(all(json.loads(a)["schema_version"] == 1 for a in attempts))
        rebuilt = self.run_script("state.py", "rebuild")
        self.assertEqual(rebuilt["topics"]["hashing"]["level"], "comfortable")

    def test_hint_ladder_caps(self):
        self.run_script("state.py", "profile", "defaults")
        for level in (1, 2, 3, 4):
            self.assertEqual(self.run_script("state.py", "hint", "floor-sqrt")["level"], level)
        self.assertIsNone(self.run_script("state.py", "hint", "floor-sqrt")["level"])

    def test_defaults_start_at_basics(self):
        self.run_script("state.py", "profile", "defaults")
        out = self.run_script("state.py", "next", "--dry-run")
        self.assertEqual(out["topic"], "arrays-strings")
        self.assertEqual(out["difficulty"], "easy")


class TestExplanation(RepoCopy):
    def test_render(self):
        content = {
            "slug": "pair-with-target",
            "plain_words": "Find two receipts that add up to the target.\n\n- smallest `j` first",
            "intuition": "Remember what you have **seen**.",
            "brute_force": {"idea": "Try every pair.", "time": "O(n^2)", "space": "O(1)"},
            "optimal": {"idea": "Hash map of first positions.", "time": "O(n)", "space": "O(n)"},
            "trace": {"intro": "amounts = [5, 9, 3, 6]", "columns": ["j", "x", "need"],
                      "rows": [[0, 5, 6], [3, 6, 5]]},
            "complexity": {"time": "O(n)", "space": "O(n)", "why": "One pass."},
            "solution": "def find_pair(amounts, target):\n    # remember first positions\n    return []\n",
            "pitfalls": ["Using the same element twice.", "<script>alert(1)</script>"],
        }
        self.run_script("state.py", "profile", "defaults")
        self.run_script("state.py", "start", "pair-with-target")
        out = self.run_script("render_explanation.py", "-", stdin=json.dumps(content))
        self.assertTrue(out.get("attempt_marked_explained"))
        page = (self.root / out["explanation"]).read_text()
        self.assertNotIn("<script>", page)
        self.assertNotIn("{{", page)
        self.assertIn("prefers-color-scheme: dark", page)
        self.assertIn('<span class="tok-kw">def</span>', page)
        self.assertIn("<table>", page)
        rec = self.run_script("state.py", "record", "pair-with-target", "--passed", "11", "--total", "11")
        self.assertEqual(rec["recorded"]["outcome"], "with_hints")


if __name__ == "__main__":
    unittest.main()
