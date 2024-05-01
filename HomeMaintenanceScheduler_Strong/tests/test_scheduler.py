"""
* Name:     	test_scheduler.py
* Author:   	David Strong
* Created:  	03 Apr 2024
* Course:   	CIS 152 - Data Structure
* Version:  	1.0
*
* OS:       	macOS Monterey Version 12.7.2
* IDE:      	PyCharm CE
* Language: 	Python
*
* Description:	Tests Scheduler class's ability to manage, sort, & retrieve tasks based on priority & due date.
* Input:        None directly
* Output:       Success or failure messages based on test results.
* BigO:         O(n log n) for sorting operations where n is the # of tasks.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""

import unittest
from scheduler import Scheduler
from task import Task
from datetime import datetime


class TestScheduler(unittest.TestCase):
    """
    Unit tests for Scheduler class, focusing on task scheduling, & retrieval.
    """

    def setUp(self):
        """
        Prepares test fixtures before each test method.
        """
        self.scheduler = Scheduler()
        self.task1 = Task("Task 1", datetime.now().strftime('%Y-%m-%d'), "Category A", "monthly", priority=2)
        self.task2 = Task("Task 2", datetime.now().strftime('%Y-%m-%d'), "Category B", "monthly", priority=1)
        self.task3 = Task("Task 3", datetime.now().strftime('%Y-%m-%d'), "Category C", "monthly", priority=3)

    def test_schedule_task(self):
        """
        Test ability of scheduler to add tasks & retrieve next task based on highest priority.
        """
        self.scheduler.schedule_task(self.task1)
        self.scheduler.schedule_task(self.task2)
        next_task = self.scheduler.get_next_task()
        self.assertEqual(next_task, self.task2, "Task w/ highest priority should be returned first")

    def test_get_all_tasks(self):
        """
        Test tasks are returned in priority order from scheduler.
        """
        self.scheduler.schedule_task(self.task1)
        self.scheduler.schedule_task(self.task2)
        self.scheduler.schedule_task(self.task3)
        tasks = self.scheduler.get_all_tasks()
        self.assertEqual([task.priority for task in tasks], [1, 2, 3], "Tasks should be returned in priority order")

    def test_reschedule_task(self):
        """
        Test rescheduling task & verify that tasks remains in priority order.
        """
        self.scheduler.schedule_task(self.task1)
        self.scheduler.schedule_task(self.task2)
        self.scheduler.schedule_task(self.task3)
        # Remove a task before rescheduling
        self.scheduler.remove_task(self.task2)
        self.scheduler.schedule_task(self.task2)
        rescheduled_tasks = self.scheduler.get_all_tasks()
        self.assertEqual([task.priority for task in rescheduled_tasks], [1, 2, 3], "Rescheduled tasks maintain order")

    def test_remove_task(self):
        """
        Test removing task & ensuring it's no longer in list.
        """
        self.scheduler.schedule_task(self.task1)
        self.scheduler.schedule_task(self.task2)
        self.scheduler.remove_task(self.task1)
        tasks = self.scheduler.get_all_tasks()
        self.assertNotIn(self.task1, tasks, "Removed task shouldn't be in list")

    def test_task_completed(self):
        """
        Test marking task as completed & ensuring it reflects in task properties.
        """
        self.scheduler.schedule_task(self.task1)
        self.scheduler.task_completed(self.task1)
        self.assertTrue(self.task1.is_completed, "Task should be marked as completed")


if __name__ == '__main__':
    unittest.main()
