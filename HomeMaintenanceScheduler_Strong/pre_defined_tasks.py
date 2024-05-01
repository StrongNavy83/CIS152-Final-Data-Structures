"""
* Name:         pre_defined_tasks.py
* Author:       David Strong
* Created:      04 Apr 2024
* Course:       CIS 152 - Data Structure
* Version:      1.0
*
* OS:           macOS Monterey Version 12.7.2
* IDE:          PyCharm CE
* Language:     Python
*
* Description:  Defines class that holds predefined tasks & their frequencies for various maintenance categories.
                Assists in planning & scheduling routine maintenance tasks efficiently.
* Input:        Category name to retrieve tasks for that category.
* Output:       Lists of tasks & their frequencies for specified categories.
* BigO:         O(1) for task retrieval due to direct dictionary access.
*
* Academic Honesty: I attest that this is my original work. I have not used unauthorized source code, either
                    modified or unmodified. I have not given other fellow student(s) access to my program.
"""


class PreDefinedTasks:
    """
    Allows quick retrieval & aids in maintaining consistent schedules for property maintenance.
    """

    TASKS_WITH_FREQUENCIES = {
        'HVAC': [
            ('Replace air filters', '3 months'),
            ('Check thermostat operation', 'annually'),
            ('Clean evaporator and condenser coils', 'annually'),
            ('Inspect for duct leakage', '2 years'),
            ('Flush condensate drain', 'annually'),
        ],
        'Plumbing': [
            ('Inspect faucets for leaks', 'annually'),
            ('Inspect toilets for leaks and efficiency', 'annually'),
            ('Drain and flush the water heater', 'annually'),
            ('Inspect pipes for signs of leaks or corrosion', 'annually'),
            ('Winterize outdoor faucets', 'annually'),
        ],
        'Electrical': [
            ('Test smoke and carbon monoxide detectors', 'monthly'),
            ('Inspect and test GFC outlets', '6 months'),
            ('Test and dust light fixtures', 'annually'),
            ('Ensure proper wattage in all fixtures', 'annually'),
            ('Tighten any loose outlets or switch covers', 'annually'),
        ],
        'Appliances': [
            ('Clean refrigerator coils', '6 months'),
            ('Clean and inspect the dryer vent', 'annually'),
            ('Clean dishwasher and check for leaks', '6 months'),
            ('Clean oven and check gasket seals', 'annually'),
            ('Clean and deodorize garbage disposal', '6 months'),
        ],
        'Safety Equipment': [
            ('Inspect fire extinguishers for expiration and pressure', 'annually'),
            ('Replace batteries in smoke and carbon monoxide detectors', 'annually'),
            ('Check and restock emergency preparedness kits', 'annually'),
            ('Inspect window locks and door deadbolts', 'annually'),
            ('Check the operation of all emergency egress windows', 'annually'),
        ],
        'Exterior': [
            ('Clean gutters and downspouts', 'annually'),
            ('Inspect the roof for damage', 'annually'),
            ('Seal cracks and gaps in windows and doors', 'annually'),
            ('Check the siding for damage or rot', 'annually'),
            ('Trim trees and shrubs away from the house', 'annually'),
        ],
        'Interior': [
            ('Fix or lubricate squeaky doors', 'annually'),
            ('Caulk around showers and tubs', '3 years'),
            ('Inspect and clean window tracks', 'annually'),
            ('Inspect and tighten hardware and fixtures', 'annually'),
            ('Lubricate garage door springs', 'annually'),
        ],
        'Lawn and Garden': [
            ('Spring Aerate lawn', 'annually'),
            ('Spring Prune trees and shrubs', 'annually'),
            ('Spring Fertilize lawn', 'annually'),
            ('Spring Mulch garden beds', 'annually'),
            ('Spring Inspect and repair sprinkler system', 'annually'),
        ],
        'Pest Control': [
            ('Inspect for termites', 'annually'),
            ('Seal potential pest entry points', 'annually'),
            ('Treat for ants and roaches as needed', 'annually'),
            ('Check attic and basement for signs of pests', 'annually'),
            ('Remove standing water to deter mosquitoes', 'weekly'),
        ],
        'Seasonal': [
            ('Fall Check weather stripping and insulation', 'annually'),
            ('Spring Prepare for extreme weather conditions', 'annually'),
            ('Fall Service heating system', 'annually'),
            ('Spring Service cooling system', 'annually'),
            ('Fall Cover or store outdoor furniture', 'annually'),
        ],
    }

    @classmethod
    def get_tasks_for_category(cls, category):
        """
        Retrieves tasks list & their frequencies & category.

        :param category: str - Category for which tasks are being requested.
        :return: list of tuples - Each tuple contains task description & frequency.
        """
        return cls.TASKS_WITH_FREQUENCIES.get(category, [])
