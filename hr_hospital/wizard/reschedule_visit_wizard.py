from odoo import models, fields


class HospitalRescheduleWizard(models.TransientModel):
    _name = 'hr.hospital.reschedule.wizard'
    _description = 'Hospital Reschedule Wizard'

    schedule_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.schedule',
        string="Schedule"
    )
    new_date = fields.Date()
    new_time = fields.Char()
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="New Doctor"
    )

    def action_reschedule(self):
        self.ensure_one()
        self.schedule_id.unlink()
        self.env['hr.hospital.doctor.schedule'].create({
            'doctor_id':
                self.new_doctor_id.id or self.schedule_id.doctor_id.id,
            'appointment_date':
                self.new_date or self.schedule_id.appointment_date,
            'appointment_time':
                self.new_time or self.schedule_id.appointment_time,
        })

        return {'type': 'ir.actions.act_window_close'}
