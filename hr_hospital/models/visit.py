from odoo import models, fields


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Patient Visit'

    name = fields.Char()
    active = fields.Boolean(
        default=True, )
    visit_date = fields.Datetime(string="Visit Date")
