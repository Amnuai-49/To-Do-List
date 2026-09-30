import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import load_task, update_task


class LoadTaskTests(unittest.TestCase):
	def test_missing_file_returns_empty_list(self):
		with tempfile.TemporaryDirectory() as directory:
			task_file = Path(directory) / "missing.json"
			with patch("main.TASK_FILE", str(task_file)):
				self.assertEqual(load_task(), [])

	def test_invalid_json_returns_empty_list(self):
		with tempfile.TemporaryDirectory() as directory:
			task_file = Path(directory) / "invalid.json"
			task_file.write_text("{invalid", encoding="utf-8")
			with patch("main.TASK_FILE", str(task_file)):
				self.assertEqual(load_task(), [])

	def test_non_list_json_returns_empty_list(self):
		with tempfile.TemporaryDirectory() as directory:
			task_file = Path(directory) / "object.json"
			task_file.write_text(json.dumps({"title": "Task"}), encoding="utf-8")
			with patch("main.TASK_FILE", str(task_file)):
				self.assertEqual(load_task(), [])


class UpdateTaskTests(unittest.TestCase):
	def test_edit_keeps_existing_date_and_time_when_fields_are_blank(self):
		task = {
			"title": "Old title",
			"des": "Old description",
			"date": "2026-09-30",
			"time": "18:30",
			"complete": False,
			"reminded": True,
		}

		updated = update_task(task, "New title", "", "", "", "")

		self.assertTrue(updated)
		self.assertEqual(task["title"], "New title")
		self.assertEqual(task["date"], "2026-09-30")
		self.assertEqual(task["time"], "18:30")
		self.assertTrue(task["reminded"])

	def test_editing_date_resets_reminder(self):
		task = {
			"title": "Task",
			"des": "",
			"date": "2026-09-30",
			"time": "18:30",
			"complete": False,
			"reminded": True,
		}

		updated = update_task(task, "", "", "2026-10-01", "", "")

		self.assertTrue(updated)
		self.assertEqual(task["date"], "2026-10-01")
		self.assertFalse(task["reminded"])

	def test_edit_rejects_invalid_datetime(self):
		task = {"date": "2026-09-30", "time": "18:30", "reminded": True}

		updated = update_task(task, "", "", "not-a-date", "", "")

		self.assertFalse(updated)
		self.assertEqual(task["date"], "2026-09-30")


if __name__ == "__main__":
	unittest.main()
