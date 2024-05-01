"""
* Name:         test_user.py
* Author:       David Strong
* Created:      03 Apr 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* Description:  Contains unit tests for the User class in the Home Maintenance Scheduler application,
*               ensuring that the class correctly handles task management for users.
* Input:        None directly; the tests programmatically create User instances and interact with them.
* Output:       Assertions that confirm the expected behavior of the User class's methods.
* BigO:         O(n) for methods that search through the task list.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""

import unittest
from datetime import datetime, timedelta
from user import User
from task import Task


class TestUser(unittest.TestCase):
    """
    Unit tests for the User class, focusing on task management.
    """
    def setUp(self):
        """
        Prepares a User object and sample Task objects for testing.
        """
        self.user = User("John Doe")
        self.task1 = Task("Fix leaky faucet", datetime.now() + timedelta(days=1), "Plumbing", "annually")
        self.task2 = Task("Replace air filters", datetime.now() + timedelta(days=30), "HVAC", "monthly")
        self.task3 = Task("Check smoke detectors", datetime.now() + timedelta(days=90), "Safety", "annually")

    def test_add_task(self):
        """
        Verifies that a task can be added to the user's task list.
        """
        self.user.add_task(self.task1)
        self.assertIn(self.task1, self.user.tasks)

    def test_remove_task(self):
        """
        Tests the removal of a task from the user's task list, verifying correct list management.
        """
        self.user.add_task(self.task1)
        self.user.remove_task(self.task1)
        self.assertNotIn(self.task1, self.user.tasks)

    def test_get_task_list(self):
        """
        Ensures that getting the task list returns all tasks currently managed by the user.
        """
        self.user.add_task(self.task1)
        self.user.add_task(self.task2)
        task_list = self.user.get_task_list()
        self.assertIn(self.task1, task_list)
        self.assertIn(self.task2, task_list)
        self.assertEqual(len(task_list), 2)

    def test_find_task_by_description(self):
        """
        Confirms that tasks can be found by description and returns the correct task.
        """
        self.user.add_task(self.task1)
        self.user.add_task(self.task2)
        result = self.user.find_task_by_description("Replace air filters")
        self.assertEqual(result, self.task2)
        self.assertIsNone(self.user.find_task_by_description("Non-existing task"))

    def test_user_initialization(self):
        """
        Confirms that the User object is initialized correctly with its attributes.
        """
        self.assertEqual(self.user.name, "John Doe")
        self.assertIsInstance(self.user.tasks, list)
        self.assertEqual(len(self.user.tasks), 0)


if __name__ == '__main__':
    unittest.main()
