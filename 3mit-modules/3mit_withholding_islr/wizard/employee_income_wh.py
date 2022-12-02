#    Description: Gets a CSV file from data collector and import it to
#                 sale order
#
##############################################################################
import base64
import functools
import logging
import xlrd
import odoo.exceptions
from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import codecs
import time
import datetime

FIELDNAMES = [
    'RIF Retenido',
    'Número Factura',
    'Número Control',
    'Fecha Operación',
    'Codigo Concepto',
    'Monto Operación',
    'Retención'
]

# ---------------------------------------------------------- employee_income_wh


class EmployeeIncomeWh(models.Model):

    _name = 'employee.income.wh'

    _description = ''

    logger = logging.getLogger('employee.income.wh')

    @api.model_create_single
    def create(self, vals_list):
        create = super(EmployeeIncomeWh, self).create(vals_list)
        create.process_employee_income_wh()
        return create

    def _parse_csv_employee_income_wh(self, csv_file):
        '''
        Method to parse CSV File
        '''
        str_file = None
        # es importante que el csv este delimitado por punto y coma ";"
        try:
            str_file = codecs.decode(csv_file, 'UTF-8')
            if not(';' in str_file):
                raise odoo.exceptions.UserError('El Archivo CSV tiene que estar delimitado por punto y coma (;)')
        except Exception as err:
            raise odoo.exceptions.UserError('Verifíque si el archivo que usted cargo es un CSV .')

        get_rows = str_file.split('\n')
        keys = FIELDNAMES
        num_keys = len(keys)
        last_index_keys = num_keys - 1
        dicts_vals = []
        #Recorrer todas las filas
        for row in get_rows:
            if row != get_rows[0]:
                #Obtener los valores de la fila actual
                row_vals = row.split(';')
                dict_record = {}
                val_index = 0
                none_values = []
                #Recorrer los valores de la fila actual
                for val in row_vals:
                    #si la posicion del valor es menor o igual a la posicion de
                    #la ultima columna de las keys
                    if  val_index <= last_index_keys:
                        #en caso de que no haya valor
                        if val == '':
                            none_values.append(True)
                        else:
                            none_values.append(False)

                        dict_record[keys[val_index]] = val
                        val_index = val_index + 1
                #en caso de que haya un campo sin rellenar
                if not(True in none_values):
                    dicts_vals.append(dict_record)
        if not(dicts_vals):
            raise odoo.exceptions.UserError('Verifíque el archivo CSV, es probable que existan campos sin rellenar.')

        if set(keys) < set(FIELDNAMES):
            msg = _('Faltan campos en el archivo CSV.\n'
                    'El archivo debe tener los siguientes campos:\n')
            for fn in FIELDNAMES:
                msg += '{field},\n'.format(field=fn)
            raise UserError("Error! \n %s" % (msg))
        return dicts_vals

    def _parce_excel_employee_income_wh(self, xml_file):
        try:
            open_workbook = xlrd.open_workbook(file_contents=xml_file)
        except Exception as err:
            raise odoo.exceptions.UserError('Verifique si el archivo es un archivo excel (.xls o .xlsx).')
        sheets = open_workbook.sheets()
        keys = FIELDNAMES
        num_keys = len(keys)
        last_index_keys = num_keys - 1
        values = []
        for sheet in sheets:
            # Recorrer todas las filas
            for row in sheet._cell_values:
                if row != sheet._cell_values[0]:
                    # Obtener los valores de la fila actual
                    dict_record = {}
                    val_index = 0
                    none_values = []
                    # Recorrer los valores de la fila actual
                    for val in row:
                        # si la posicion del valor es menor o igual a la posicion de
                        # la ultima columna de las keys
                        if val_index <= last_index_keys:
                            # en caso de que no haya valor
                            if val == '':
                                none_values.append(True)
                            else:
                                none_values.append(False)

                            dict_record[keys[val_index]] = val
                            val_index = val_index + 1
                    # en caso de que haya un campo sin rellenar
                    if not (True in none_values):
                        values.append(dict_record)
        if not (values):
            raise odoo.exceptions.UserError('Verifique las hojas de su archivo excel, es probable que existan campos sin rellenar.')
        return values

    def _clear_xml_employee_income_wh(self):
        context = self._context or {}
        if context.get('islr_xml_wh_doc_id'):
            obj_ixwl = self.env('islr.xml.wh.line')
            unlink_ids = obj_ixwl.search(
                [('islr_xml_wh_doc', '=', context['islr_xml_wh_doc_id']),
                 ('type', '=', 'employee')])
            if unlink_ids:
                obj_ixwl.unlink( unlink_ids)
        return True

    def _get_xml_employee_income_wh(self, xml_list, file_type='csv'):
        def memoize(func):
            cache = {}

            @functools.wraps(func)
            def wrapper(*args):
                if args in cache:
                    return cache[args]
                result = func(*args)
                cache[args] = result
                return result
            return wrapper

        def get_concept_code(concept_code):
            concept_code_str = ''
            if type(concept_code) == float or type(concept_code) == int:
                if concept_code > 0 and concept_code <= 99:
                    concept_code_str = '00' + str(int(concept_code))
                elif concept_code > 9 and concept_code <= 99:
                    concept_code_str = '0' + str(int(concept_code))
                elif concept_code > 99 and concept_code <= 999:
                    concept_code_str = str(int(concept_code))
            elif type(concept_code_str) == str:
                concept_code_str = concept_code
            return concept_code_str

        @memoize
        def find_data(obj, field, operator, value):
            ids = obj.search( [(field, operator, value)])
            if len(ids) == 1:
                return ids[0]
            return False

        context = self._context or {}
        field_map = {'RIF Retenido': 'partner_vat',
                     'Número Factura': 'invoice_number',
                     'Número Control': 'control_number',
                     'Fecha Operación': 'date_ret',
                     'Codigo Concepto': 'concept_code',
                     'Monto Operación': 'base',
                     'Retención': 'porcent_rete'
                     }
        obj_pnr = self.env['res.partner']
        obj_irt = self.env['islr.rates']
        valid = []
        invalid = []
        item_num = 0
        #by each item we must check it
        for item in xml_list:
            item_num = item_num + 1
            data = {}
            #assign the "technical key's name" to value
            # data['base'] = 1
            for key, data_key in field_map.items():
                if key in item:
                    data[data_key] = item[key]
                else:
                    raise odoo.exceptions.UserError(f"Hay campos vacios, todos los campos deben estar llenos.")

            #if our concept_code is in float format
            data['concept_code'] = get_concept_code(data['concept_code'])
            #search employee by the rif
            pnr_id = find_data(obj_pnr, 'rif', '=', data.get('partner_vat'))
            #update partnet_id with id of the employee
            if pnr_id:
                data.update({'partner_id': pnr_id.id})
            # search islr_rate by the concept_code
            irt_id = find_data(obj_irt, 'code', '=', data.get('concept_code'))
            if irt_id:
                # search the record
                irt_brw = obj_irt.browse(irt_id.id)
                data.update({'concept_id': irt_brw.concept_id.id,
                             'rate_id': irt_id.id})

            date_ret = None
            if 'date_ret' in data:
                #if we have an excel file, it usually converted the date in float
                #so we need to put the date between single quotes in our excel file
                #but it's for csv files too
                if file_type == 'excel':
                    if not data['date_ret']:
                        raise UserError('Por favor indique la fecha.')
                    try:
                        date_ret = datetime.strptime(data['date_ret'], '%d/%m/%Y')
                    except:
                        date_ret = datetime.date.fromordinal(datetime.date(1900, 1, 1).toordinal() + int(float(data['date_ret'])) - 2)
                else:
                    try:
                        date_ret = time.strptime(data['date_ret'], '%d/%m/%Y')
                        date_ret = time.strftime('%Y-%m-%d', date_ret)
                    except Exception as err:
                        raise odoo.exceptions.UserError("Usted debe escribir la fecha en el siguiente formato 'd/m/Y' (dia/mes/año).")

            if 'base' in data:
                if type(data['base']) == str:
                    if data['base'] and data['base'] != '':
                        if '"' in data['base']:
                            data['base'] = data['base'].replace('"', '')
                        try:
                            if ',' in data['base']:
                                data['base'] = data['base'].replace(',', '.')
                            data['base'] = float(data['base'])
                        except Exception as err:
                            data['base'] = 0
                    else:
                        data['base'] = 0

            if 'porcent_rete' in data:
                if type(data['porcent_rete']) == str:
                    if data['porcent_rete'] != '':
                        if '"' in data['porcent_rete']:
                            data['porcent_rete'] = data['porcent_rete'].replace('"', '')
                        try:

                            if ',' in data['porcent_rete']:
                                data['porcent_rete'] = data['porcent_rete'].replace(',', '.')

                            data['porcent_rete'] = float(data['porcent_rete'])

                        except Exception as err:
                            data['porcent_rete'] = 0
                    else:
                        data['porcent_rete'] = 0

            wh = 0
            if ('base' and 'porcent_rete') in data:
                wh = (data['base'] * data['porcent_rete']) / 100

            if not pnr_id:
                raise UserError("Error! No existe un empleado con cedula de identidad: %s" %(data.get('partner_vat')))

            islr_line = self.env["islr.wh.doc.line"].create({
                "concept_id": data["concept_id"],
                "control_number": data["control_number"],
                "invoice_number": data["invoice_number"],
                "base_amount": data["base"],
                "retencion_islr": data["porcent_rete"],
                "amount": wh,
                "partner_id": pnr_id.id,
                "partner_vat": pnr_id.rif,
                "subtract": 0,
                "raw_tax_ut": wh,
            })

            data.update({
                'wh': wh,
                'date_ret': date_ret,
                'islr_xml_wh_doc': context.get('active_id'),
                "islr_wh_doc_line_id": islr_line.id,
                'type': 'employee',
            })

            if pnr_id and irt_id:
                valid.append(data)
            else:
                invalid.append(data)

        return valid, invalid

    def process_employee_income_wh(self):
        #Search the current record id
        eiw_brw = self.browse(self)[0].id
        #get binary of the file
        eiw_file = eiw_brw.obj_file
        invalid = []
        values = []
        #decode binary in bytes
        xml_file = base64.decodebytes(eiw_file)
        #parse file
        if eiw_brw.type == 'excel':
            values = self._parce_excel_employee_income_wh(xml_file)
        elif eiw_brw.type == 'csv':
            values = self._parse_csv_employee_income_wh(xml_file)
        obj_ixwl = self.env['islr.xml.wh.line']
        #if we have the values
        if values:
            self._clear_xml_employee_income_wh()
            #validation of the file
            valid, invalid = self._get_xml_employee_income_wh(values, eiw_brw.type)
            #create lines
            lines_created = []
            for data in valid:
                create = obj_ixwl.create(data)
                if create:
                    lines_created.append(create)

        #if we don't have the values or the file is invalid
        if not values or invalid:
            msg = _('No se encontraron empleados con la siguiente data:\n') if invalid else \
                _('Archivo vacio o invalido'
                  '(Tambien se debe verificar el RIF del empleado y el periodo establecido)')
            for item in invalid:
                msg += 'RIF Retenido: %s\n' % item['partner_vat']
            raise UserError("Error! \n %s" %(msg))
        islr_xml_wh_doc_active = self.env["islr.xml.wh.doc"].browse([self.env.context['active_id']])
        if islr_xml_wh_doc_active:
            islr_xml_wh_doc_active.employee_xml_ids = [(6,0, [line.id for line in lines_created])]
            islr_xml_wh_doc_active.action_generate_line_xml()
        return {'type': 'ir.actions.act_window_close'}

    name = fields.Char('Nombre del Archivo', size=128, readonly=True)
    type = fields.Selection([
            ('excel', 'Archivo Excel')
            ], string='Tipo de Archivo', required=True, default='excel')
    obj_file= fields.Binary('Archivo', required=True,
                                  help=("Excel file name with employee income "
                                        "withholding data"))

EmployeeIncomeWh()
