from odoo import models, fields, api, exceptions, _


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Hospital Patient Diagnosis'

    name = fields.Char(
        string='Patient Diagnosis',
        index=True, required=True)

    active = fields.Boolean(
        default=True, )
    diagnosis_date = fields.Date(required=True)
    doctor_id = fields.Many2one(comodel_name='hr.hospital.doctor',
                                string='Treatment doctor', required=True)
    patient_id = fields.Many2one(comodel_name='hr.hospital.patient',
                                 string='Patient', required=True)
    disease_id = fields.Many2one(comodel_name='hr.hospital.disease',
                                 string='Disease', required=True)
    treatment_note = fields.Text()
    mentor_comment = fields.Text(required=True)
    intern_id = fields.Many2one(comodel_name='hr.hospital.doctor',
                                string="Intern",
                                domain="[('is_intern', '=', True)]",
                                )

    @api.constrains('intern_id', 'mentor_comment')
    def _check_mentor_comments(self):
        for record in self:
            if record.intern_id and not record.mentor_comment:
                raise exceptions.ValidationError(
                    _("Mentor's comment is required for "
                      "the diagnosis made by the intern."))
