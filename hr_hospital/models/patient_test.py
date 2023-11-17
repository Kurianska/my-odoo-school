from odoo import models, fields


class HospitalPatientTest(models.Model):
    _name = 'hr.hospital.patient.test'
    _description = 'Hospital Patient Test Record'
    _inherit = ['hr.hospital.patient']

    name = fields.Char(string="Test Name", required=True)
    active = fields.Boolean(default=True)
    date = fields.Date(string="Test Date", required=True)
    patient_id = fields.Many2one(
        comodel_name="hr.hospital.patient",
        string="Patient Name", required=True)
    phone = fields.Char(related="patient_id.phone", required=True, store=True)
    email = fields.Char(related="patient_id.email", required=True, )
    birthday_date = fields.Char(related="patient_id.birthday_date",
                                string='Patient Birthday Date', required=True)
    passport_data = fields.Char(related="patient_id.passport_data",
                                string='Patient Passport Data', required=True)
    age = fields.Integer(related="patient_id.age",
                         required=True)
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', string="Doctor")

    test_type = fields.Selection([
        ('blood', 'Blood Analysis'),
        ('cytological', 'Cytological Examination'),
        ('hormonal', 'Hormonal Test'),
        ('genetic', 'Genetic Test'),
    ], required=True)
