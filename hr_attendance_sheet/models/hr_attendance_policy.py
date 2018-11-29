# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
import babel
import time
from datetime import datetime, timedelta


class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _name = 'hr.contract'
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    att_policy_id = fields.Many2one('hr.attendance.policy', string='Attendance Policy')


class hr_attendance_policy(models.Model):
    _name = 'hr.attendance.policy'

    name = fields.Char(string="Name",required=True)
    overtime_rule_ids = fields.Many2many(comodel_name="hr.overtime.rule", relation="overtime_rule_policy_rel",
                                         column1="attendance_policy_col", column2="overtime_rule_col",
                                         string="Overtime Rules", )
    late_rule_id = fields.Many2one(comodel_name="hr.late.rule",required=True,
                                   string="Late In Rule")
    absence_rule_id = fields.Many2one(comodel_name="hr.absence.rule",
                                   string="Absence Rule" ,required=True)

    diff_rule_id = fields.Many2one(comodel_name="hr.diff.rule",
                                   string="Difference Time Rule",required=True)






class hr_policy_overtime_line(models.Model):
    _name = 'hr.policy.overtime.line'
    type = [
        ('weekend', 'Week End'),
        ('workday', 'Working Day'),
        ('ph', 'Public Holiday')

    ]

    overtime_rule_id = fields.Many2one(comodel_name='hr.overtime.rule', string='Name', required=True)
    type = fields.Selection(selection=type, string="Type", default='workday')
    active_after = fields.Float(string="Apply after", help="After this time the overtime will be calculated")
    rate = fields.Float(string='Rate')
    attendance_policy_id = fields.Many2one(comodel_name='hr.attendance.policy')

    @api.multi
    @api.onchange('overtime_rule_id')
    def onchange_ov_id(self):
        for line in self:
            line.type = line.overtime_rule_id.type
            line.active_after = line.overtime_rule_id.active_after
            line.rate = line.overtime_rule_id.rate


class hr_overtime_rule(models.Model):
    _name = 'hr.overtime.rule'
    type = [
        ('weekend', 'Week End'),
        ('workday', 'Working Day'),
        ('ph', 'Public Holiday')

    ]


    name = fields.Char(string="name")
    type = fields.Selection(selection=type, string="Type", default='workday')
    active_after = fields.Float(string="Apply after", help="After this time the overtime will be calculated")
    rate = fields.Float(string='Rate')





class hr_late_rule(models.Model):
    _name = 'hr.late.rule'

    name = fields.Char(string='name',required=True)
    line_ids=fields.One2many(comodel_name='hr.late.rule.line',inverse_name='late_id',string='Late In Periods')


class hr_late_rule_line(models.Model):
    _name = 'hr.late.rule.line'
    type = [
        ('fix', 'Fixed'),
        ('rate', 'Rate')
    ]

    late_id = fields.Many2one(comodel_name='hr.late.rule', string='Late Rule')
    type = fields.Selection(string="Type", selection=type, required=True, )
    rate = fields.Float(string='Rate')
    time = fields.Float('Time')
    amount=fields.Float('Amount')


class hr_diff_rule(models.Model):
    _name = 'hr.diff.rule'

    name = fields.Char(string='name', required=True)
    line_ids = fields.One2many(comodel_name='hr.diff.rule.line', inverse_name='diff_id', string='Difference time Periods')


class hr_diff_rule_line(models.Model):
    _name = 'hr.diff.rule.line'
    type = [
        ('fix', 'Fixed'),
        ('rate', 'Rate')
    ]

    diff_id = fields.Many2one(comodel_name='hr.diff.rule', string='Diff Rule')
    type = fields.Selection(string="Type", selection=type, required=True, )
    rate = fields.Float(string='Rate')
    time = fields.Float('Time')
    amount = fields.Float('Amount')






class hr_absence_rule(models.Model):
    _name = 'hr.absence.rule'

    name = fields.Char(string='name', required=True)
    line_ids = fields.One2many(comodel_name='hr.absence.rule.line', inverse_name='absence_id', string='Late In Periods')


class hr_absence_rule_line(models.Model):
    _name = 'hr.absence.rule.line'

    times = [
        ('1', 'First Time'),
        ('2', 'Second Time'),
        ('3', 'Third Time'),
        ('4', 'Fourth Time'),
        ('5', 'Fifth Time'),

    ]

    absence_id = fields.Many2one(comodel_name='hr.absence.rule', string='name')
    rate = fields.Float(string='Rate',required=True)
    # counter = fields.Integer('Times')
    counter = fields.Selection(string="Times", selection=times, required=True, )


