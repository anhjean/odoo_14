from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    made_mrp = fields.Boolean(default=False, help="Default value is false ")

    def update_made_mrp(self):
        if self.made_mrp == False:
            self.made_mrp = True