# Copyright 2017 Odoo S.A.
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import fields, models


class HrAttendanceReason(models.Model):
    _name = "hr.attendance.reason"
    _description = "Motivo modificación"

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'El codigo debe ser unico')
    ]

    name = fields.Char(
        String='Motivo',
        help='Indique motivo por el que se va pronto o llega tarde',
        required=True, index=True)
    code = fields.Char('Codigo Motivo')
    action_type = fields.Selection(
        [('sign_in', 'Entrada'),
         ('sign_out', 'Salida')],
        string="Tipo de Accion", help="Dejar vacio si es independiente")
