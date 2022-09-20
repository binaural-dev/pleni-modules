# coding: utf-8
##############################################################################
#
# Copyright (c) 2016 Tecnología y Servicios AMN C.A. (http://3MIT.com/) All Rights Reserved.
# <contacto@3MIT.com>
# <Teléfono: +58(212) 237.77.53>
# Caracas, Venezuela.
#
# Colaborador: <<Diego Marfil>> <diego@3mit.dev>
#
##############################################################################

{
    'name': 'Tasas Cambiarias',
    'version': '1.0',
    'author': '3MIT',
    'depends': ['account_accountant', 'sale', 'purchase', 'base', '3mit_grupo_localizacion'],
    'data': ["view/views.xml", "view/account_move_view.xml"],
    'installable': True,
    'active': True,
}
