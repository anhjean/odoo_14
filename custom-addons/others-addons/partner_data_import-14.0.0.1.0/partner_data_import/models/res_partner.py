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

from odoo import models,api,fields,_
import logging
import base64
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz
from xlrd import open_workbook
import tempfile
import csv
import requests
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def remove_finish_import_crons(self):
        master_partners = self.env['import.part.master'].search(
            ['|', ('status', '=', 'imported'), ('status', '=', 'failed')])
        # Remove completed crons
        for master_part in master_partners:
            if master_part.cron_id:
                master_part.cron_id.unlink()
        # Remove the Import status lines
        imported_master_part = self.env['import.part.master'].search(
            [('status', '=', 'imported')])
        imported_master_part.unlink()

    def import_data(self, part_master_id=False):
        if part_master_id:
            part_master = self.env[
                'import.part.master'].browse(part_master_id)
            total_success_import_record = 0
            total_failed_record = 0
            list_of_failed_record = ''
            datafile = part_master.file
            file_name = str(part_master.filename)
            partner_obj = self.env['res.partner']
            state_obj = self.env['res.country.state']
            country_obj = self.env['res.country']
            try:
                if not datafile or not \
                        file_name.lower().endswith(('.xls', '.xlsx', '.csv')):
                    list_of_failed_record += "Please Select an .xls or .csv or its compatible file to Import."
                    _logger.error(
                        "Please Select an .xls or .csv or its compatible file to Import.")
                if part_master.type == 'csv':
                    if not datafile or not file_name.lower().endswith(('.csv')):
                        list_of_failed_record += "Please Select an .csv or its compatible file to Import."
                        _logger.error(
                            "Please Select an .csv or its compatible file to Import.")
                    file_path = tempfile.gettempdir() + '/import.csv'
                    f = open(file_path, 'wb+')
                    f.write(base64.decodestring(part_master.file))
                    f.close()

                    archive = csv.DictReader(open(file_path))
                    archive_lines = [line for line in archive]
                    count = 1
                    for line in archive_lines:
                        try:
                            count += 1
                            partner_vals = {
                                'name': line.get('Name'),
                                'street': line.get('street') or '',
                                'street2': line.get('street2') or '',
                                'city': line.get('city') or '',
                                'phone': line.get('phone') or '',
                                'mobile': line.get('mobile') or '',
                                'email': line.get('email') or '',
                                'company_type': line.get('ctype'),
                                'vat': line.get('vat') or '',
                                'website': line.get('website') or '',
                                'zip': line.get('zip') or '',
                            }
                            state = state_obj.search(
                                [('name', '=', line.get('state'))])
                            country = country_obj.search(
                                [('name', '=', line.get('country'))])
                            partner_vals['state_id'] = state.id or ''
                            partner_vals[
                                'country_id'] = country.id or ''

                            if part_master.operation == 'create':
                                partner_obj.create(partner_vals)

                            else:
                                part_id = self.env['res.partner'].search(
                                    [('name', '=', line.get('Name', ''))], limit=1)
                                if not part_id:
                                    part_id = partner_obj.create(
                                        partner_vals)
                                else:
                                    part_id.write(partner_vals)
                            total_success_import_record += 1
                        except Exception as e:
                            total_failed_record += 1
                            list_of_failed_record += line
                            _logger.error("Error at %s" % str(line))
                else:
                    if not datafile or not file_name.lower().endswith(('.xls', '.xlsx',)):
                        list_of_failed_record += "Please Select an .xls or its compatible file to Import."
                        _logger.error(
                            "Please Select an .xls or its compatible file to Import.")

                    temp_path = tempfile.gettempdir()
                    file_data = base64.decodestring(datafile)
                    fp = open(temp_path + '/xsl_file.xls', 'wb+')
                    fp.write(file_data)
                    fp.close()
                    wb = open_workbook(temp_path + '/xsl_file.xls')
                    data_list = []
                    header_list = []
                    headers_dict = {}
                    for sheet in wb.sheets():
                        # Sales data xlsx
                        for rownum in range(sheet.nrows):
                            if rownum == 0:
                                header_list = [
                                    x for x in sheet.row_values(rownum)]
                                headers_dict = {
                                    'name': header_list.index('Name'),
                                    'mobile': header_list.index('Mobile'),
                                    'phone': header_list.index('Phone'),
                                    'email': header_list.index('Email'),
                                    'vat': header_list.index('Vat'),
                                    'street': header_list.index('Street'),
                                    'street2': header_list.index('Street2'),
                                    'city': header_list.index('City'),
                                    'company_type': header_list.index('Company Type'),
                                    'website': header_list.index('Website'),
                                    'state': header_list.index('State'),
                                    'country': header_list.index('Country'),
                                    'zip': header_list.index('ZIP'),
                                }
                            if rownum >= 1:
                                data_list.append(sheet.row_values(rownum))
                        count = 1
                        for row in data_list:
                            try:
                                count += 1

                                state = state_obj.search(
                                    [('name', '=', row[headers_dict['state']])])
                                country = country_obj.search(
                                    [('name', '=', row[headers_dict['country']])])

                                partner_vals = {
                                    'name': row[headers_dict['name']],
                                    'phone': row[headers_dict['phone']] or '',
                                    'mobile': row[headers_dict['mobile']] or '',
                                    'email': row[headers_dict['email']] or '',
                                    'vat': row[headers_dict['vat']] or '',
                                    'street': row[headers_dict['street']] or '',
                                    'street2': row[headers_dict['street2']] or '',
                                    'city': row[headers_dict['city']] or '',
                                    'state_id': state.id or '',
                                    'country_id': country.id or '',
                                    'zip': row[headers_dict['zip']] or '',
                                    'company_type': row[headers_dict['company_type']],
                                }
                                if part_master.operation == 'create':
                                    order_id = partner_obj.create(
                                        partner_vals)
                                else:
                                    order_id = self.env['res.partner'].search(
                                        [('name', '=', row[headers_dict['name']])], limit=1)
                                    if not order_id:
                                        order_id = partner_obj.create(
                                            partner_vals)
                                    else:
                                        order_id.write(partner_vals)
                                total_success_import_record += 1
                            except Exception as e:
                                total_failed_record += 1
                                list_of_failed_record += row
                                _logger.error("Error at %s" % str(row))
            except Exception as e:
                list_of_failed_record += str(e)
            try:
                file_data = base64.b64encode(
                    list_of_failed_record.encode('utf-8'))
                part_master.status = 'imported'
                datetime_object = datetime.strptime(
                    str(part_master.create_date), '%Y-%m-%d %H:%M:%S.%f')
                start_date = datetime.strftime(
                    datetime_object, DEFAULT_SERVER_DATETIME_FORMAT)
                self._cr.commit()
                now_time = datetime.now()
                user_tz = self.env.user.tz or str(pytz.utc)
                local = pytz.timezone(user_tz)
                start_date_in_user_tz = datetime.strftime(pytz.utc.localize(
                    datetime.strptime(str(start_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(
                    local), DEFAULT_SERVER_DATETIME_FORMAT)
                end_date_in_user_tz = datetime.strftime(pytz.utc.localize(
                    now_time).astimezone(local),
                    DEFAULT_SERVER_DATETIME_FORMAT)
                self.env['import.part.history'].create({
                    'total_success_count': total_success_import_record,
                    'total_failed_count': total_failed_record,
                    'file': file_data,
                    'file_name': 'report_importazione.txt',
                    'type': part_master.type,
                    'import_file_name': part_master.filename,
                    'start_date': start_date_in_user_tz,
                    'end_date': end_date_in_user_tz,
                    'operation': part_master.operation,
                })
                if part_master.user_id:
                    message = "Import process is completed. Check in Imported Partner History if all the partners have" \
                              " been imported correctly. </br></br> Imported File: %s </br>" \
                              "Imported by: %s" % (
                                  part_master.filename, part_master.user_id.name)
                    part_master.user_id.notify_partner_info(
                        message, part_master.user_id, sticky=True)
                self._cr.commit()
            except Exception as e:
                part_master.status = 'failed'
                _logger.error(e)
                self._cr.commit()
