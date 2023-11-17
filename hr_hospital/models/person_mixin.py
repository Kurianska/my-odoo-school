from odoo import fields, models


class PersonMixin(models.AbstractModel):
    _name = 'person.mixin'
    _description = 'Hospital Person Mixin'

    name = fields.Char(
        string='Person Name', required=True)

    active = fields.Boolean(
        default=True, )
    phone = fields.Char(required=True,)
    email = fields.Char(required=True,)
    address = fields.Char()
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female')
    ], default='male')
    image = fields.Image()
