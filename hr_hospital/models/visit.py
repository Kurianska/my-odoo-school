from odoo import models, fields, exceptions, _


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Patient Visit'

    active = fields.Boolean(
        default=True, )
    visit_date = fields.Datetime(required=True)
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor')
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient')
    diagnosis_id = fields.Many2one(
        comodel_name='hr.hospital.diagnosis',
        string='Diagnosis')

    def write(self, vals):

        if set(vals).intersection({'visit_date', 'doctor_id'}):
            for record in self:
                if (record.visit_date and record.visit_date
                        <= fields.Datetime.now()):
                    raise exceptions.UserError(
                        _('You cannot change the date, time, '
                          'or doctor for a visit that has already occurred'))
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.diagnosis_id:
                raise exceptions.UserError(
                    _('You cannot delete visits with diagnoses'))
        return super().unlink()

    def toggle_active(self):
        for record in self:
            if record.diagnosis_id:
                raise exceptions.UserError(
                    _('You cannot archive visits with diagnoses'))
        return super().toggle_active()
