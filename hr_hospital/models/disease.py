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
