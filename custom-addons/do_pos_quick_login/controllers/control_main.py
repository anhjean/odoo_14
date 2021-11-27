from odoo.addons.web.controllers.main import Home as Home
from odoo.exceptions import AccessError
from odoo.http import request

import json
import logging
import werkzeug.utils

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Home(Home):

    def _login_redirect(self, uid, redirect=None):
        res_users_obj=request.env['res.users']
        if uid:
            search_user=res_users_obj.search([('id','=',uid)],limit=1)            
            if search_user and search_user.pos_config_id:
                if search_user.pos_config_id.pos_session_state==False and search_user.pos_config_id.pos_session_username==False:
                    res = search_user.pos_config_id.open_session_cb()
                    return redirect if redirect else '/pos/web'
                elif search_user.pos_config_id.current_session_state=='opened' and search_user.pos_config_id.pos_session_username==request.env.user.name:                    
                    return redirect if redirect else '/pos/web'  
                else:
                    return redirect if redirect else '/web'
        return redirect if redirect else '/web'

    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        response = super(Home, self).web_login(redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            search_user = request.env['res.users'].browse(request.uid)
            if search_user and search_user.pos_config_id:
                if search_user.pos_config_id.pos_session_state==False and search_user.pos_config_id.pos_session_username==False:
                    res = search_user.pos_config_id.open_session_cb()
                    redirect = b'/pos/web?' + request.httprequest.query_string
                elif search_user.pos_config_id.current_session_state=='opened' and search_user.pos_config_id.pos_session_username==request.env.user.name:                    
                    redirect = b'/pos/web?' + request.httprequest.query_string
            elif search_user.has_group('base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                redirect = '/my'
            return http.redirect_with_hash(redirect)
        return response
