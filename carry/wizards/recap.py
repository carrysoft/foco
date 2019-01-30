# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from dateutil import relativedelta
from dateutil.tz import gettz

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class AttendanceRecapReportWizard1(models.TransientModel):
    _name = 'attendance.recap.report.wizard1'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

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
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        # return self.env.ref('carry.recap_report').report_action(self, data=data)
        return self.env.ref('carry.recap_report1').report_action(self, data=data)


class ReportAttendanceRecap1(models.AbstractModel):
    """Abstract Model for report template.

    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.carry.attendance_recap_report_view1'

    @api.model
    def get_report_values(self, docids, data=None):
        from_zone = gettz('UTC')
        to_zone = gettz(self.env.user.tz)
        date_start = datetime.strptime(data['form']['date_start'], DEFAULT_SERVER_DATE_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DEFAULT_SERVER_DATE_FORMAT) + timedelta(days=1)
        date_diff = (date_end - date_start).days
        d_start = date_start.strftime("%d/%m/%Y")
        d_end = date_end.strftime("%d/%m/%Y")

        docs = []

        attendances = self.env['hr.attendance'].search([
            ('check_in', '>=', date_start.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
            ('check_in', '<=', date_end.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
            ],order='check_in')

        for attendance in attendances:
            utc = datetime.strptime(attendance.check_in, DEFAULT_SERVER_DATETIME_FORMAT)
            utc = utc.replace(tzinfo=from_zone)
            central = utc.astimezone(to_zone)
            ci = central.strftime("%d/%m/%Y %H:%M")
            try:
                utc = datetime.strptime(attendance.check_out, DEFAULT_SERVER_DATETIME_FORMAT)
                utc = utc.replace(tzinfo=from_zone)
                central = utc.astimezone(to_zone)
                co = central.strftime("%d/%m/%Y %H:%M")
            except:
                co=''

            hour,minute = divmod(attendance.worked_hours,1)
            minute *=60
            w_hours = '{0:0{width}}'.format(int(hour),width=2)+':{0:0{width}}'.format(int(minute),width=2)
            nombre='Nombre: {n} DNI: {id}: Departemento: {d}'.format (n=attendance.employee_id.name,id=attendance.employee_id.identification_id,d=attendance.employee_id.department_id.name)

            docs.append({
                'employee': nombre,
                'entrada': ci,
                'salida': co,
                'horas_dia': w_hours,
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': d_start,
#            'date_start': date_start.strftime(DEFAULT_SERVER_DATE_FORMAT),
            'date_end': d_end,
#            'date_end': (date_end - timedelta(days=1)).strftime(DEFAULT_SERVER_DATE_FORMAT),
            'docs': docs,
        }
