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


from odoo import fields, models, api, _, exceptions
from odoo.http import request
from datetime import datetime
import logging, requests, platform
import httpagentparser
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'    

    google_api_key = fields.Char(string='Google API KEY')
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(google_api_key=self.env['ir.config_parameter'].sudo().get_param('aspl_employee_attendance_map.google_api_key'))
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('aspl_employee_attendance_map.google_api_key', self.google_api_key)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    location_name = fields.Char(string="Location Name")
    latitude = fields.Char(string="latitude")
    longitude = fields.Char(string="Logitude")
    os_name = fields.Char(string="Operationg System")
    browser_name = fields.Char(string="Browser")
    location_name_out = fields.Char(string="Ubicacion salida")
    latitude_out = fields.Char(string="latitud salida")
    longitude_out = fields.Char(string="Logitud salida")


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def attendance_manual(self, next_action, entered_pin=None, latitude=None,longitude=None):
        return self.attendance_action(next_action, entered_pin, latitude,longitude)

    @api.multi
    def attendance_action(self, next_action, entered_pin=None, latitude=None,longitude=None):
        self.ensure_one()
        action_message = self.env.ref('hr_attendance.hr_attendance_action_greeting_message').read()[0]
        action_message['previous_attendance_change_date'] = self.last_attendance_id and (
                    self.last_attendance_id.check_out or self.last_attendance_id.check_in) or False
        action_message['employee_name'] = self.name
        action_message['next_action'] = next_action
        if self.user_id:
            modified_attendance = self.sudo(self.user_id.id).attendance_action_change(latitude, longitude)
        else:
            modified_attendance = self.sudo().attendance_action_change(latitude, longitude)
        action_message['attendance'] = modified_attendance.read()[0]
        return {'action': action_message}

    @api.multi
    def attendance_action_change(self, latitude=None,longitude=None):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        if len(self) > 1:
            raise exceptions.UserError(_('Cannot perform check in or check out on multiple employees.'))
        action_date = fields.Datetime.now()
        agent = request.httprequest.environ.get('HTTP_USER_AGENT')
        agent_details = httpagentparser.detect(agent)
        user_os = agent_details['os']['name']
        browser_name = agent_details['browser']['name']
        bit_type = platform.architecture()
        key = self.env['ir.config_parameter'].sudo().get_param('aspl_employee_attendance_map.google_api_key')
        api_response = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s' % (latitude, longitude, key))
        api_response_dict = api_response.json()
        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date
            }
            if latitude and longitude:
                if api_response_dict['status'] == 'OK':
                    vals.update({
                        'longitude': longitude,
                        'latitude': latitude,
                        'os_name': user_os + ", " + bit_type[0],
                        'browser_name': browser_name,
                        'location_name': api_response_dict['results'][0]['formatted_address'],
                    })
                return self.env['hr.attendance'].create(vals)   
            else:
                return self.env['hr.attendance'].create(vals)
        else:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)],limit=1)
            if attendance:
                attendance.check_out = action_date
                if latitude and longitude:
                   if api_response_dict['status'] == 'OK':
                      vals.update({
                        'longitude_out': longitude,
                        'latitude_out': latitude,
                        'location_name_out': api_response_dict['results'][0]['formatted_address'],
                    })
            else:
                raise exceptions.UserError(('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                      'Your attendances have probably been modified manually by human resources.') % {
                        'empl_name': self.name, })
            return attendance


class EmployeeAttendanceMap(models.Model):
    _name = 'employee.attendance.map'

    employee_ids = fields.Many2many('hr.employee', string="Employees")
    attendance_date = fields.Date(string="Date", required=True)
    department_id = fields.Many2one('hr.department', string="Department")
    job_position = fields.Many2one('hr.job', string="Job Position")

    @api.multi
    def show_map(self):
        try:
            response = requests.get("http://www.google.com")
            check_connection = True
        except requests.ConnectionError:
            check_connection = False
        attendance_obj = self.env['hr.attendance']
        result = []
        result.append({'connection': check_connection})

        domain = []
        if self.employee_ids:
            domain += [('id', 'in', self.employee_ids.ids)]
        if self.department_id:
            domain += [('department_id', '=', self.department_id.id)]
        if self.job_position:
            domain += [('job_id', '=', self.job_position.id)]
        employee_ids = self.env['hr.employee'].search(domain)
        emp_detail = attendance_obj.search([('employee_id', 'in', employee_ids.ids)])
        for each_emp in emp_detail:
            emp_date = datetime.strptime(each_emp.check_in, '%Y-%m-%d %H:%M:%S')
            select_date = datetime.strptime(self.attendance_date, '%Y-%m-%d')
            new_emp_date = datetime.date(emp_date)
            new_select_date = datetime.date(select_date)
            if new_emp_date == new_select_date:
                result.append({'latitude': each_emp.latitude,
                               'longitude': each_emp.longitude,
                               'os_name': each_emp.os_name,
                               'name': each_emp.employee_id.name,
                               'emp_id': each_emp.employee_id.id,
                               'image': each_emp.employee_id.image,
                               'date': self.attendance_date,
                               'dept_id': self.department_id.id,
                               'job_position': self.job_position.id
                               })
            else:
                continue
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
