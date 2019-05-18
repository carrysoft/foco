# Copyright 2017 Comunitea Servicios Tecnológicos S.L.
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):

    _inherit = "hr.employee"
    _sql_constraints = [(
        'rfid_card_code_uniq',
        'UNIQUE(rfid_card_code)',
        'The rfid code should be unique.'
    )]

    rfid_card_code = fields.Char("RFID Card Code")

    @api.model
    def register_attendance(self, card_code, time, lugar):
        """ Register the attendance of the employee.
        :returns: dictionary
            'rfid_card_code': char
            'employee_name': char
            'employee_id': int
            'error_message': char
            'logged': boolean
            'action': check_in/check_out
        """

        res = {
            'rfid_card_code': card_code,
            'time': time,
            'lugar': lugar,
            'employee_name': '',
            'employee_id': False,
            'error_message': '',
            'logged': False,
            'action': 'FALSE',
        }
        print ('busco tarjeta')
        print (card_code)
        employee = self.search([('rfid_card_code', '=', card_code)], limit=1)
        if employee:
            res['employee_name'] = employee.name
            res['employee_id'] = employee.id
        else:
            msg = _("No employee found with card %s") % card_code
            _logger.warning(msg)
            res['error_message'] = msg
            return res
        try:
            attendance = employee.attendance_action_change_time(time,lugar)
            if attendance:
                msg = _('Attendance recorded for employee %s') % employee.name
                _logger.debug(msg)
                res['logged'] = True
                if attendance.check_out:
                    res['action'] = 'check_out'
                else:
                    res['action'] = 'check_in'
                return res
            else:
                msg = _('No attendance was recorded for '
                        'employee %s') % employee.name
                _logger.error(msg)
                res['error_message'] = msg
                return res
        except Exception as e:
            res['error_message'] = e
            _logger.error(e)
        return res

    @api.multi
    def attendance_action_change_time(self,time,lugar):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        if len(self) > 1:
            raise exceptions.UserError(_('Cannot perform check in or check out on multiple employees.'))
        action_date = time

        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
                'location_name': lugar,
            }
            return self.env['hr.attendance'].create(vals)
        else:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
            if attendance:
                attendance.check_out = action_date
                attendance.location_name_out = lugar
            else:
                raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                    'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.name, })
            return attendance
