"""
* Name:         test_category_health.py
* Author:       David Strong
* Created:      03 Apr 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* OS:           macOS Monterey Version 12.7.2
* IDE:          PyCharm CE
* Language:     Python
*
* Description:  Tests for CategoryHealth class, ensuring proper management & querying health statuses.
* Input:        None.
* Output:       Success or failure messages based on test results.
* BigO:         O(1) for health status assignment & retrieval.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
*                   modified or unmodified. I have not given other fellow student(s) access to my program.
"""


import unittest
from category_health import CategoryHealth


class TestCategoryHealth(unittest.TestCase):
    """Unit tests for the CategoryHealth class."""

    def setUp(self):
        """Prepare resources for each test; create a CategoryHealth instance."""
        self.category_health = CategoryHealth()

    def test_initial_health_status(self):
        """Check initial health status for a new category is None."""
        self.assertIsNone(self.category_health.get_health_status('HVAC'))

    def test_health_status_assignment(self):
        """Ensure that health status can be set and retrieved correctly."""
        self.category_health.set_health_status('Plumbing', 75)
        self.assertEqual(self.category_health.get_health_status('Plumbing'), 75)

    def test_update_health_status(self):
        """Verify that health status can be updated and the new value is retrieved."""
        self.category_health.set_health_status('Electrical', 80)
        self.category_health.set_health_status('Electrical', 90)
        self.assertEqual(self.category_health.get_health_status('Electrical'), 90)

    def test_set_get_health_status_non_existing_category(self):
        """
        Test setting and retrieving the health status for a category that does not initially exist in the system.
        This test ensures that the CategoryHealth class can handle new categories dynamically by adding them
        with their respective health statuses, and then correctly returning the status when queried.
        """
        self.category_health.set_health_status('Non-Existing', 50)
        status = self.category_health.get_health_status('Non-Existing')
        self.assertEqual(status, 50, "Should be able to set and get health status for any category, even new ones.")

    def test_nonexistent_category_status(self):
        """Ensure that querying a non-existent category returns None."""
        self.assertIsNone(self.category_health.get_health_status('NonExistent'))

    def test_set_negative_health_status(self):
        """Check that setting a negative health status raises a ValueError."""
        with self.assertRaises(ValueError):
            self.category_health.set_health_status('HVAC', -10)

    def test_empty_category(self):
        """Test that an empty category name raises a ValueError."""
        with self.assertRaises(ValueError):
            self.category_health.set_health_status('', 30)

    def test_non_string_category(self):
        """Ensure non-string category names raise a TypeError."""
        with self.assertRaises(TypeError):
            self.category_health.set_health_status(123, 50)

    def test_null_status_assignment(self):
        """Check setting a health status to None raises a TypeError."""
        with self.assertRaises(TypeError):
            self.category_health.set_health_status('HVAC', None)

    def test_multiple_categories(self):
        """Stress test: setting and retrieving statuses for multiple categories."""
        categories = [f"Category{i}" for i in range(100)]
        for i, category in enumerate(categories):
            self.category_health.set_health_status(category, i * 10)
        for i, category in enumerate(categories):
            self.assertEqual(self.category_health.get_health_status(category), i * 10)


if __name__ == '__main__':
    unittest.main()
