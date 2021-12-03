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

{
    'name': 'Partner Data Import',
    'summary': "Import Partner Data from CSV or XLS with Different columns",
    'description': "Import Partner Data from CSV or XLS with Different columns",
    'version': '14.0.0.1.0',
    'category': 'Base',
    'author': 'Jupical Technologies Pvt. Ltd.',
    'maintainer': 'Jupical Technologies Pvt. Ltd.',
    'contributors': ['Anil Kesariya <anil.r.kesariya@gmail.com>'],
    'website': 'http://jupical.com/',
    'live_test_url': 'https://www.youtube.com/channel/UC2x2iEL-oW3LrwmB3OO_3hQ/videos',
    'depends': ['base', 'web_notify', 'contacts'],
    'data': [
        'wizard/import_part_data_view.xml',
        'views/import_part_history_view.xml',
        'views/import_part_master_view.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'images': ['static/description/poster_image.png'],
}
