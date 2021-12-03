# -*- coding: utf-8 -*-
##############################################################################
#
#    Jupical Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Jupical Technologies(<http://www.jupical.com>).
#    Author: Jupical Technologies Pvt. Ltd.(<http://www.jupical.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz


class ImportPartner(models.TransientModel):

    _name = 'import.partner'
    _description = "Import Partner"

    name = fields.Char('File name')
    file = fields.Binary('File')
    state = fields.Selection([('init', 'init'), ('done', 'done')],
                             string='Status', readonly=True, default='init')
    type = fields.Selection([("csv", "CSV"), ("xlsx", "XLSX")],
                            default="csv", string="File type.")
    operation = fields.Selection(
        [('create', 'Create Record'), ('update', 'Update Record')],
        default='create')

    def import_data_through_cron(self):
        self.ensure_one()
        cron_obj = self.env['ir.cron']
        now_time = datetime.now() + timedelta(seconds=30)
        part_master = self.env['import.part.master'].create({
            'file': self.file,
            'filename': self.name,
            'type': self.type,
            'file_updated': True,
            'user_id': self._uid,
            'status': 'in_process',
            'operation': self.operation,
        })

        user_tz = self.env.user.tz or str(pytz.utc)
        local = pytz.timezone(user_tz)
        user_time_zone = datetime.strftime(pytz.utc.localize(
            datetime.strptime(datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S'),
                              DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),
            DEFAULT_SERVER_DATETIME_FORMAT)
        order_model = self.env['ir.model'].search(
            [('model', '=', 'res.partner')])
        cron_data = {
            'name': "Import Partners" + ' - ' + user_time_zone,
            'code': 'model.import_data(%s)' % part_master.id,
            'nextcall': now_time,
            'numbercall': -1,
            'user_id': self._uid,
            'model_id': order_model.id,
            'state': 'code',
        }

        cron = cron_obj.sudo().create(cron_data)
        part_master.cron_id = cron.id
        self.state = 'done'
        return {
            'name': _('Import Order'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.partner',
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }
