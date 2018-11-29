# -*- coding: utf-8 -*-
{
    'name': "hr_attendance_report",

    'summary': """
        Informe de Entradas/Salidas de empleados""",

    'description': """
        Informe de Entradas/Salidas de empleados
    """,

    'author': "Fco Jose Carrion",
    'website': "http://www.carrysoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_attendance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'wizards/carrysoft.xml',
        'reports/carrysoft.xml',
    ],
}
