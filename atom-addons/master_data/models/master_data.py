from odoo import fields, models, api


class MasterData(models.Model):
    _name = 'master.data'
    _description = 'Description'
    _rec_name = 'name'

    model = fields.Char(string="Đối tượng")
    field = fields.Char(string="Trường dữ liệu")
    value = fields.Char(string="Giá trị")
    name = fields.Char(string="Hiển thị")
