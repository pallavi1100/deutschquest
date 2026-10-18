import ast
import pathlib
import unittest
from bonus_lessons import EXTRA_MISSIONS, PHRASES

class GameContentTests(unittest.TestCase):
    def test_quantity(self):
        self.assertEqual(len(EXTRA_MISSIONS), 10)
        self.assertEqual(sum(len(m["questions"]) for m in EXTRA_MISSIONS), 80)
        self.assertGreaterEqual(len(PHRASES), 12)
    def test_unique_missions(self):
        ids = [m["id"] for m in EXTRA_MISSIONS]
        self.assertEqual(len(set(ids)), len(ids))
    def test_question_data(self):
        for mission in EXTRA_MISSIONS:
            self.assertEqual(len(mission["questions"]), 8)
            for q in mission["questions"]:
                self.assertTrue(q.get("prompt"))
                self.assertTrue(q.get("grammar"))
                self.assertTrue(q.get("example"))
                mode = q["mode"]
                self.assertIn(mode, {"choice","listen","type","order"})
                if mode in {"choice","listen"}:
                    self.assertGreaterEqual(len(q["options"]), 3)
                    self.assertLess(q["answer"], len(q["options"]))
                    self.assertGreaterEqual(q["answer"], 0)
                if mode == "listen": self.assertTrue(q.get("listen_text"))
                if mode in {"type","order"}: self.assertTrue(q.get("answer_text"))
                if mode == "order":
                    self.assertEqual(' '.join(q['tokens']), q['answer_text'])
    def test_python_parses(self):
        base = pathlib.Path(__file__).parent
        for name in ['app.py','bonus_lessons.py']:
            ast.parse((base/name).read_text())

if __name__ == '__main__': unittest.main()
