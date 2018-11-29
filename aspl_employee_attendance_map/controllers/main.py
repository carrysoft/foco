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
import json
from datetime import datetime
from odoo import http
from odoo.http import request


class WebsiteSale(http.Controller):

    @http.route(['/employee_attendance'], type='http', auth="public")
    def employee_attendance(self, **post):
        lst = []
        filter_domain = "[('id','in',"
        emp_attendance = request.env['hr.attendance'].search([('employee_id', '=', int(post['employee_id']))])
        
        for each_emp in emp_attendance:
            emp_date = datetime.strptime(each_emp.check_in, '%Y-%m-%d %H:%M:%S')
            select_date = datetime.strptime(post['date'], '%Y-%m-%d')
            new_emp_date = datetime.date(emp_date)
            new_select_date = datetime.date(select_date)
            if new_emp_date == new_select_date:
                if each_emp:
                    lst.append(each_emp.id)
                else:
                    filter_domain = ""
        filter_domain += "[" + ','.join(map(str, lst)) + "]"
        filter_domain += ")]"
        return json.dumps({'filter_domain': filter_domain})

    @http.route(['/get_api_key'], type='http', auth="public")
    def get_api_key(self, **post):
        return json.dumps({'key':request.env['ir.config_parameter'].sudo().get_param('aspl_employee_attendance_map.google_api_key') or False})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:          