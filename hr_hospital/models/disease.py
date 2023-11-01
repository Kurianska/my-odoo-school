from odoo import models, fields, api


class Disease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Hospital Patient Disease'
    _parent_name = 'parent_id'
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(
        string="Patient Disease", index=True, required=True)
    active = fields.Boolean(
        default=True, )
    complete_name = fields.Char(compute='_compute_complete_name',
                                recursive=True, store=True)
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease', string='Parent Disease',
        index=True, ondelete='restrict')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id', string='Child Diseases')
    disease_count = fields.Integer(compute='_compute_disease_count')

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='disease_id', string='Diagnoses')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = \
                    '%s / %s' \
                    '' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    def _compute_disease_name(self):
        for obj in self:
            obj.disease_count = self.env['hr.hospital.disease'].search_count([
                ('disease_id', 'child', obj.id)

            ])


class ReportDisease(models.TransientModel):
    _name = 'hr.hospital.report.disease'
    _description = 'Disease Report for a Month'

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        required=True)
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
    year = fields.Char()
    diagnosis_count = fields.Integer(
        comodel_name='hr.hospital.diagnosis',
        string="Number of Diagnoses")
