from odoo import models, fields, api, exceptions, _


class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['person.mixin']

    name = fields.Char(
        string="Doctor Name", index=True, required=True)
    active = fields.Boolean(
        default=True, )

    specialty = fields.Char(required=True)
    is_intern = fields.Boolean(default=False)
    mentor_id = fields.Many2one(comodel_name='hr.hospital.doctor',
                                string="Doctor-mentor",
                                domain="[('is_intern', '=', False)]")
    diagnoses_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='intern_id',
        string="Diagnoses"
    )
    schedules_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.schedule',
        inverse_name='doctor_id',
        string="Schedules"
    )
    patient_ids = fields.Many2many(comodel_name='hr.hospital.patient',
                                   string='Patients')

    @api.constrains('is_intern', 'mentor_id')
    def _check_intern_mentor(self):
        for record in self:
            if record.is_intern and not record.mentor_id:
                raise exceptions.ValidationError(
                    _('An intern should have a mentor.'))
            if not record.is_intern and record.mentor_id:
                raise exceptions.ValidationError(
                    _('Only interns can have mentors.'))

    def open_disease_report_wizard(self):
        return {
            'name': 'Monthly Disease Report',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.hospital.disease.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_show_reschedule_wizard(self):
        self.ensure_one()
        view_id = self.env.ref(
            'hr_hospital.hr_hospital_reschedule_wizard_form').id

        return {
            'name': _('Reschedule Appointment'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.reschedule.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {'default_schedule_id': self.id}
        }

    def action_show_schedule_week_wizard(self):
        self.ensure_one()
        view_id = self.env.ref(
            'hr_hospital.doctor_schedule_week_wizard_form').id

        return {
            'name': _('Set Doctor Weekly Schedule'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.doctor.schedule.week.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {'default_doctor_id': self.id}
        }
