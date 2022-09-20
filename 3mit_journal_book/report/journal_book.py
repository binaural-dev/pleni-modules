# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.exceptions import UserError
import time
from datetime import datetime


class JournalBookReport(models.AbstractModel):
    _name = 'report.3mit_journal_book.journal_book_report'
    _description = 'Get data to print journal book report'

    @api.model
    def _get_report_values(self, docids, data):
        filter_wizard = data['form']['filter_wizard']

        if filter_wizard == 'fecha':
            date_init = data['form']['date_init']
            date_end = data['form']['date_end']
        else:
            date_init = data['form']['dates'][0][0:10]
            date_end = data['form']['dates'][1][0:10]

        account_move_line = self.env['account.move.line'].search([('date', '>=', date_init), ('date', '<=', date_end), ('parent_state', '=', 'posted')])
        ids_in_lines = [line.code_account_id for line in account_move_line]
        ids_in_lines = list(set(ids_in_lines))
        date_init = datetime.strptime(date_init.replace('-', '/'), '%Y/%m/%d')
        date_init = datetime.strftime(date_init, '%d/%m/%Y')
        date_end = datetime.strptime(date_end.replace('-', '/'), '%Y/%m/%d')
        date_end = datetime.strftime(date_end, '%d/%m/%Y')

        if account_move_line:
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

            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'actual_company': self.env.company,
                'lines': amount_dict,
                'total_debit': total_debit,
                'total_credit': total_credit,
                'print_date': print_date,
                'print_hour': print_hour,
                'date_init': date_init,
                'date_end': date_end,
                'period': data['form']['period'],
                'register_total': len(ids_in_lines)
            }
        else:
            raise UserError("No se han encontrado registros en el período establecido.")

    @staticmethod
    def separador_cifra(valor):
        monto = '{0:,.2f}'.format(valor).replace('.', '-')
        monto = monto.replace(',', '.')
        monto = monto.replace('-', ',')
        return monto
