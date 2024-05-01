"""
* Name:         test_gui.py
* Author:       David Strong
* Created:      09 Apr 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* Description:  Unit tests for main graphical user interface of the Home Maintenance Scheduler application.
*
* Input:        Simulated user interactions & predefined task setups.
* Output:       Assertions to check correctness of GUI behavior & state management.
* BigO:         Generally O(n) for operations involving task manipulations.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""

import sys
import unittest
import logging
from PySide6.QtWidgets import QApplication
from main_gui import MainWindow
from task import Task


class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Starts application for test."""
        cls.app = QApplication(sys.argv)

    def setUp(self):
        """Initialize MainWindow for each test & ensures clean scheduler."""
        self.window = MainWindow()
        self.window.scheduler.tasks.clear()  # Clears tasks for clean slate.

        self.window.load_tasks()  # Reloads predefined tasks.
        self.initial_task_count = len(self.window.scheduler.tasks)  # Stores initial count for use in tests.

    def test_initial_task_loading(self):
        """Test that tasks are loaded into scheduler upon initialization."""
        self.assertGreater(len(self.window.scheduler.tasks), 0, "Scheduler should have tasks loaded on startup.")

    def test_task_display(self):
        """Test that tasks are displayed in task table."""
        self.assertGreater(self.window.dashboard_view.task_table.rowCount(), 0, "Task table should display tasks.")

    def test_add_new_task(self):
        """Test adding new task & verifying in scheduler."""
        logging.debug(f"Initial task count: {self.initial_task_count}")
        new_task = Task("Test Task", "2025-01-01", "HVAC", "annually", priority=1)
        self.window.handle_new_task(new_task)
        self.window.dashboard_view.refresh_task_table(self.window.tasks)
        expected_task_count = self.initial_task_count + 1
        actual_task_count = len(self.window.scheduler.tasks)
        # Check if the new task is displayed correctly
        displayed_description = self.window.dashboard_view.task_table.item(
            self.window.dashboard_view.task_table.rowCount() - 1, 1).text()

    def tearDown(self):
        """Close main window after test."""
        self.window.close()

    @classmethod
    def tearDownClass(cls):
        """Clean up Qt application after all tests done."""
        cls.app.exit()


if __name__ == "__main__":
    unittest.main()
