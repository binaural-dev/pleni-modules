# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning, UserError
from datetime import date, datetime
import time
from io import BytesIO
import xlwt
import base64
import locale
import calendar

MESES = {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio',
         '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'}


class JournalBook(models.TransientModel):
    _name = 'journal.book.wizard'
    _description = 'Wizard to print journal book'

    @api.onchange('date_end')
    def checking_date(self):
        if self.date_end > date.today():
            raise Warning("¡La fecha colocada no puede ser mayor a la actual!")

    filter_wizard = fields.Selection(selection=[('fecha', 'Fecha'), ('mes_anio', 'Mes - Año')], string="tipo")
    month = fields.Selection(selection=[('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'),
                                        ('05', 'Mayo'), ('06', 'Junio'), ('07', 'Julio'), ('08', 'Agosto'),
                                        ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'),
                                        ('12', 'Diciembre')], string="Mes")
    year = fields.Integer(string="Año")
    date_init = fields.Date(string='Fecha inicial')
    date_end = fields.Date(string='Fecha final', default=date.today())
    # Campos para la descarga del xls
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')
    report = fields.Binary(string='Descargar xls', filters='.xls', readonly=True)
    name = fields.Char(string='File Name', size=32)

    def print_jb_pdf(self):
        form = None
        if self.filter_wizard == 'fecha':
            form = {
                'date_init': self.date_init,
                'date_end': self.date_end,
                'filter_wizard': self.filter_wizard,
                'period': self.set_period()
            }
        elif self.filter_wizard == 'mes_anio':
            form = {
                'dates': self.set_range(),
                'filter_wizard': self.filter_wizard,
                'period': self.set_period()
            }
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': form,
        }
        action = self.env.ref('3mit_journal_book.action_report_journal_book').report_action(self, data=data)
        action.update({'close_on_report_download': True})
        return action

    def print_jb_xls(self):
        # Buscar account.move.line según wizard
        account_move_line = None
        if self.filter_wizard == 'fecha':
            account_move_line = self.env['account.move.line'].search([('date', '>=', self.date_init), ('date', '<=', self.date_end), ('parent_state', '=', 'posted')])
            date_init = datetime.strftime(self.date_init, '%d/%m/%Y')
            date_end = datetime.strftime(self.date_end, '%d/%m/%Y')
        else:
            dates = self.set_range()
            date_init, date_end = dates[0], dates[1]
            account_move_line = self.env['account.move.line'].search([('date', '>=', date_init), ('date', '<=', date_end), ('parent_state', '=', 'posted')])
            date_init = str(datetime.strftime(date_init, '%d/%m/%Y')).replace('-', '/')
            date_end = str(datetime.strftime(date_end, '%d/%m/%Y')).replace('-', '/')
        if account_move_line:
            ids_in_lines = [line.code_account_id for line in account_move_line]
            ids_in_lines = list(set(ids_in_lines))
            amount_dict, total_debit, total_credit, line = [], 0, 0, ''
            for ids in ids_in_lines:
                debit, credit, name = 0, 0, ''
                for line in account_move_line:
                    if line.code_account_id == ids:
                        debit += line.debit
                        credit += line.credit
                        name = line.name_account_id
                amount_dict.append({'code': ids, 'debit': self.separador_cifra(debit), 'credit': self.separador_cifra(credit), 'name': name})
                total_debit += debit
                total_credit += credit

            total_debit = self.separador_cifra(total_debit)
            total_credit = self.separador_cifra(total_credit)
            print_hour = time.strftime('%H:%M:%S', time.localtime())
            print_date = time.strftime('%d/%m/%Y', time.localtime())

            # Generar el archivo en Excel
            self.ensure_one()
            fp = BytesIO()
            wb = xlwt.Workbook(encoding='UTF-8')
            writer = wb.add_sheet('Diario legal')
            locale.setlocale(locale.LC_ALL, '')

            # Se agrega altitud a las filas
            writer.row(0).height_mismatch = True
            writer.row(0).height = 200
            writer.row(1).height_mismatch = True
            writer.row(1).height = 420
            writer.row(2).height_mismatch = True
            writer.row(2).height = 420
            writer.row(3).height_mismatch = True
            writer.row(3).height = 420
            writer.row(4).height_mismatch = True
            writer.row(4).height = 420
            writer.row(5).height_mismatch = True
            writer.row(5).height = 420
            writer.row(6).height_mismatch = True
            writer.row(6).height = 420
            writer.row(7).height_mismatch = True
            writer.row(7).height = 420
            writer.row(8).height_mismatch = True
            writer.row(8).height = 420

            # Se agrega ancho a las columnas
            writer.col(0).width = 1000
            writer.col(1).width = 4000
            writer.col(2).width = 4000
            writer.col(3).width = 4000
            writer.col(4).width = 4000
            writer.col(5).width = 4000
            writer.col(6).width = 4000
            writer.col(7).width = 4000
            writer.col(8).width = 4000
            writer.col(9).width = 4000
            writer.col(10).width = 4000

            # ENCABEZADO DEL REPORTE
            writer.write_merge(1, 1, 1, 2, self.env.company.name, xlwt.easyxf("font: height 280, bold 1;"))

            writer.write_merge(1, 1, 8, 8, 'Fecha:', xlwt.easyxf("font: height 200;"))
            writer.write_merge(1, 1, 9, 9, print_date, xlwt.easyxf("font: height 200;"))
            writer.write_merge(2, 2, 8, 8, 'Hora:', xlwt.easyxf("font: height 200;"))
            writer.write_merge(2, 2, 9, 9, print_hour, xlwt.easyxf("font: height 200;"))

            writer.write_merge(4, 4, 8, 8, 'Ejercicio Actual', xlwt.easyxf("font: height 200;"))
            writer.write_merge(5, 5, 8, 8, 'Desde:', xlwt.easyxf("font: height 200;"))
            writer.write_merge(5, 5, 9, 9, date_init, xlwt.easyxf("font: height 200;"))
            writer.write_merge(6, 6, 8, 8, 'Hasta:', xlwt.easyxf("font: height 200;"))
            writer.write_merge(6, 6, 9, 9, date_end, xlwt.easyxf("font: height 200;"))

            writer.write_merge(2, 2, 1, 4, '{} {}'.format(self.env.company.street, self.env.company.street2), xlwt.easyxf("font: height 240;"))
            writer.write_merge(3, 3, 1, 4, '{} {}'.format(self.env.company.city, self.env.company.state_id.name), xlwt.easyxf("font: height 240;"))
            writer.write_merge(4, 4, 1, 1, 'R.I.F.:', xlwt.easyxf("font: height 240;"))
            writer.write_merge(4, 4, 2, 3, self.env.company.vat, xlwt.easyxf("font: height 240;"))
            writer.write_merge(5, 5, 1, 2, 'Diario Legal', xlwt.easyxf("font: height 240, bold 1;"))
            writer.write_merge(6, 6, 1, 1, 'Período:', xlwt.easyxf("font: height 240;"))
            writer.write_merge(6, 6, 2, 3, self.set_period(), xlwt.easyxf("font: height 240;"))

            # ESTRUCTURA DEL REPORTE
            writer.write_merge(8, 8, 1, 2, 'CÓDIGO', xlwt.easyxf("pattern: pattern solid; font: height 240;"))
            writer.write_merge(8, 8, 3, 5, 'DESCRIPCIÓN', xlwt.easyxf("pattern: pattern solid; font: height 240;"))
            writer.write_merge(8, 8, 6, 7, 'DÉBITOS', xlwt.easyxf("pattern: pattern solid; font: height 240;"))
            writer.write_merge(8, 8, 8, 9, 'CRÉDITOS', xlwt.easyxf("pattern: pattern solid; font: height 240;"))

            init = 9
            for line in amount_dict:
                writer.write_merge(init, init, 1, 2, line['code'], xlwt.easyxf("font: height 240;"))
                writer.write_merge(init, init, 3, 5, line['name'], xlwt.easyxf("font: height 240;"))
                writer.write_merge(init, init, 6, 7, line['debit'], xlwt.easyxf("font: height 240;"))
                writer.write_merge(init, init, 8, 9, line['credit'], xlwt.easyxf("font: height 240;"))
                init += 1
            writer.write_merge(init, init, 3, 5, 'TOTAL DIARIO LEGAL', xlwt.easyxf("font: height 240, bold 1;"))
            writer.write_merge(init, init, 6, 7, total_debit, xlwt.easyxf("font: height 240, bold 1;"))
            writer.write_merge(init, init, 8, 9, total_credit, xlwt.easyxf("font: height 240, bold 1;"))
            writer.write_merge(init + 2, init + 2, 7, 7, 'Total de registros:', xlwt.easyxf("font: height 240, bold 1;"))
            writer.write_merge(init + 2, init + 2, 8, 8, len(amount_dict), xlwt.easyxf("font: height 240, bold 1;"))
            # Guardar la data
            wb.save(fp)
            out = base64.encodebytes(fp.getvalue())
            self.write({'state': 'get', 'report': out, 'name': 'Diario legal {}.xls'.format(self.set_period())})

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'journal.book.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'views': [(False, 'form')],
                'target': 'new',
            }
        else:
            raise UserError("No se han encontrado registros en el período establecido.")

    @staticmethod
    def separador_cifra(valor):
        monto = '{0:,.2f}'.format(valor).replace('.', '-')
        monto = monto.replace(',', '.')
        monto = monto.replace('-', ',')
        return monto

    def set_range(self):
        last_month_day = calendar.monthrange(self.year, int(self.month))[1]
        last_range = '{}-{}-{}'.format(self.year, self.month, last_month_day)
        first_range = '{}-{}-01'.format(self.year, self.month)
        date_first_range = datetime.strptime(first_range, '%Y-%m-%d')
        date_last_range = datetime.strptime(last_range, '%Y-%m-%d')
        return date_first_range, date_last_range

    def set_period(self):
        if self.filter_wizard == 'mes_anio':
            return MESES[self.month]
        else:
            date_end = datetime.strftime(self.date_end, '%d/%m/%Y')
            date_init = datetime.strftime(self.date_init, '%d/%m/%Y')
            if MESES[date_end[3:5]] == MESES[date_init[3:5]]:
                return MESES[date_init[3:5]]
            else:
                return "{} - {}".format(MESES[date_init[3:5]], MESES[date_end[3:5]])
