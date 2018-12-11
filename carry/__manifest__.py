# -*- coding: utf-8 -*-
{
    'name': "carry",

    'summary': """
        Custom Report Example""",

    'description': """
        Custom report for practice purpose
    """,

    'author': "Fco Jose Carrio",
    'website': "https://www.carrysoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_attendance'],

    # always loaded
    'data': [
        'wizards/recap.xml',
        'reports/recap.xml',
    ],
}
