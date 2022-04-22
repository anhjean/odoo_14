from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # partner_id = fields.Many2one('res.partner', string='Hồ sơ đăng ký')
    sequence_code = fields.Char(related="picking_type_id.sequence_code")

    return_from_picking_id = fields.Many2one('stock.picking')

    def _get_return_picking_id(self):
        for record in self:
            record.return_picking_id = False
            if record.out_picking_id and not record.return_from_picking_id:
                return_picking_id = self.env['stock.picking'].search([('return_from_picking_id', '=', record.id)],
                                                                     limit=1)
                print('return_picking_id', return_picking_id)
                if return_picking_id:
                    record.return_picking_id = return_picking_id

    out_picking_id = fields.Many2one('stock.picking')
    return_picking_id = fields.Many2one('stock.picking', compute='_get_return_picking_id')
    out_picking_id_state = fields.Selection(related='out_picking_id.state')

    def _get_first_stock_production_lot(self):
        for record in self:
            record.first_stock_production_lot = False
            if len(record.move_line_ids) > 0:
                record.first_stock_production_lot = record.move_line_ids[0].lot_id

    first_stock_production_lot = fields.Many2one('stock.production.lot', compute='_get_first_stock_production_lot')

    def _get_show_booking(self):
        show_booking = self.env.context.get('show_booking') or False
        for record in self:
            record.show_booking = show_booking

    show_booking = fields.Boolean(compute='_get_show_booking')

    def edit_booking(self):
        view_id = self.env.ref('stock.view_picking_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đặt máy làm hồ sơ',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'view_id': view_id,
            'target': 'new',
            'context': {
                'force_detailed_view': True
            }
        }

    @api.onchange('move_line_ids_without_package')
    def onchange_move_line_ids_without_package(self):
        if len(self.move_line_ids_without_package) > 1 and self.sequence_code == 'BOOKING':
            raise ValidationError('Tối đa 1 máy')

    def make_return(self):
        for line in self.move_line_ids:
            if line.account.status == 'active':
                raise ValidationError(f'Vui lòng khóa tài khoản {line.account.username}, trước khi hoàn trả máy')
        for line in self.move_line_ids:
            line.account.write({
                'status': 'return_machine'
            })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reverse Transfer',
            'res_model': 'stock.return.picking',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.out_picking_id.id,
                'active_model': 'stock.picking',
                'default_return_from_picking_id': self.id
            }
        }
