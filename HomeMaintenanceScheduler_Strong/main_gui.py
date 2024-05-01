"""
* Name:         main_gui.py
* Author:       David Strong
* Created:      04 Apr 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* OS:           macOS Monterey Version 12.7.2
* IDE:          PyCharm CE
* Language:     Python
*
* Description:  Implements main graphical user interface for Home Maintenance Scheduler application.
*               Coordinates views like dashboard, calendar, and tasks through central window, managing task, their
*               health statuses, & utilizes predefined tasks & scheduling functionalities.
* Input:        User interactions through GUI.
* Output:       Displays task info & responds to user inputs, updating task statuses & health indicators.
* BigO:         Generally O(n) where n is the # of tasks.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""

import sys
from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QStackedWidget, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from task import Task, AddTaskDialog, save_tasks
from category_health import CategoryHealth
from pre_defined_tasks import PreDefinedTasks
from scheduler import Scheduler
import json

# Global list of categories for tasks
CATEGORIES = [
    'HVAC', 'Plumbing', 'Electrical', 'Appliances', 'Safety Equipment',
    'Exterior', 'Interior', 'Lawn and Garden', 'Pest Control', 'Seasonal'
]


class MainWindow(QMainWindow):
    """
    Initializes main window & its associated views, setting up layout & data interactions.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Maintenance Scheduler")
        self.setGeometry(100, 100, 800, 600)

        # Initialize scheduler
        self.scheduler = Scheduler()

        # Initialize UI components before loading tasks
        self.category_health = CategoryHealth()
        self.predefined_tasks = PreDefinedTasks()
        self.dashboard_view = DashboardWidget(self)
        self.calendar_view = CalendarWidget()
        self.task_view = TaskWidget()
        self.settings_view = SettingsWidget()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.calendar_view)
        self.stacked_widget.addWidget(self.task_view)
        self.stacked_widget.addWidget(self.settings_view)
        self.setCentralWidget(self.stacked_widget)

        # Setup menu & status bar
        self.create_menu_bar()
        self.create_status_bar()

        # Set initial view
        self.stacked_widget.setCurrentWidget(self.dashboard_view)

        # Load tasks after all components are initialized
        self.tasks = self.load_tasks()  # This will use dashboard_view, so it must be initialized first

        # Additional setup as required
        self.dashboard_view.refresh_task_table(self.tasks)
        self.recalculate_health_statuses()

    def load_tasks(self):
        """
        Loads tasks into scheduler, either from JSON file if available, or from predefined data.
        """
        loaded_tasks = self.load_tasks_from_file()
        if not loaded_tasks:  # If no tasks are loaded (i.e., file doesn't exist or is empty)
            # Predefined tasks are loaded only if no existing tasks are found
            task1 = Task("Replace air filters", "2024-07-28", "HVAC", "monthly", priority=1)
            task2 = Task("Check thermostat operation", "2025-04-29", "HVAC", "annually", priority=2)
            loaded_tasks = [task1, task2]

        for task in loaded_tasks:
            self.scheduler.schedule_task(task)
        self.refresh_task_view()
        return loaded_tasks  # Ensures return statement

    @staticmethod
    def load_tasks_from_file():
        """Tries to load tasks from 'tasks.json' file."""
        try:
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                return [Task.from_dict(data) for data in tasks_data]
        except FileNotFoundError:
            return []  # Return empty list if no tasks are stored yet

    def create_menu_bar(self):
        """
        Creates menu bar for application window.
        """
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_status_bar(self):
        """
        Creates status bar for application window.
        """
        status_bar = self.statusBar()
        status_bar.showMessage("Ready")

    def get_predefined_tasks(self):
        """
        Retrieves predefined tasks & converts them into Task objects for scheduler.
        """
        predefined_task_objects = []
        for category in CATEGORIES:
            tasks = PreDefinedTasks.get_tasks_for_category(category)
            for task_info in tasks:
                task_description, frequency = task_info
                task_due_date = self.calculate_due_date_based_on_frequency(frequency)
                predefined_task_objects.append(Task(task_description, task_due_date, category, frequency))
        return predefined_task_objects

    @staticmethod
    def calculate_due_date_based_on_frequency(frequency):
        """
        Calculates due date for task based on frequency.

        :param frequency: str - Frequency of task.
        :return: str - Due date of task formatted as 'YYYY-MM-DD'.
        """
        due_date = datetime.now()
        if frequency == 'weekly':
            due_date += timedelta(weeks=1)
        elif frequency == 'monthly':
            due_date += timedelta(days=30)
        elif frequency == '3 months':
            due_date += timedelta(days=30 * 3)
        elif frequency == '6 months':
            due_date += timedelta(days=30 * 6)
        elif frequency == 'annually':
            due_date = due_date.replace(year=due_date.year + 1)
        elif frequency == '2 years':
            due_date = due_date.replace(year=due_date.year + 2)
        elif frequency == '3 years':
            due_date = due_date.replace(year=due_date.year + 3)
        else:
            raise ValueError(f"Unhandled frequency: {frequency}")

        return due_date.strftime('%Y-%m-%d')

    def handle_new_task(self, task):
        """
        Adds new task to system & updates UI components accordingly.
        """
        if task not in self.tasks:
            self.tasks.append(task)
            self.dashboard_view.refresh_task_table(self.tasks)
            self.recalculate_health_statuses()

    def task_changed(self):
        """
        Handles updates when task properties change, updating health status & refreshing task table.
        """
        print("Task changed signal received")
        self.recalculate_health_statuses()
        # self.dashboard_view.refresh_task_table(self.tasks)

    @staticmethod
    def mark_task_as_complete(task, is_completed):
        """
        Toggles task's completion status & emits signal indicating task updated.
        """
        task.is_completed = is_completed
        task.task_updated.emit()

    def recalculate_health_statuses(self):
        """
        Recalculates health status based on completion state of tasks w/ each category.
        """
        for category in CATEGORIES:
            completed_tasks = sum(1 for task in self.tasks if task.category == category and task.is_completed)
            total_tasks = sum(1 for task in self.tasks if task.category == category)
            health_status = (completed_tasks / total_tasks) * 100 if total_tasks else 0
            self.category_health.set_health_status(category, health_status)
        self.dashboard_view.refresh_health_status(self.category_health.health_statuses)

    def closeEvent(self, event):
        """
        Performs cleanup actions before application window closed.
        Automatically called when window attempts close.
        """
        self.save_state()  # Saves current state before closing
        super().closeEvent(event)

    def save_state(self):
        """
        Saves current state of application to persistent storage.
        Saves all tasks to JSON file.
        """
        if hasattr(self, 'tasks') and self.tasks:  # Check if tasks exist & not empty
            save_tasks(self.tasks)  # Save tasks to JSON file
        else:
            print("No tasks to save or task list not initialized.")

    def refresh_task_view(self):
        """
        Refreshes task view by reloading tasks from scheduler into task table UI component.
        """
        # Clears existing tasks in UI
        self.dashboard_view.task_table.setRowCount(0)

        # Gets all tasks from scheduler in sorted order
        tasks = self.scheduler.get_all_tasks()

        # Iterate through sorted tasks & add them to UI
        for task in tasks:
            self.dashboard_view.add_task_to_table(task)


