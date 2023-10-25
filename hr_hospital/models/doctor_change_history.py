from odoo import models, fields


class DoctorChangeHistory(models.Model):
    _name = 'hr.hospital.doctor.change.history'
    _description = 'Doctor Change History'

    name = fields.Char(
        string="Doctor Change History", index=True)
    active = fields.Boolean(
        default=True, )
    change_doctor_date = fields.Datetime(
        required=True,
        default=lambda self: fields.Datetime.now()
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient', required=True
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor', required=True)
