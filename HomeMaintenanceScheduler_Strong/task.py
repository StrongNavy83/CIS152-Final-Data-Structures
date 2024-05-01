"""
* Name:         task.py
* Author:       David Strong
* Created:      20 Mar 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* OS:           macOS Monterey Version 12.7.2
* IDE:          PyCharm CE
* Language:     Python
*
* Description:  Defines Task class to model maintenance tasks w/ comprehensive attributes & signal mechanisms
*               for property changes, & AddTaskDialog class for GUI-based task creation. Includes methods to
*               serialize tasks to JSON format & back to Task instances.
* Input:        Attributes for creating task instance & user inputs from GUI for task creation.
* Output:       Emits signals for property changes in Task class, creates tasks from user input in AddTaskDialog,
*               & supports saving to & loading from JSON format.
* BigO:         O(1) for task attribute manipulations & signal emissions, O(n) for saving/loading tasks.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""

import json
from datetime import timedelta, datetime
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QMessageBox, QSpinBox
from PySide6.QtCore import Signal, QObject, QDate


class Task(QObject):
    """
    Represents maintenance task w/ attributes such as description, due date, frequency, category, & priority.
    #Emits signals to notify other components when task attributes change.
    """
    task_updated = Signal()
    priority_changed = Signal(int)  # Signal for priority changes w/ new priority as argument

    def __init__(self, description, due_date, category, frequency, priority=3, is_completed=False):
        super().__init__()
        self.description = description
        self.due_date = due_date
        self.category = category
        self.frequency = frequency
        self.priority = self._validate_priority(priority)
        self.is_completed = is_completed  # Now explicitly accepting 'is_completed' in constructor

    @staticmethod
    def _validate_priority(priority):
        return priority if priority in [1, 2, 3] else 3

    def set_priority(self, new_priority):
        if new_priority != self.priority:
            self.priority = self._validate_priority(new_priority)
            self.priority_changed.emit(new_priority)
            self.task_updated.emit()

    def complete_task(self):
        """
        Marks task as completed, calculates next due date based on task's frequency, & emits task_updated signal.
        """
        next_due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
        # Calculate next due date based on frequency
        adjustment = {
            'weekly': timedelta(weeks=1),
            'monthly': timedelta(days=30),
            'annually': timedelta(days=365)
        }.get(self.frequency, timedelta(days=365))  # Default to annually if frequency is unrecognized
        self.due_date = (next_due_date + adjustment).strftime('%Y-%m-%d')
        self.is_completed = True
        self.task_updated.emit()

    def reset_task(self):
        """
        Resets task's completion status w/o changing due date, & emits task_updated signal.
        """
        self.is_completed = False
        self.task_updated.emit()

    def to_dict(self):
        return {
            'description': self.description,
            'due_date': self.due_date,
            'category': self.category,
            'frequency': self.frequency,
            'priority': self.priority,
            'is_completed': self.is_completed
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates instance of Task from dictionary of attributes.
        """
        # Using .get for 'is_completed' to provide default value of False if it's not present in data.
        return cls(
            description=data['description'],
            due_date=data['due_date'],
            category=data['category'],
            frequency=data['frequency'],
            priority=data['priority'],
            is_completed=data.get('is_completed', False)
        )


class AddTaskDialog(QDialog):
    """
    Dialog for adding new tasks through GUI interface, allowing users to specify task details.
    """
    task_added = Signal(Task)

    def __init__(self, categories):
        super().__init__()
        self.setWindowTitle('Add New Task')
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel('Description:'))
        self.description_input = QLineEdit()
        layout.addWidget(self.description_input)

        layout.addWidget(QLabel('Due Date:'))
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.due_date_input)

        layout.addWidget(QLabel('Category:'))
        self.category_input = QComboBox()
        self.category_input.addItems(categories)
        layout.addWidget(self.category_input)

        layout.addWidget(QLabel('Frequency:'))
        self.frequency_input = QLineEdit()
        layout.addWidget(self.frequency_input)

        layout.addWidget(QLabel('Priority:'))
        self.priority_input = QSpinBox()
        self.priority_input.setRange(1, 3)
        layout.addWidget(self.priority_input)

        add_button = QPushButton('Add Task')
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

    def add_task(self):
        """
        Gathers user input from dialog, validates it, & emits task_added signal w/ new Task instance if valid.
        """
        description = self.description_input.text()
        due_date = self.due_date_input.date().toString('yyyy-MM-dd')
        category = self.category_input.currentText()
        frequency = self.frequency_input.text()
        priority = self.priority_input.value()

        if not description.strip():
            QMessageBox.warning(self, 'Validation Error', 'Please enter all required fields.')
            return

        task = Task(description, due_date, category, frequency, priority)
        self.task_added.emit(task)
        QMessageBox.information(self, "Task Added", "A new task has been successfully added.")
        self.accept()


def save_tasks(tasks, filename='tasks.json'):
    """
    Saves list of Task objects to JSON file.

    Serializes Task objects using their `to_dict` method & writes them to file.
    If file doesn't exist, one created.

    :param tasks: list of Task - Tasks to be saved.
    :param filename: str - Filename to save tasks, defaults 'tasks.json'.
    """
    with open(filename, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)


def load_tasks(filename='tasks.json'):
    """
    Loads tasks from JSON file & returns them as list of Task objects.

    Attempts read JSON file specified & convert back into list of Task objects using 'from_dict' class method of Task.
    If file doesn't exist, returns empty list.

    :param filename: str - Filename from load tasks, defaults 'tasks.json'.
    :return: list of Task - List of deserialized Task objects.
    """
    try:
        with open(filename, 'r') as file:
            tasks_data = json.load(file)
            return [Task.from_dict(data) for data in tasks_data]
    except FileNotFoundError:
        return []  # Return  empty list if no tasks stored.
