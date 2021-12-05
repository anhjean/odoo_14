# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields


class PosConfigImage(models.Model):
    _inherit = 'pos.config'

    image = fields.Binary(string='Image')
    pos_bank_holder = fields.Char(
        string="Bank Holder",
        help="Defines the value of the"
        " client-side timeout for the creation of PoS Order(s)"
        " from the POS UI.\n",
    )
    pos_bank_name = fields.Char(
        string="Bank Name",
        help="Defines the value of the"
        " client-side timeout for the creation of PoS Order(s)"
        " from the POS UI.\n",
    )
    pos_bank_account = fields.Char(
        string="Bank Account",
        help="Defines the value of the"
        " client-side timeout for the creation of PoS Order(s)"
        " from the POS UI.\n",
    )
   
