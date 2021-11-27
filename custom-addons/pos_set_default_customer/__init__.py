# # -*- coding: utf-8 -*-
from . import models

def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import UserError
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie != '14.0':
        raise UserError(('Module support Odoo Version 14.0 only and found ' + server_serie))
    return True
