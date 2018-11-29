# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class AttendanceRecapReportWizard(models.TransientModel):
    _name = 'attendance.recap.report.wizard1'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

    user_id = fields.Many2one('res.users', string='User')

    @api.multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'user_id': self.user_id[0],
                'display_name': self.user_id[0].display_name,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('carry.recap_report').report_action(self, data=data)


class ReportAttendanceRecap(models.AbstractModel):
    """Abstract Model for report template.

    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.carry.attendance_recap_report_view1'

    @api.model
    def get_report_values(self, docids, data=None):
        date_start = datetime.strptime(data['form']['date_start'], DATE_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATE_FORMAT) + timedelta(days=1)
        date_diff = (date_end - date_start).days
        empleado_id = data['form']['user_id']

        docs = []

# - Codigo nuevo
        attendances = self.env['hr.attendance'].search([
            ('check_in', '>=', date_start.strftime(DATETIME_FORMAT)),
            ('check_in', '<=', date_end.strftime(DATETIME_FORMAT)),
            ],order='check_in')

        for attendance in attendances:
            ent=attendance.check_in.strftime(DATETIME_FORMAT)
            docs.append({
                'employee': attendance.display_name,
                'entrada': ent,
                'salida': self.env["res.lang"].datetime_formatter(attendance.check_out),
                'horas_dia': '{:5.2f}'.format(attendance.worked_hours),
            })

# - Fin codigo nuevo


#        employees = self.env['hr.employee'].search([], order='name asc')
#        for employee in employees:
#            presence_count = self.env['hr.attendance'].search_count([
#                ('employee_id', '=', employee.id),
#                ('check_in', '>=', date_start.strftime(DATETIME_FORMAT)),
#                ('check_out', '<', date_end.strftime(DATETIME_FORMAT)),
#            ])
#
#            absence_count = date_diff - presence_count
#
#            docs.append({
#                'employee': employee.name,
#                'presence': presence_count,
#                'absence': absence_count,
#            })
#
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start.strftime(DATE_FORMAT),
            'date_end': (date_end - timedelta(days=1)).strftime(DATE_FORMAT),
            'docs': docs,
        }
