from odoo import models, fields


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = 'Wizard to mass reassign doctor'

    current_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Current Doctor', required=True)
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor', required=True)

    def action_mass_reassign_doctor(self):
        patient = self.env['hr.hospital.patient']
        patients = patient.search([(
            'doctor_id', '=', self.current_doctor_id.id)])
        patients.write({'doctor_id': self.new_doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
