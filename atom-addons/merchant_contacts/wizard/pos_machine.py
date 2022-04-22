from odoo import fields, models, api


class PosMachine(models.TransientModel):
    _name = 'pos.machine'

    name = fields.Char()


