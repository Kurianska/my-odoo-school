from odoo import models, fields


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Wizard for Monthly Disease Report'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor')
    _rec_name = 'doctor_id'
    year = fields.Char(required=True)
    month = fields.Selection(
        selection=[
            ('1', 'January'),
            ('2', 'February'),
            ('3', 'March'),
            ('4', 'April'),
            ('5', 'May'),
            ('6', 'June'),
            ('7', 'July'),
            ('8', 'August'),
            ('9', 'September'),
            ('10', 'October'),
            ('11', 'November'),
            ('12', 'December')
        ], required=True)
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        required=True)
    diagnosis_count = fields.Integer(
        comodel_name='hr.hospital.diagnosis',
        string="Number of Diagnoses")

    def action_generate_report(self):
        for wizard in self:
            wizard.env['hr.hospital.report.disease'].search([]).unlink()

            first_day = "{}-{}-01".format(wizard.year, wizard.month)
            last_day = "{}-{}-{}".format(wizard.year, wizard.month, 28 if int(
                wizard.month) == 2 else 30)

            domain = [
                ('diagnosis_date', '>=', first_day),
                ('diagnosis_date', '<=', last_day)
            ]
            diagnoses = wizard.env['hr.hospital.diagnosis'].search(domain)

            disease_counts = {}
            for diagnosis in diagnoses:
                disease_id = diagnosis.disease_id.id
                if disease_id not in disease_counts:
                    disease_counts[disease_id] = 0
                disease_counts[disease_id] += 1

            for disease_id, diagnosis_count in disease_counts.items():
                wizard.env['hr.hospital.report.disease'].create({
                    'disease_id': disease_id,
                    'month': wizard.month,
                    'year': wizard.year,
                    'diagnosis_count': diagnosis_count
                })

            return {
                'name': 'Disease Report',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'hr.hospital.report.disease',
                'type': 'ir.actions.act_window',
                'domain': [('month', '=', wizard.month),
                           ('year', '=', wizard.year)],
                'context': {'default_month': wizard.month,
                            'default_year': wizard.year}
            }
