# coding: utf-8
##############################################################################
{
    "name": "Calcula la Retención del ISLR",
    "version": "0.3",
    "author": "Localizacion Venezolana",
    "license": "AGPL-3",
    "category": "Contabilidad, facturacion",
    "depends": [
        "account",
        "3mit_account_fiscal_requirements",
        "3mit_base_withholdings",
        '3mit_grupo_localizacion',
        '3mit_menuitems_multicomp',
    ],
    "data": [
        'security/ir.model.access.csv',
         "data/l10n_ve_islr_withholding_data.xml",
         "data/sequence_withholding_islr.xml",
         "view/partner_view.xml",
         "view/res_company_view.xml",
         "view/islr_wh_doc_view.xml",
         "view/islr_wh_concept_view.xml",
         "view/product_view.xml",
         "view/islr_xml_wh.xml",
         "view/invoice_view.xml",
         "view/retention_group_view.xml",
         "report/wh_islr_report.xml",
         "report/wh_islr_report_group.xml",
         "wizard/record_group_retention.xml",
    ],
    "installable": True,
    'application': True,
}


