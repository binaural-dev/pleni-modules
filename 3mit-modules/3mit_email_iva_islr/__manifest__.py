# -*- coding: utf-8 -*-
{
    'name': "Email: Información I.V.A. e I.S.L.R.",

    'summary': """
        Envía un email automático al partner al momento de confirmar el documento 
        de I.V.A. o I.S.L.R. según sea el caso.""",

    'description': """
        * Verifica si existe un email asociado al partner y lo setea como obligatorio.
        * Crea un template para enviar el Comprobante del I.V.A.
        * Envía automáticamente por correo el Comprobante de I.V.A. una vez confirmado.
        * Crea un template para enviar el Detalle de Retenciones de I.S.L.R.
        * Envía automáticamente por correo el Detalle de Retenciones de I.S.L.R. una vez confirmado.\n\n
        Elaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Accounting',
    'version': '1.0.1',

    'depends': ['base', 'account', '3mit_account_fiscal_requirements',
                '3mit_base_withholdings', '3mit_iva_withholding', '3mit_withholding_islr', '3mit_retention_islr', '3mit_grupo_localizacion'],

    'data': [
        'views/islr_wh_doc_suppliers_inherit_view.xml',
        # 'views/islr_wh_doc_inherit_view.xml',
        'views/email_template_islr.xml',
        'views/account_wh_iva_inherit_view.xml',
        'views/email_template_iva.xml',
    ],
    'installable': True,
    'active': True,
}
