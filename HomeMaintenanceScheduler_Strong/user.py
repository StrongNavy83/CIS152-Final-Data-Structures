"""
* Name:         user.py
* Author:       David Strong
* Created:      19 Mar 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* Description:  Represents user of Home Maintenance Scheduler application. Handles task management including
*               adding, removing, & querying tasks associated w/ user.
* Input:        User info including name & tasks to manage.
* Output:       User object capable of managing collection of tasks.
* BigO:         O(n) for operations that involve searching through list of tasks.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""


class User:
    """
    Represents user w/ name & a collection of tasks, providing methods to manage tasks.
    """
    def __init__(self, name):
        """
        Initializes new User object w/ name & an empty list of tasks.

        :param name: str - Name of user.
        """
        self.name = name
        self.tasks = []

    def add_task(self, task):
        """
        Adds task to user's list of tasks.

        :param task: Task - Task object to be added to user's tasks.
        """
        self.tasks.append(task)

    def remove_task(self, task):
        """
        Removes specified task from user's task list.

        :param task: Task - Task object to be removed from user's tasks.
        """
        if task in self.tasks:
            self.tasks.remove(task)

    def get_task_list(self):
        """
        Returns list of all tasks associated w/ user.

        :return: list of Task - List of tasks associated w/ user.
        """
        return self.tasks

    def find_task_by_description(self, description):
        """
        Finds & returns first task w/ given description.

        :param description: str - Description of task to find.
        :return: Task or None - Task w/ matching description, or None if no match found.
        """
        for task in self.tasks:
            if task.description == description:
                return task
        return None
