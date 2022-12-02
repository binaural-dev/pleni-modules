# -*- coding: utf-8 -*-
{
    'name': "Pleni - Whatsapp Integration",
    'version': '0.1',
    'category': 'Uncategorized',
    'author': "Manuel Escalante",
    'license': 'GPL-3',
    'website': "https://pleni.app",
    'depends': [
        'base',
        'sale',
        'web',
        'stock',
        'purchase',
        'account',
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/sms_security.xml',
        'views/setting_inherit_view.xml',
        'views/template.xml',
        'views/views.xml',
        'wizard/message_wizard.xml',
        'wizard/share_action.xml',
        'wizard/wizard.xml',
        'wizard/wizard_contact.xml',
        'wizard/wizard_multiple_contact.xml',
    ],
}
