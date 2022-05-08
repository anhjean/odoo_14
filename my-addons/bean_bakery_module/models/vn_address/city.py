from odoo import models, fields
from odoo.tools.translate import translate

class City(models.Model):
    # _name is the important field to define the global name of model
    _name = "res.country.city"
    _description = 'City'
    _order = 'name'
    
    code = fields.Char(string="City Code",help='The City code.', required=True)
    slug = fields.Char(string="City Code ID")
    state_id = fields.Many2one(comodel_name='res.country.state',string='State')
    name = fields.Char(string="City Name", translate=True)