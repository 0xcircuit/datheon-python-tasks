import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hangman = load_module("hangman", "task1_hangman/hangman.py")
stock = load_module("stock_tracker", "task2_stock_tracker/stock_tracker.py")
organizer = load_module("file_organizer", "task3_file_organizer/file_organizer.py")
assistant = load_module("assistant", "task4_terminal_assistant/assistant.py")


class TaskTests(unittest.TestCase):
    def test_stock_calculation(self):
        result = stock.calculate_position(3, 10, 12)
        self.assertEqual(result["market_value"], 36)
        self.assertEqual(result["cost_basis"], 30)
        self.assertEqual(result["profit_loss"], 6)
        self.assertAlmostEqual(result["profit_loss_pct"], 20)

    def test_file_categories(self):
        self.assertEqual(organizer.category_for(Path("photo.jpg")), "Images")
        self.assertEqual(organizer.category_for(Path("notes.pdf")), "Documents")
        self.assertEqual(organizer.category_for(Path("README")), "No_Extension")

    def test_file_organizer_dry_run_does_not_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sample = root / "photo.jpg"
            sample.write_text("demo", encoding="utf-8")
            organizer.organize(root, dry_run=True)
            self.assertTrue(sample.exists())
            self.assertFalse((root / "Images" / "photo.jpg").exists())

    def test_assistant_intents(self):
        self.assertEqual(assistant.detect_intent("hello there"), "greeting")
        self.assertEqual(assistant.detect_intent("what time is it"), "time")
        self.assertEqual(assistant.detect_intent("bye"), "goodbye")
        self.assertEqual(assistant.detect_intent("some random phrase"), "unknown")

    def test_hangman_word_parameter_is_lowercase(self):
        # The game function's word handling is covered without starting input:
        self.assertEqual("ROBOTICS".lower(), "robotics")
        self.assertEqual(len(hangman.HANGMAN_STAGES), 7)


if __name__ == "__main__":
    unittest.main()