class DashboardWidget(QWidget):
    """
    DashboardWidget serves as primary interface for user interactions w/ task data. Displays task health,
    task tables, & provides options to add new tasks & view upcoming tasks. Each component w/ widget is
    designed for specific functionality related to task management.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Layout Setup
        # ------------------------------------------------------------
        self.layout = QVBoxLayout(self)

        # Health Status Display
        # ------------------------------------------------------------
        self.health_status_label = QLabel("Health Status")
        self.layout.addWidget(self.health_status_label)

        self.health_layout = QVBoxLayout()
        self.layout.addLayout(self.health_layout)

        # Task Table Configuration
        # ------------------------------------------------------------
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)  # Including Priority column
        self.task_table.setHorizontalHeaderLabels(["Priority", "Description", "Due Date", "Category", "Completed"])
        self.layout.addWidget(self.task_table)

        # Task Addition & Management
        # ------------------------------------------------------------
        self.add_task_button = QPushButton("Add New Task")
        self.add_task_button.clicked.connect(self.open_add_task_dialog)
        self.layout.addWidget(self.add_task_button)

        self.upcoming_tasks_label = QLabel("Upcoming Tasks")
        self.layout.addWidget(self.upcoming_tasks_label)

        # Dialog for Adding New Tasks
        # ------------------------------------------------------------
        self.dialog = None

    def refresh_health_status(self, health_statuses):
        """
        Updates display of health statuses for each category based on completion rate of associated tasks.
        """
        while self.health_layout.count():
            child = self.health_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for category, status in health_statuses.items():
            label = QLabel(f"{category}: {status}%")
            self.health_layout.addWidget(label)

    def refresh_task_table(self, tasks):
        """
        Refreshes task table w/ updated task data, ensuring table reflects current task priorities & statuses.
        """
        print("Starting to refresh task table...")
        self.task_table.setRowCount(0)
        for task in sorted(tasks, key=lambda t: t.priority):
            self.add_task_to_table(task)
        print("Resizing rows...")
        self.task_table.resizeRowsToContents()
        print("Finished refreshing task table.")

    def add_task_to_table(self, task):
        """
        Adds single task row to task table, including interactive components like checkboxes for task completion.
        """
        row_position = self.task_table.rowCount()
        self.task_table.insertRow(row_position)

        self.task_table.setItem(row_position, 0, QTableWidgetItem(str(task.priority)))
        self.task_table.setItem(row_position, 1, QTableWidgetItem(task.description))
        self.task_table.setItem(row_position, 2, QTableWidgetItem(task.due_date))
        self.task_table.setItem(row_position, 3, QTableWidgetItem(task.category))

        complete_checkbox = QCheckBox()
        complete_checkbox.setChecked(task.is_completed)
        complete_checkbox.stateChanged.connect(
            lambda state, t=task: self.main_window.mark_task_as_complete(t, state))
        self.task_table.setCellWidget(row_position, 4, complete_checkbox)

        task.task_updated.connect(self.main_window.task_changed)

    def open_add_task_dialog(self):
        """
        Opens dialog for users to input details for new task.
        """
        if not self.dialog or not self.dialog.isVisible():
            self.dialog = AddTaskDialog(CATEGORIES)
            self.dialog.task_added.connect(self.main_window.handle_new_task,
                                           Qt.UniqueConnection)  # Ensures unique connection to prevent multiple slots
            self.dialog.show()

    def display_predefined_tasks(self, category, tasks):
        """
        Displays list of predefined tasks in task table, each associated w/ specific category.
        """
        for task_description, frequency in tasks:
            due_date = "Due Date based on frequency"  # Placeholder, needs calculated
            new_task = Task(task_description, due_date, category, frequency)
            self.add_task_to_table(new_task)


# Placeholder widgets for Calendar, Tasks, Settings
class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Calendar View")
        layout.addWidget(label)
        self.setLayout(layout)


class TaskWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Task View")
        layout.addWidget(label)
        self.setLayout(layout)


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Settings View")
        layout.addWidget(label)
        self.setLayout(layout)


# Main function to run application
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
