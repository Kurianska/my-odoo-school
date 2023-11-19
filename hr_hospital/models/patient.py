from odoo import models, fields, _, api


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
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', )
    change_doctor_date = fields.Datetime(
        string="Change Date", required=True, default=fields.Datetime.now)
    doctor_change_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.change.history',
        inverse_name='patient_id',
        string='Doctor Change History'
    )
    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='patient_id',
        string='Patient Diagnosis'
    )
    disease_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='patient_id',
        string='Patient Disease'
    )

    incidence_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], help='Level of incidence.')

    color_code = fields.Char(compute='_compute_color_code')

    def write(self, vals):
        res = super().write(vals)
        if 'doctor_id' in vals:
            for record in self:
                self.env['hr.hospital.doctor.change.history'].create({
                    'patient_id': record.id,
                    'doctor_id': vals['doctor_id']
                })
        return res

    def action_view_visits(self):
        action = self.env.ref(
            'hr_hospital.hr_hospital_visit_act_window').read()[0]
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id}
        return action

    def action_view_diagnosis(self):
        action = self.env.ref(
            'hr_hospital.hr_hospital_diagnosis_act_window').read()[0]
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id}
        return action

    def action_view_tests(self):
        action = self.env.ref(
            'hr_hospital.hr_hospital_patient_test_act_window').read()[0]
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id}
        return action

    def action_schedule_appointment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Schedule Appointment'),
            'res_model': 'hr.hospital.doctor.schedule',
            'view_mode': 'form',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
                'form_view_initial_mode': 'edit',
            },
            'target': 'new',
        }

    @api.depends('incidence_level')
    def _compute_color_code(self):
        for record in self:
            if record.incidence_level == 'high':
                record.color_code = 'red'
            elif record.incidence_level == 'medium':
                record.color_code = 'yellow'
            else:
                record.color_code = 'green'
