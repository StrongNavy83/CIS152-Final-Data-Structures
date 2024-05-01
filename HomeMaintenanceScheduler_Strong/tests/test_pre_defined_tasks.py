
"""
* Name:         test_pre_defined_tasks.py
* Author:       David Strong
* Created:      09 Apr 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* OS:           macOS Monterey Version 12.7.2
* IDE:          PyCharm CE
* Language:     Python
*
* Description:  Tests retrieval & handling of predefined tasks from PreDefinedTasks class.
* Input:        None.
* Output:       Success or failure messages based on test results.
* BigO:         O(1) for direct retrievals, O(n) where n is the # of predefined tasks.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""

import unittest
from pre_defined_tasks import PreDefinedTasks


class TestPreDefinedTasks(unittest.TestCase):
    """
    Unit tests for PreDefinedTasks class.
    """

    def test_get_tasks_for_existing_category(self):
        """
        Test retrieving tasks for an existing category returns non-empty list & checks type.
        """
        tasks = PreDefinedTasks.get_tasks_for_category('HVAC')
        self.assertTrue(tasks, "Should retrieve tasks for 'HVAC' category.")
        self.assertIsInstance(tasks, list, "Expected tasks to be returned as a list.")

    def test_get_tasks_for_non_existing_category(self):
        """
        Test retrieving tasks for non-existing category returns an empty list.
        """
        tasks = PreDefinedTasks.get_tasks_for_category('Non-Existing')
        self.assertEqual(tasks, [], "Should return an empty list for non-existing categories.")


if __name__ == '__main__':
    unittest.main()
