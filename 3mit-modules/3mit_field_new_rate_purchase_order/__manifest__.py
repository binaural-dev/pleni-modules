# coding: utf-8
##############################################################################
#
# Copyright (c) 2016 Tecnología y Servicios AMN C.A. (http://3MIT.com/) All Rights Reserved.
# <contacto@3MIT.com>
# <Teléfono: +58(212) 237.77.53>
# Caracas, Venezuela.
#
# Colaborador: <<Ismael Castillo>> <ismael@3mit.dev>
#
##############################################################################

{
    'name': 'Agregando nuevo campo a pedido de compras',
    'version': '1.0',
    'author': '3MIT',
    'depends': ['sale', 'purchase', 'base', 'sale_management','3mit_grupo_localizacion', '3mit_rates'],
    'data': [
    "views/view_field.xml"
    ],
    'installable': True,
    'active': True,
}
