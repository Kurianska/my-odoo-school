from odoo import models, fields


class DoctorScheduleWeekWizard(models.TransientModel):
    _name = 'hr.hospital.doctor.schedule.week.wizard'
    _description = 'Doctor Weekly Schedule Wizard'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor",
        required=True,
    )
    week_type = fields.Selection(
        selection=[('even', 'Even Week'), ('odd', 'Odd Week')],
        required=True,
    )
    monday_time = fields.Char(string="Monday")
    tuesday_time = fields.Char(string="Tuesday")
    wednesday_time = fields.Char(string="Wednesday")
    thursday_time = fields.Char(string="Thursday")
    friday_time = fields.Char(string="Friday")
    saturday_time = fields.Char(string="Saturday")
    sunday_time = fields.Char(string="Sunday")

    def action_set_schedule_week(self):

        doctor_schedule = self.env['hr.hospital.doctor.schedule']

        days_mapping = {
            'monday': 'monday_time',
            'tuesday': 'tuesday_time',
            'wednesday': 'wednesday_time',
            'thursday': 'thursday_time',
            'friday': 'friday_time',
            'saturday': 'saturday_time',
            'sunday': 'sunday_time',
        }

        for day, field_name in days_mapping.items():
            time_value = getattr(self, field_name)

            if time_value:
                existing_schedule = doctor_schedule.search([
                    ('doctor_id', '=', self.doctor_id.id),
                    ('week_type', '=', self.week_type),
                    ('day', '=', day)
                ])

                if existing_schedule:
                    existing_schedule.write({'appointment_time': time_value})
                else:
                    doctor_schedule.create({
                        'doctor_id': self.doctor_id.id,
                        'week_type': self.week_type,
                        'day': day,
                        'appointment_time': time_value,
                    })
