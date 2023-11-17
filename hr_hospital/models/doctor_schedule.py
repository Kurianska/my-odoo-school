import re
from odoo import models, fields, api, exceptions, _


class DoctorSchedule(models.Model):
    _name = 'hr.hospital.doctor.schedule'
    _description = 'Hospital Doctor Schedule'

    active = fields.Boolean(
        default=True, )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor",
        required=True,
        ondelete='cascade'
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient', required=True)
    appointment_date = fields.Date(required=True)
    appointment_time = fields.Char(required=True)
    day_of_week = fields.Selection(
        selection=[('monday', 'Monday'),
                   ('tuesday', 'Tuesday'),
                   ('wednesday', 'Wednesday'),
                   ('thursday', 'Thursday'),
                   ('friday', 'Friday'),
                   ('saturday', 'Saturday'),
                   ('sunday', 'Sunday')
                   ], string='Day of the Week',
        compute='_compute_day_of_week',
        store=True)

    week_type = fields.Selection([
        ('even', 'Even Week'),
        ('odd', 'Odd Week'),
        ('all', 'Every Week')
    ], default='all',
        required=True)

    @api.constrains('doctor_id', 'appointment_date', 'appointment_time')
    def _check_unique_appointment(self):
        for record in self:
            domain = [
                ('doctor_id', '=', record.doctor_id.id),
                ('appointment_date', '=', record.appointment_date),
                ('appointment_time', '=', record.appointment_time)
            ]
            existing_appointments = self.search(domain)
            if len(existing_appointments) > 1:
                raise exceptions.ValidationError(
                    _('The appointment time is already booked for '
                      'this doctor on the selected date.'))

    @api.constrains('appointment_time')
    def _check_appointment_time_format(self):
        pattern = re.compile(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
        for record in self:
            if not pattern.match(record.appointment_time):
                raise exceptions.ValidationError(
                    _('Appointment Time should be in HH:MM format.'))

        @api.constrains('doctor_id', 'appointment_date',
                        'appointment_time', 'week_type')
        def _check_unique_appointment(self):
            for record in self:
                domain = [
                    ('doctor_id', '=', record.doctor_id.id),
                    ('appointment_date', '=', record.appointment_date),
                    ('appointment_time', '=', record.appointment_time),
                    ('week_type', '=', record.week_type)
                ]
                existing_appointments = self.search(domain)
                if len(existing_appointments) > 1:
                    raise exceptions.ValidationError(
                        _('The appointment time is already booked for'
                          ' this doctor on the selected date for this '
                          'week type.'))
