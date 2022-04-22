# -*- coding: utf-8 -*-

# File: res_partner.py
# Created at 07/12/2021

"""
   Description:
        -
        -
"""
import json
import traceback
from datetime import datetime
import math

import odoo.exceptions
from odoo import http, _, exceptions
from odoo.http import Response
from odoo.http import request
from .constants import HelpdeskTicketConstants

_prefix = '/iapi/v1/'


def make_response(data: dict = {}, msg: str = '', error=None, status=1, error_code=0):
    return {
        "version": "1.0",
        "error": {
            "name": str(error),
            "message": msg,
            "arguments": list(error.args),
            "exception_type": type(error).__name__
        } if error else {},
        'time': datetime.utcnow().timestamp(),
        'data': data,
        'msg': msg,
        'status': status,
        'error_code': error_code
    }


class HelpdeskTicketHub(http.Controller):
    @http.route(
        f'{_prefix}helpdesk/tickets/create',
        type='json', auth='public', methods=["POST"], csrf=False)
    def create_new_helpdesk_ticket_from_iapi(self, **post):
        body = request.jsonrequest
        
        print('Create new ticket from iapi : ', body)
        # args = []
        # kwargs = {}
        # if "args" in post:
        #     args = post["args"]
        # if "kwargs" in post:
        #     kwargs = post["kwargs"]
        
        vals = {
            "partner_name": HelpdeskTicketConstants.partner_name,
            # "company_id": HelpdeskTicketConstants.company_id, #Staging 2
            "stage_id": HelpdeskTicketConstants.stage_id,
            "partner_email": HelpdeskTicketConstants.partner_email,
            "description": body.get("description"),
            "name": body.get("subject"),
            "attachment_ids": False,
            "channel_id": request.env["helpdesk.ticket.channel"]
            .sudo()
            .search([("name", "=", "Email")])
            .id,
            "user_id": HelpdeskTicketConstants.user_id,
            "team_id": HelpdeskTicketConstants.team_id,
            "partner_id": request.env["res.partner"]
            .sudo()
            .search([("name", "=", HelpdeskTicketConstants.partner_name), 
                     ("email", "=", HelpdeskTicketConstants.partner_email),
                     ("id", "=", HelpdeskTicketConstants.partner_id)])
            .id,
        }
        
        new_ticket = request.env["helpdesk.ticket"].sudo().create(vals)
        print('New ticket : ', new_ticket)
        if new_ticket:
            res = {
                'result': 'success'
            }
        else:
            res = {
                'result': 'failed'
            }
        return http.Response(
            json.dumps(res),
            status=200,
            mimetype='application/json'
        )