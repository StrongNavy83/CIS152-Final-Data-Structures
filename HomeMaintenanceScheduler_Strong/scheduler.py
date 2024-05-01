"""
* Name:         scheduler.py
* Author:       David Strong
* Created:      09 Apr 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* OS:           macOS Monterey Version 12.7.2
* IDE:          PyCharm CE
* Language:     Python
*
* Description:  Manages schedule of tasks, allowing for adding, sorting, & retrieving based on priority & due date.
* Input:        Tasks to be scheduled w/ attributes including description, due date, category, frequency, & priority.
* Output:       Operations on tasks such as scheduling & retrieval don't produce output directly but affect scheduler.
* BigO:         O(n log n) for sorting, O(1) for task retrieval.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
                    modified or unmodified. I have not given other fellow student(s) access to my program.
"""


class Scheduler:
    """
    Maintains list of tasks, providing functionality to add, sort, & retrieve them based on priority & due date.
    """
    def __init__(self):
        """
        Initializes empty list to store scheduled tasks.
        """
        self.tasks = []

    def _sort_tasks(self):
        """
        Method to sort tasks by priority & due date. Called internally after operation that may change task order.
        """
        self.tasks.sort(key=lambda x: (x.priority, x.due_date))

    def schedule_task(self, task):
        """
        Adds task to scheduler & sorts tasks to maintain order.
        :param task: Task - Task to be added to scheduler.
        """
        self.tasks.append(task)
        self._sort_tasks()

    def get_next_task(self):
        """
        Retrieves next task from scheduler based on highest priority & earliest due date.
        :return: Task - Task w/ highest priority & earliest due date.
        """
        return self.tasks[0] if self.tasks else None

    def remove_task(self, task):
        """
        Removes specified task from list & re-sorts list to maintain order.
        :param task: Task - Task to be removed from scheduler.
        """
        self.tasks.remove(task)
        self._sort_tasks()

    def get_all_tasks(self):
        """
        Retrieves all tasks from scheduler, sorted by priority & due date.
        :return: list of Task - Sorted by priority & due date.
        """
        return self.tasks

    def task_completed(self, task):
        """
        Marks task completed & resorts list to reflect any priority changes.
        :param task: Task - Task to be marked completed.
        """
        task.is_completed = True
        self._sort_tasks()
