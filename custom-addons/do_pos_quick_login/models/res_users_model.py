from odoo import models,fields,api

class res_users(models.Model):
    _inherit="res.users"
    
    pos_config_id=fields.Many2one("pos.config",string="POS Configuration")