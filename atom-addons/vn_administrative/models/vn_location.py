from odoo import fields, models, api


class VNLocation(models.Model):
    _name = 'vn.location'
    _description = 'Description'
    _rec_name = 'name_with_type'

    name = fields.Char(string="Tên")
    slug = fields.Char(string="Slug")
    type = fields.Char(string="Loại")
    name_with_type = fields.Char(string="Tên + Loại")
    code = fields.Char(string="Mã code")
    path = fields.Char(string="Đường dẫn")
    path_with_type = fields.Char(string="Đường dẫn + Loại")

    parent_id = fields.Many2one('vn.location')

    def _get_parent_code(self):
        for record in self:
            if record.parent_id:
                record.parent_code = record.parent_id.code

    def _set_parent_code(self):
        for record in self:
            if record.parent_code:
                parent = self.search([('code', '=', record.parent_code)], limit=1)
                if parent:
                    record.parent_id = parent.id

    parent_code = fields.Char(compute='_get_parent_code', inverse='_set_parent_code')
