"""
* Name:         category_health.py
* Author:       David Strong
* Created:      20 Mar 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* OS:           macOS Monterey Version 12.7.2
* IDE:          PyCharm CE
* Language:     Python
*
* Description:  Manages health status tracking for maintenance categories. Supports setting & retrieving statuses.
* Input:        Category name & health status values for updates.
* Output:       Returns health status values; raises exceptions for invalid operations.
* BigO:         O(1) for get & set operations due to dictionary access.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""


class CategoryHealth:
    """Manages health statuses for different maintenance categories."""

    def __init__(self):
        """Initialize dictionary to keep track of category's health status."""
        self.health_statuses = {}

    def set_health_status(self, category, status):
        """
        Sets health status for given category.

        Args:
            category (str): Name of category.
            status (int): Health status value to set for category.

        Raises:
            ValueError: If status is negative or category is empty.
            TypeError: If category is not string.
        """
        if not isinstance(category, str):
            raise TypeError("Category name must be string.")
        if category == "":
            raise ValueError("Category name cannot be empty.")
        if status < 0:
            raise ValueError("Health status cannot be negative.")
        self.health_statuses[category] = status

    def get_health_status(self, category):
        """
        Retrieves health status for specific category.

        Args:
            category (str): Name of category.

        Returns:
            int or None: Health status of category or None if category doesn't exist.

        Raises:
            TypeError: If category is not string.
        """
        if not isinstance(category, str):
            raise TypeError("Category name must be a string.")
        return self.health_statuses.get(category, None)
