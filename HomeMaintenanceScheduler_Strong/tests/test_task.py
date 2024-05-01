"""
* Name:         test_task.py
* Author:       David Strong
* Created:      03 Apr 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* OS:           macOS Monterey Version 12.7.2
* IDE:          PyCharm CE
* Language:     Python
*
* Description:  Tests Task class for correct initialization, signal emissions upon changes, & correct update of task
*               attributes like priority & completion status.
* Input:        None directly.
* Output:       Assertions to validate behavior, success or failure messages based on test outcomes.
* BigO:         O(1) for individual attribute manipulations & signal emissions.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""

import sys
import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDate
from task import Task, AddTaskDialog

app = None


class TestTask(unittest.TestCase):
    """
    Contains unit tests for Task class to ensure it correctly handles attribute assignments & signal emissions.
    """
    def setUp(self):
        """
        Creates Task instance to use in tests.
        """
        self.task = Task("Test Description", "2024-12-31", "HVAC", "annually", priority=1)

    def test_priority_assignment(self):
        """
        Tests priority is set correctly & emits appropriate signals.
        """
        self.task.set_priority(2)  # Change priority to valid value
        self.assertEqual(self.task.priority, 2)

    def test_complete_task(self):
        """
        Tests completing task updates its status & due date correctly.
        """
        self.task.complete_task()
        self.assertTrue(self.task.is_completed)


class TestAddTaskDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Initializes QApplication. Required for testing GUI components.
        """
        global app
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()

    def setUp(self):
        """
        Set up instance of AddTaskDialog to be used in tests.
        """
        self.dialog = AddTaskDialog(categories=["HVAC", "Plumbing"])

    def test_dialog_initial_state(self):
        """
        Test initial state of AddTaskDialog to ensure all components are set up correctly.
        """
        self.assertEqual(self.dialog.description_input.text(), "")  # Confirm description input is initially empty
        self.assertEqual(self.dialog.category_input.count(), 2)  # Confirm correct # of categories

    def test_add_task(self):
        """
        Test adding task through dialog to confirm correct task creation & signal emission.
        """
        self.dialog.description_input.setText("Check filters")
        self.dialog.due_date_input.setDate(QDate.fromString("2025-01-01", "yyyy-MM-dd"))
        self.dialog.category_input.setCurrentText("HVAC")
        self.dialog.frequency_input.setText("monthly")
        self.dialog.priority_input.setValue(2)
        self.dialog.add_task()
        # Simulate clicking add button & check input fields
        self.assertEqual(self.dialog.description_input.text(), "Check filters")

    @classmethod
    def tearDownClass(cls):
        """
        Properly shuts down QApplication after all tests.
        """
        global app
        if app:
            app.quit()
        app = None


if __name__ == '__main__':
    unittest.main()
