# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    "name": "HR Leave Mass Approve/Refuse ",
    "version": "11.0.1.0.0",
    "license" : 'AGPL-3',
    "depends": ["hr_holidays"],
    "author": 'Serpent Consulting Services Pvt. Ltd.',
    "website": 'http://www.serpentcs.com',
    "category": "Human Resources",
    "description": """
        This module provide a wizard on leaves so that one can \n
        select multiple leaves at a time and approve all leaves together.
        Mass leave approval, Leaves Approve rejection in bulk,
        Bulk leave approve reject
    """,
    "summary": """
        This module provide a wizard on leaves so that one can \n
        select multiple leaves at a time and approve all leaves together.
        Mass leave approval, Leaves Approve rejection in bulk,
        Bulk leave approve reject
    """,
    'data': [
           'wizard/hr_leave_mass_approve_view.xml',
           'wizard/hr_leave_mass_refuse_view.xml',
           ],
    'installable': True,
    'auto_install': False,
    'price': 5,
    'currency': 'EUR',
}
