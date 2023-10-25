from odoo import models, fields, api


class ReassignDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.reassign.doctor.wizard'
    _description = 'Wizard to reassign doctor'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor', required=True)
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patients')

    @api.model
    def action_open_wizard(self):
        return {
            'name': 'Reassign Doctor',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.hospital.reassign.doctor.wizard',
            'target': 'new',
        }

    def action_reassign_doctor(self):
        for record in self:
            record.patient_ids.write({'doctor_id': record.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
