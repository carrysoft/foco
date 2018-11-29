# -*- coding: utf-8 -*-

from odoo import models,fields,api

class AttendanceRander(models.AbstractModel):
    _name='report.hr_attendance_print.attendance_template_custom_id'
    
    @api.model
    #def render_html(self,docids, data=None):
    def get_report_values(self, docids, data=None):                    # odoo 11
        attendance_ids = data['ids']
        report = self.env['ir.actions.report']._get_report_from_name('hr_attendance_print.attendance_template_custom_id')
        #docargs = {
        return {                             # odoo 11
            'doc_ids': attendance_ids,
            'doc_model': 'hr.attendance',
            'docs': self.env['hr.employee'].browse(attendance_ids),
            'data':data,
        }
        #return self.env['report'].render('hr_attendance_print.attendance_template_custom_id', docargs)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

