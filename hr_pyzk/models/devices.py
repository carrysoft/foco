from odoo import models, fields, api, exceptions, _

from addons.hr_pyzk.controllers import controller as c



class Devices(models.Model):


    _name = 'devices'

    name = fields.Char(string='Nombre Dispositivo')
    ip_address = fields.Char(string='Direccióon Ip')
    port = fields.Integer(string='Puerto', default = 4370)
    sequence = fields.Integer(string='Secuencia')
    device_password = fields.Char(string='Password Dispositivo')
    state = fields.Selection([(0, 'Activo'), (1, 'Inactivo')], string='Estado', default=1)
    difference = fields.Float(string='Diferencia horaria con UTC',
                              help = "Por favor, indica las horas de diferencia entre el horario local y horario UTC")

    def test_connection(self):
        with c.ConnectToDevice(self.ip_address, self.port, self.device_password) as conn:
            if conn:
                return {
                    "type": "ir.actions.act_window",
                    "res_model": "devices",
                    "views": [[False, "form"]],
                    "res_id": self.id,
                    "target": "main",
                    "context": {'show_message1': True},
                }

