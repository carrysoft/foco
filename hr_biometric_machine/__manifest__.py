# -*- coding: utf-8 -*-
{
    'name': "Biometric Machine ",

    'summary': """
       Registro de EMpleados, integracion con lector de huella""",

    'description': """
Integracion Lector Huellas
=============================

This application enables you to integrate the fingerprint machine at you organization with Odoo.
Downloads the logs of each employee from the fingerprint machine with their details.
    """,

    'author': "Pravitha V / Fco. Jose Carrion",
    'website': "http://www.qpr.qa/",
    'category': 'Human Resources Custom',
    'version': '0.1',

    'depends': ['base_setup', 'hr', 'hr_attendance',],


    'data': [
        # 'security/ir.model.access.csv',
        'views/biometric_machine_view.xml',
        'report/daily_attendance_view.xml',
        'schedule.xml',
        'wizard/schedule_wizard.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
    
}
