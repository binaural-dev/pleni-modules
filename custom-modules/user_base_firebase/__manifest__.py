# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-Today Geminate Consultancy Services (<http://geminatecs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Userwise Push Notification By Firebase",
    'version': '14.0.0.1',
    'category': 'website',
    'summary': "Userwise Push Notification By Firebase",
    'description': "Geminate comes with a feature of push notification on your device by firebase. user will receive push notification only when he has enabled permission to receive notifications for your website.",
    'license': 'Other proprietary',
    'author': "Geminate Consultancy Services",
    'website': 'http://www.geminatecs.com',
    "depends": [
        'portal', 'base_setup','contacts', 'toastr_in_all'
    ],
    "data": [
        "security/ir.model.access.csv",
        'views/view.xml',
        "wizard/wizard.xml",
        'views/assets.xml',
    ],
    "images": ['static/description/banner.png'],
    "test": [],
    "installable": True,
    'price': 79.99,
    'currency': 'EUR'
}
