# -*- coding: utf-8 -*-

##############################################################################
#
#    Clear Groups for Odoo
#    Copyright (C) 2016 Bytebrand GmbH (<http://www.bytebrand.net>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime, timedelta
import pytz

from odoo import fields, models, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _
from odoo.exceptions import UserError


class ImportLeaveRequests(models.TransientModel):
    _name = 'import.leave.requests'
    _description = 'Import Leave Requests With Employee Tag'
    leave_dates = fields.Binary('Select *.csv',
                                required=True,
                                help="Select csv file having "
                                     "holiday dates.")
    leave_type_id = fields.Many2one('hr.holidays.status',
                                    'Leave Type',
                                    required=True)
    employee_tag_id = fields.Many2one('hr.employee.category',
                                      "Employee Tag", required=True)

    def convert_to_user_timezone(self, user_tz, dt):
        input_tz = pytz.timezone(user_tz)
        converted_date = input_tz.localize(dt, is_dst=False)
        converted_date = converted_date.astimezone(pytz.UTC).strftime(
            DEFAULT_SERVER_DATETIME_FORMAT)
        return converted_date

    @api.multi
    def import_leave_data(self):
        holiday_obj = self.env['hr.holidays']
        employee_obj = self.env['hr.employee']
        timesheet_obj = self.env['hr_timesheet_sheet.sheet']
        converter = self.env['ir.fields.converter']
        for data in self:
            leaves = (data.leave_dates.decode('base64')).split('\n')
            category_id = data.employee_tag_id.id
            employees = employee_obj.search(
                [('category_ids', 'in', [category_id])])
            for employee in employees:
                for leave in leaves[:-1]:
                    dt_fmt, tm_fmt = \
                        (timesheet_obj._get_user_datetime_format())
                    try:
                        datetime.strptime(leave, dt_fmt)
                    except ValueError:
                        raise UserError(_(
                            "Date format in your .csv file does not "
                            "match with database date format."))
                    dt1 = datetime.strptime(leave, dt_fmt)
                    dt2 = (datetime.strptime(leave, dt_fmt) +
                           timedelta(hours=23,
                                     minutes=59,
                                     seconds=59))
                    user_tz = employee.user_id and employee.user_id.tz or 'utc'
                    leave_date = self.convert_to_user_timezone(user_tz, dt1)
                    leave_date_to = self.convert_to_user_timezone(user_tz, dt2)
                    holiday_id = holiday_obj.create({
                        'name': data.leave_type_id.name,
                        'date_from': leave_date,
                        'date_to': leave_date_to,
                        'holiday_status_id': data.leave_type_id.id,
                        'employee_id': employee.id,
                        'number_of_days_temp': 1.0,
                        'type': 'remove'})
                    holiday_obj.holidays_validate([holiday_id])
        return True

        # END
