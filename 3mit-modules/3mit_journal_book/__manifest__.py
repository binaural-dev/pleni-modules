# -*- coding: utf-8 -*-
{
    'name': "Libro Diario",

    'summary': """
        Libro diario para la Localización venezolana.""",

    'description': """
        * Añade una vista para consultar el libro diario.
        * Añade distintos filtros para mayor comodidad.
        * Reporte de libro diario impreso.
        * Crea un wizard para imprimir el reporte del Libro diario en formatos:
            * Excel.
            * Pdf.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Accounting',
    'version': '1.1',

    'depends': ['base', 'account_accountant', '3mit_multimoneda'],

    'data': [
        'security/ir.model.access.csv',
        'views/journal_book_view.xml',
        'wizard/journal_book_view.xml',
        'views/menu_views.xml',
        'views/report_views.xml',
        'report/journal_book_report.xml',
    ],
}
