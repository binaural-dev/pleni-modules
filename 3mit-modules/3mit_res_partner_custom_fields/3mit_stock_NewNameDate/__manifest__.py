# -*- coding: utf-8 -*-
{
    'name': "Cambio Termino Fecha Programada",

    'summary': """
        Cambiar el termino del campo fecha programada de stock.picking y account.move
        """,

    'description': """
    1.0: Cambiar el termino del campo fecha programada heredando del modelo stock.picking y account.move
    2.0: Fue necesario reformular la manera que seabordaba el problema ya que mediante query (como era anteriormente) 
        arrojaba error por ello se cambio y se arreglo mediante las funciones create y write.
    Colaborador: Ricardo Sanchez
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Sale',
    'version': '2.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','account','3mit_account_advance_payment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "views/view.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
