# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta
from re import search


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    date_delivery_view = fields.Date(
        string='Fecha Programada de Entrega', compute='_compute_only_date', store=True)
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], string="Bloque de Hora de Entrega")

    @api.depends('commitment_date')
    def _compute_only_date(self):
        for element in self:
            if element.commitment_date and not element.date_delivery_view:
                element.date_delivery_view = element.commitment_date
            else:
                element.commitment_date = element.date_delivery_view

    def write(self, vals):
        date_delivery_view = vals['date_delivery_view'] if 'date_delivery_view' in vals else self.date_delivery_view
        am_pm = vals['am_pm'] if 'am_pm' in vals else self.am_pm
        vals['commitment_date'] = date_delivery_view

        for picking in self.picking_ids:
            picking.scheduled_date_stock = date_delivery_view
            picking.am_pm = am_pm

        for invoice in self.invoice_ids:
            invoice.scheduled_date_account = date_delivery_view
            invoice.am_pm = am_pm

        res = super(SaleOrderInherit, self).write(vals)

        for r in self:
            if 'carrier_id' not in vals:
                r.changing_order_line()
        return res


    @api.onchange('order_line')
    def changing_order_line(self):
        if len(self.order_line) > 0:
            amount_real = sum([line.price_total for line in self.order_line if not line.is_delivery])
            if amount_real > 50:
                delivery_line = self.env['sale.order.line'].search([('order_id', '=', self.id), ('is_delivery', '=', True)])
                if not delivery_line:
                    return
                delivery_line.price_total = 0.0
            else:
                id_2_search = False
                if len(self.ids) > 0:
                    id_2_search = self.ids[0]
                if id_2_search:
                    delivery_line_exists = self.env['sale.order.line'].search([('is_delivery', '=', True), ('order_id', '=', id_2_search)])
                    if not delivery_line_exists:
                        delivery_carrier = self.env['delivery.carrier'].search([('name', '=ilike', 'Delivery')], order='write_date desc', limit=1)
                        if not delivery_carrier:
                            delivery_carrier = delivery_carrier.create({
                                'name': 'Delivery',
                                'product_id': self.env['product.product'].search([('name', '=ilike', 'Delivery'), ('type', '=', 'service')]).id,
                                'fixed_price': 3
                            })
                        self._create_delivery_line(delivery_carrier, delivery_carrier.fixed_price)

    def _create_delivery_line(self, carrier, price_unit):
        SaleOrderLine = self.env['sale.order.line']
        if self.partner_id:
            # set delivery detail in the customer language
            carrier = carrier.with_context(lang=self.partner_id.lang)

        # Apply fiscal position
        taxes = carrier.product_id.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.map_tax(taxes, carrier.product_id, self.partner_id).ids
        print("taxereees", taxes_ids)
        # Create the sales order line
        carrier_with_partner_lang = carrier.with_context(lang=self.partner_id.lang)
        if carrier_with_partner_lang.product_id.description_sale:
            so_description = '%s: %s' % (carrier_with_partner_lang.name, carrier_with_partner_lang.product_id.description_sale)
        else:
            so_description = carrier_with_partner_lang.name
        values = {
            'order_id': self.ids[0],
            'name': so_description,
            'product_uom_qty': 1,
            'product_uom': carrier.product_id.uom_id.id,
            'product_id': carrier.product_id.id,
            'tax_id': [(6, 0, taxes_ids)],
            'is_delivery': True,
        }
        if carrier.invoice_policy == 'real':
            values['price_unit'] = 0
            values['name'] += _(' (Estimated Cost: %s )', self._format_currency_amount(price_unit))
        else:
            values['price_unit'] = price_unit
        if carrier.free_over and self.currency_id.is_zero(price_unit):
            values['name'] += '\n' + 'Free Shipping'
        if self.order_line:
            values['sequence'] = self.order_line[-1].sequence + 1
        sol = SaleOrderLine.sudo().create(values)

        self.delivery_set = True

        return sol


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    is_new_client = fields.Boolean(string='¿Cliente Nuevo?', compute='search_exists_so_with_partner', store=True)

    @api.depends('partner_id')
    def search_exists_so_with_partner(self):
        for record in self:
            if record.partner_id:
                so_count = self.env['sale.order'].search_count([('partner_id', '=', record.partner_id.id), ('state', 'not in', ['draft', 'cancel'])])
                if so_count > 4:
                    record.is_new_client = False
                else:
                    record.is_new_client = True
            else:
                record.is_new_client = False

    scheduled_date_stock = fields.Date(string='Fecha Programada de Entrega')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], string="Bloque de Hora de Entrega")

    @api.model_create_multi
    def create(self, vals_list):

        INCOMING_PICKING = 1
        OUTCOMING_PICKING = 2

        for element in vals_list:
            sale = self.env['sale.order'].search(
                [('name', '=', element['origin'])])

            # When a backorder is created, an extra day is added to the scheduled delivery date.
            if (self and 'backorder_id' in element):
                element['scheduled_date_stock'] = sale.date_delivery_view + \
                    timedelta(days=1)
                element['am_pm'] = sale.am_pm
            # When a return is created, an extra day is added to the scheduled delivery date.
            elif (self and 'picking_type_id' in element and element['picking_type_id'] == INCOMING_PICKING):
                element['scheduled_date_stock'] = element['scheduled_date_stock']
                element['am_pm'] = element['am_pm']
            # When a re-return is created, an extra day is added to scheduled delivert date based into date field.
            elif (self and ('picking_type_id' in element and element['picking_type_id'] == OUTCOMING_PICKING) and search('IN', element['origin'])):
                element['scheduled_date_stock'] = element['date'] + \
                    timedelta(days=1)
                element['am_pm'] = element['am_pm']
            else:
                element['scheduled_date_stock'] = sale.date_delivery_view
                element['am_pm'] = sale.am_pm

        res = super(StockPickingInherit, self).create(vals_list)
        return res


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    scheduled_date_account = fields.Date(
        string='Fecha Programada de Entrega')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], string="Bloque de Hora de Entrega")

    @api.model_create_multi
    def create(self, vals_list):
        for element in vals_list:
            if 'invoice_origin' in element:
                sale = self.env['sale.order'].search(
                    [('name', '=', element['invoice_origin'])])
                element['scheduled_date_account'] = sale.date_delivery_view
                element['am_pm'] = sale.am_pm
        res = super(AccountMoveInherit, self).create(vals_list)
        return res


class SaleReportInherit(models.Model):
    _inherit = 'sale.report'

    scheduled_date_report = fields.Date(
        string='Fecha Programada de Entrega', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['scheduled_date_report'] = ", s.date_delivery_view as scheduled_date_report"
        groupby += ', s.date_delivery_view'
        return super(SaleReportInherit, self)._query(with_clause, fields, groupby, from_clause)
