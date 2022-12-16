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
    'name': "Toastr in all",
    'version': '14.0.0.1',
    'category': 'tools',
    'summary': "Toastr in all",
    'description': " Geminate comes with the feature of Toastr In All. Toastr is a Javascript library for non-blocking notifications. it comes with a bunch of options which you can use as per your need with different layouts.",
    'license': 'Other proprietary',
    'author': "Geminate Consultancy Services",
    'website': 'http://www.geminatecs.com',
    "depends": [
        'base'
    ],
    "data": [
        "views/assets.xml",
    ],
    "images": ['static/description/banner.png'],
    "test": [],
    "installable": True,
    'price': 39.99,
    'currency': 'EUR'
}
