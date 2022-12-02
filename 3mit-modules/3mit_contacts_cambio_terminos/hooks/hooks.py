from odoo import api, SUPERUSER_ID


def cambio_terminos(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    termino1 = env['ir.translation'].search([('module', '=', 'base'), ('value', '=', 'Móvil')])
    for element in termino1:
        element.value = "Teléfono Móvil"
    termino2 = env['ir.translation'].search([('module', '=', 'purchase'), ('value', '=', 'Pedidos de compra')])
    for element in termino2:
        element.value = "Ordenes de Compra"


def revertir_cambios(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    termino1 = env['ir.translation'].search([('module', '=', 'base'), ('value', '=', 'Teléfono Móvil')])
    for element in termino1:
        element.value = "Móvil"
    termino2 = env['ir.translation'].search([('module', '=', 'purchase'), ('value', '=', 'Pedidos de compra')])
    for element in termino2:
        element.value = "Ordenes de Compra"