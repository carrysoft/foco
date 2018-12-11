# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, models


class HrLeaveMassRefuse(models.TransientModel):
    _name = 'hr.leave.mass.refuse'

    @api.multi
    def refuse_mass_leave(self):
        context = self._context
        leave_ids = context.get('active_ids')
        for holiday_record in self.env['hr.holidays'].browse(leave_ids):
            holiday_record.write({'state': 'refuse'})
        return {'type': 'ir.actions.act_window_close'}
