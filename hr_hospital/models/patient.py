from odoo import models, fields


class Patient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['person.mixin']

    name = fields.Char(
        string="Patient Name", index=True, required=True)
    active = fields.Boolean(
        default=True, )
    birthday_date = fields.Char(
        string='Patient Birthday Date', required=True)
    passport_data = fields.Char(
        string='Patient Passport Data', required=True)
    age = fields.Integer(required=True)
    contact_person = fields.Char()
    address = fields.Char()
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', )
    change_doctor_date = fields.Datetime(
        string="Change Date", required=True, default=fields.Datetime.now)
    doctor_change_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.change.history',
        inverse_name='patient_id',
        string='Doctor Change History'
    )

    def write(self, vals):
        res = super().write(vals)
        if 'doctor_id' in vals:
            for record in self:
                self.env['hr.hospital.doctor.change.history'].create({
                    'patient_id': record.id,
                    'doctor_id': vals['doctor_id']
                })
        return res
