# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 BroadTech IT Solutions Pvt Ltd 
#    (<http://broadtech-innovations.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
import xlwt
import io
import base64
from xlwt import easyxf
import datetime
from operator import itemgetter

class LeaveSummaryReport(models.TransientModel):
    _name = "leave.summary.report"


    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    leave_summary_file = fields.Binary('Informe Resumen Ausencias')
    file_name = fields.Char('File Name')
    leave_report_printed = fields.Boolean('Leave Report Printed')
    department_id = fields.Many2one('hr.department','Department')


    @api.multi
    def action_print_leave_summary(self):
        workbook = xlwt.Workbook()
        amount_tot = 0
        hr_holiday_objs_list = []
        column_heading_style = easyxf('font:height 200;font:bold True;align: horiz left;')
        worksheet = workbook.add_sheet('Resumen ausencias')
        worksheet.write(2, 2, self.from_date, easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(2, 3, 'a',easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(2, 4, self.to_date,easyxf('font:height 200;font:bold True;align: horiz center;'))
        worksheet.write(4, 0, _('Date'), column_heading_style)
        worksheet.write(4, 1, _('No of Days'), column_heading_style)
        worksheet.write(4, 2, _('Employee'), column_heading_style) 
        worksheet.write(4, 3, _('Department'), column_heading_style)
        worksheet.write(4, 4, _('Leave Type'), column_heading_style)
        worksheet.write(4, 5, _('Description'), column_heading_style)
        worksheet.write(4, 6, _('End Date'), column_heading_style)
        
        worksheet.col(0).width = 3000
        worksheet.col(1).width = 3000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 6500
        worksheet.col(4).width = 5000
        worksheet.col(5).width = 6500
        worksheet.col(6).width = 3000
        
        String = self.from_date + ' ' + ' hasta ' + ' ' + self.to_date
        worksheet2 = workbook.add_sheet('Resumen ausencias por empleado')
        worksheet2.write_merge(2, 2, 0, 1, String, easyxf('font:height 200; align: horiz center;font:bold True;'))
        worksheet2.write(4, 0, _('Employee'), column_heading_style)
        worksheet2.write(4, 1, _('No of Leaves'), column_heading_style)
        worksheet2.col(0).width = 5000
        worksheet2.col(1).width = 5000
        row = 5
        employee_row = 5
        
        
        dict = {}
        for wizard in self:
            employee_leave_data = {}
            heading =  'Resumen ausencias'
            worksheet.write_merge(0, 0, 0, 6, heading, easyxf('font:height 210; align: horiz center;pattern: pattern solid, fore_color black; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            heading =  'Resumen de ausencias por empleado'
            worksheet2.write_merge(0, 0, 0, 1, heading, easyxf('font:height 210; align: horiz center;pattern: pattern solid, fore_color black; font: color white; font:bold True;' "borders: top thin,bottom thin"))
            if wizard.department_id:
                hr_holiday_objs = self.env['hr.holidays'].search([('date_from','>=',wizard.from_date),
                                                               ('date_to','<=',wizard.to_date),
                                                                ('department_id','=',wizard.department_id.id),
                                                                ('state','not in',['draft','cancel','refuse']),
                                                                ('type','=','remove')])
            else:
                hr_holiday_objs = self.env['hr.holidays'].search([('date_from','>=',wizard.from_date),
                                                               ('date_to','<=',wizard.to_date),
                                                               ('state','not in',['draft','cancel','refuse']),('type','=','remove')]) 
            for obj in hr_holiday_objs:
                date_from = datetime.datetime.strptime(obj.date_from,'%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                hr_holiday_objs_list.append({'id':obj,'date':date_from,'emp':obj.employee_id.name})
            hr_holiday_objs_list = sorted(hr_holiday_objs_list, key=itemgetter('emp'))
            hr_holiday_objs_list = sorted(hr_holiday_objs_list, key=itemgetter('date'),reverse=True)
            
            for dict  in hr_holiday_objs_list:
                for id in dict['id']:
                    description = id.name
                    if not description:
                        description = ' '
                    department = id.department_id.name
                    if not department:
                        department = ' '
                    leave_date_from = datetime.datetime.strptime(id.date_from,'%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                    leave_date_to = datetime.datetime.strptime(id.date_to,'%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                    worksheet.write(row, 0, leave_date_from,easyxf('font:height 200;align: horiz left;'))
                    worksheet.write(row, 1, id.number_of_days_temp,easyxf('font:height 200;align: horiz right;'))
                    worksheet.write(row, 2, id.employee_id.name,easyxf('font:height 200;align: horiz left;'))
                    worksheet.write(row, 3, department,easyxf('font:height 200;align: horiz left;'))
                    worksheet.write(row, 4, id.holiday_status_id.name,easyxf('font:height 200;align: horiz left;'))
                    worksheet.write(row, 5, description,easyxf('font:height 200;align: horiz left;'))
                    worksheet.write(row, 6, leave_date_to,easyxf('font:height 200;align: horiz left;'))
                    
                    if id.employee_id.name not in employee_leave_data:
                        employee_leave_data.update({id.employee_id.name: id.number_of_days_temp})
                    else:
                        leave_data = employee_leave_data[id.employee_id.name] + id.number_of_days_temp
                        employee_leave_data.update({id.employee_id.name: leave_data})
                    row += 1
            
            for employee in sorted(employee_leave_data):
                worksheet2.write(employee_row, 0, employee)
                worksheet2.write(employee_row, 1, employee_leave_data[employee])
                employee_row += 1
            
        fp = io.BytesIO()
        workbook.save(fp)
        excel_file = base64.encodestring(fp.getvalue())
        wizard.leave_summary_file = excel_file
        wizard.file_name = 'Informe Resumen Ausencias.xls'
        wizard.leave_report_printed = True
        fp.close()
        return {
                'view_mode': 'form',
                'res_id': wizard.id,
                'res_model': 'leave.summary.report',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'context': self.env.context,
                'target': 'new',
                       }  
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
 # vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
