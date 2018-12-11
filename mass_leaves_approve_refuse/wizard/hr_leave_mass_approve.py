# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, models


class HrLeaveMassApprove(models.TransientModel):
    _name = 'hr.leave.mass.approve'

    @api.multi
    def approve_mass_leave(self):
        context = self._context
        leave_ids = context.get('active_ids')
        for holiday_record in self.env['hr.holidays'].browse(leave_ids):
            holiday_record.write({'state': 'validate'})
        return {'type': 'ir.actions.act_window_close'}
