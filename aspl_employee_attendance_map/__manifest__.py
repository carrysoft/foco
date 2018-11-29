# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': 'Odoo Employee Attandance Map',
    'summary': 'Get location of employee and load map using employee attendance location',
    'version': '1.0',
    'description': """Get location of employee and load map using employee attendance location""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'General',
    'website': "http://www.acespritech.com",
    'price': 20,
    'currency': 'EUR',
    'depends': ['base', 'hr_attendance'],
    'data': [
        'views/templates.xml',
        'views/res_config_setting.xml',
        'views/hr_attendance_form_view.xml',            
    ],
    'qweb': [
        'static/src/xml/template.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
