from odoo import models, fields
from odoo.tools.translate import translate

class District(models.Model):
    # _name is the important field to define the global name of model
    _name = "res.country.district"
    # _descriptin is define the friendly name for model
    _description = "District"
    
    name = fields.Char('District name', translate=True)
    state_id = fields.Many2one(comodel_name='res.country.state',string='State')