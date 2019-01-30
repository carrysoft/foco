# -*- coding: utf-8 -*-
import time
from openerp.exceptions import Warning
from datetime import datetime, timedelta
from dateutil import relativedelta
from dateutil.tz import gettz
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models,fields,api,_

class EmployeePrint(models.TransientModel):
    _name = 'employee.print'
    
    start_date = fields.Date(
        string = 'Date From',
        required = True,
        default=time.strftime('%Y-%m-01'),
    )
    end_date = fields.Date(
        string = 'Date To',
        required = True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],
    )
    employee_ids = fields.Many2many(
        'hr.employee',
        string = 'Employee(s)',
    )
    
    @api.multi
    def print_attendance(self):
        atten_obj = self.env['hr.attendance']
        attendance_data = {}
        emp_ids = []
        if self.employee_ids:
            for emp in self.employee_ids:
                atten_record = atten_obj.search([('check_in','>=',self.start_date), ('check_out', '<=', self.end_date), ('employee_id', '=',emp.id)],order='check_in')
                for rec in atten_record:
                    from_zone = gettz('UTC')
                    to_zone = gettz(self.env.user.tz)

                   # utc = datetime.utcnow()
                    utc = datetime.strptime(rec.check_in, DEFAULT_SERVER_DATETIME_FORMAT)

                   # Tell the datetime object that it's in UTC time zone since 
                   # datetime objects are 'naive' by default
                    utc = utc.replace(tzinfo=from_zone)

                   # Convert time zone
                    central = utc.astimezone(to_zone)
                    ci = central.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    ci = central.strftime("%d/%m/%Y %H:%M:%S")

                    utc_out = datetime.strptime(rec.check_out, DEFAULT_SERVER_DATETIME_FORMAT)

                   # Tell the datetime object that it's in UTC time zone since 
                   # datetime objects are 'naive' by default
                    utc_out = utc_out.replace(tzinfo=from_zone)

                   # Convert time zone
                    central_out = utc_out.astimezone(to_zone)
                    ci_out = central_out.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    ci_out = central_out.strftime("%d/%m/%Y %H:%M:%S")

                    hour,minute = divmod(rec.worked_hours,1)
                    minute *=60
                    w_hours= '{0:0{width}}'.format(int(hour),width=2)+':{0:0{width}}'.format(int(minute),width=2)

                    # w_hours = '{:,.2f}'.format(rec.worked_hours)

                    if rec.employee_id.id not in attendance_data:
                        emp_ids.append(rec.employee_id.id)
                        #attendance_data[rec.employee_id.id] = [{'check_in' : rec.check_in,'check_out' : rec.check_out, 'sheet' : rec.sheet_id.name, 'name' : rec.employee_id.name}]
                        attendance_data[rec.employee_id.id] = [{'check_in' : ci,'check_out' :ci_out, 'worked_hours': w_hours, 'name' : rec.employee_id.name}]           # odoo 11
                    else:
                        #attendance_data[rec.employee_id.id].append({'check_in' : rec.check_in,'check_out' : rec.check_out, 'sheet' : rec.sheet_id.name, 'name' : rec.employee_id.name})
                        attendance_data[rec.employee_id.id].append({'check_in' : ci,'check_out' : ci_out, 'worked_hours':w_hours, 'name' : rec.employee_id.name})            # odoo 11
                        
            if not attendance_data:
                print ('ttttttttttttttttttttttttttttttttttttttttttttttttttttttt',attendance_data)
                raise Warning(_('No Attendance for this date.'))
            data = self.read()[0]
            data['ids'] = emp_ids
            data['model'] = 'hr.attendance'
            data['attendance_data'] = attendance_data
        else:
            atten_record = atten_obj.search([('check_in','>=',self.start_date), ('check_out', '<=', self.end_date)],order='check_in')
            for rec in atten_record:
                from_zone = gettz('UTC')
                to_zone = gettz(self.env.user.tz)

               # utc = datetime.utcnow()
                utc = datetime.strptime(rec.check_in, DEFAULT_SERVER_DATETIME_FORMAT)

               # Tell the datetime object that it's in UTC time zone since 
               # datetime objects are 'naive' by default
                utc = utc.replace(tzinfo=from_zone)

               # Convert time zone
                central = utc.astimezone(to_zone)
                ci = central.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                ci = central.strftime("%d/%m/%Y %H:%M:%S")

                utc_out = datetime.strptime(rec.check_out, DEFAULT_SERVER_DATETIME_FORMAT)

               # Tell the datetime object that it's in UTC time zone since 
               # datetime objects are 'naive' by default
                utc_out = utc_out.replace(tzinfo=from_zone)

               # Convert time zone
                central_out = utc_out.astimezone(to_zone)
                ci_out = central_out.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                ci_out = central_out.strftime("%d/%m/%Y %H:%M:%S")

                #w_hours = '{:,.2f}'.format(rec.worked_hours)

                hour,minute = divmod(rec.worked_hours,1)
                minute *=60
                w_hours= '{0:0{width}}'.format(int(hour),width=2)+':{0:0{width}}'.format(int(minute),width=2)
                
                if rec.employee_id.id not in attendance_data:
                    emp_ids.append(rec.employee_id.id)
                    #attendance_data[rec.employee_id.id] = [{'check_in' : rec.check_in,'check_out' : rec.check_out, 'sheet' : rec.sheet_id.name, 'name' : rec.employee_id.name}]
                    attendance_data[rec.employee_id.id] = [{'check_in' : ci,'check_out' : ci_out, 'worked_hours': w_hours, 'name' : rec.employee_id.name}]              # odoo 11
                else:
                    #attendance_data[rec.employee_id.id].append({'check_in' : rec.check_in,'check_out' : rec.check_out, 'sheet' : rec.sheet_id.name, 'name' : rec.employee_id.name})
                    attendance_data[rec.employee_id.id].append({'check_in' : ci,'check_out' : ci_out, 'worked_hours': w_hours, 'name' : rec.employee_id.name})               # odoo 11
            if not attendance_data:
                raise Warning(_('No Attendance for this date.'))
            data = self.read()[0]
            data['ids'] = emp_ids
            data['model'] = 'hr.attendance'
            data['attendance_data'] = attendance_data
        #return self.env['report'].get_action(self, 'hr_attendance_print.attendance_template_custom_id',data=data)
        return self.env.ref('hr_attendance_print.hr_attendance_report_custom').report_action(self, data=data, config=False)   # odoo 11

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
         
