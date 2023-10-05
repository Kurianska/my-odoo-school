from odoo import models, fields


class Patient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char()
    active = fields.Boolean(
        default=True, )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease', )
