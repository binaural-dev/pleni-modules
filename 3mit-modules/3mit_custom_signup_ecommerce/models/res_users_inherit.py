# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import UserError


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    @staticmethod
    def check_missing_values(company_type, values):
        missing = ''
        if company_type == 'person':
            if 'nationality' not in values:
                missing += 'Nationality, '
            if 'identification_id' not in values:
                missing += 'Identification, '
            if 'people_type_individual' not in values:
                missing += 'People Type Individual, '

        if company_type == 'company:':
            if 'rif' not in values:
                missing += 'RIF, '
            if 'people_type_company' not in values:
                missing += 'People Type Company, '
            if 'commercial_name' not in values:
                missing += 'Commercial Name, '

        if 'name' not in values:
            missing += 'Name, '
        if 'mobile' not in values:
            missing += 'Telephone, '
        if 'country_id' not in values:
            missing += 'Country, '
        if 'street' not in values:
            missing += 'Street, '
        if 'street2' not in values:
            missing += 'Street 2, '
        if 'city' not in values:
            missing += 'City, '
        if 'state_id' not in values:
            missing += 'State, '
        if 'municipality_id' not in values:
            missing += 'Municipality, '
        if 'parish_id' not in values:
            missing += 'Parish, '
        if 'zip' not in values:
            missing += 'Zip, '

        if missing != '':
            missing = missing[:len(missing) - 2]
        return missing

    @api.model
    def signup(self, values, token=None):
        """ signup a user, to either:
            - create a new user (no token), or
            - create a user for a partner (with token, but no user for partner), or
            - change the password of a user (with token, and existing user).
            :param values: a dictionary with field values that are written on user
            :param token: signup token (optional)
            :return: (dbname, login, password) for the signed up user
        """

        if (values.get('nationality')):
            original_values = {
                'login': values.get('login'),
                'name': values.get('name'),
                'password': values.get('password'),
                'mobile': values.get('mobile'),
                'country_id': 238,
            }

        if token:
            # signup with a token: find the corresponding partner id
            partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
            # invalidate signup token
            partner.write({'signup_token': False, 'signup_type': False, 'signup_expiration': False})

            partner_user = partner.user_ids and partner.user_ids[0] or False

            # avoid overwriting existing (presumably correct) values with geolocation data
            if partner.country_id or partner.zip or partner.city:
                values.pop('city', None)
                values.pop('country_id', None)
            if partner.lang:
                values.pop('lang', None)

            if partner_user:
                # user exists, modify it according to values
                values.pop('login', None)
                values.pop('name', None)

                if (values.get('nationality')):
                    original_values = {
                        'password': values.get('password'),
                    }
                    partner_user.write(original_values)
                else:
                    partner_user.write(values)
                if not partner_user.login_date:
                    partner_user._notify_inviter()


                if (values.get('nationality')):
                    return (self.env.cr.dbname, partner_user.login, original_values.get('password'))
                else:
                    return (self.env.cr.dbname, partner_user.login, values.get('password'))
            else:
                # user does not exist: sign up invited user
                values.update({
                    'name': partner.name,
                    'partner_id': partner.id,
                    'email': values.get('email') or values.get('login'),
                })
                if partner.company_id:
                    values['company_id'] = partner.company_id.id
                    values['company_ids'] = [(6, 0, [partner.company_id.id])]

                    if (values.get('nationality')):
                        original_values = {
                            'login': values.get('login'),
                            'name': values.get('name'),
                            'password': values.get('password'),
                            'mobile': values.get('mobile'),
                            'country_id': 238,
                        }
                        partner_user = self._signup_create_user(original_values)
                    else:
                        partner_user = self._signup_create_user(values)
                partner_user._notify_inviter()
        else:
            # no token, sign up an external user
            values['email'] = values.get('email') or values.get('login')

            if (not values.get('nationality')):
                self._signup_create_user(values)
                return (self.env.cr.dbname, values.get('login'), values.get('password'))

            new_user = self._signup_create_user(original_values)
            if new_user.partner_id:
                missing_values = self.check_missing_values(values.get('company_type'), values)
                if missing_values != '':
                    raise UserError(f'Missing some fields for the user creation: {missing_values}.')

                if values.get('company_type') == 'person':
                    people_type_individual = values.get('people_type_individual')
                    nationality = values.get('nationality')
                    identification_id = values.get('identification_id')
                    identification_id_nationality = nationality+'-'+identification_id
                    people_type_company = False
                    rif = False
                    rif_separable = False
                    commercial_name = False

                else:
                    people_type_individual = False
                    nationality = False
                    identification_id = False
                    identification_id_nationality = False
                    people_type_company = values.get('people_type_company')
                    commercial_name = values.get('commercial_name')
                    rif = values.get('rif')
                    rif_separable = False
                    if len(rif.split('-')) > 1:
                        rif_separable = True
                        rif_type = rif.split('-')[0]
                        identification_rif = rif.split('-')[1]

                new_user.partner_id.write({
                    'company_type': values.get('company_type'),
                    'email': values.get('login'),
                    'lang': 'es_VE',
                    'people_type_company': people_type_company,
                    'people_type_individual': people_type_individual,
                    'country_id': 238,
                    'nationality': nationality,
                    'document_type': nationality,
                    'identification_id': identification_id_nationality,
                    'identification_document': identification_id,
                    'rif': rif,
                    'rif_type': rif_type if rif_separable else None,
                    'identification_rif': identification_rif if rif_separable else None,
                    'mobile': values.get('mobile'),
                    'state_id': int(values.get('state_id')),
                    'municipality_id': int(values.get('municipality_id')),
                    'parish_id': int(values.get('parish_id')),
                    'street': values.get('street'),
                    'street2': values.get('street2'),
                    'city': values.get('city'),
                    'zip': values.get('zip'),
                    'ref_point': values.get('ref_point'),
                    'dispatcher_instructions': values.get('dispatcher_instructions'),
                    'commercial_name': commercial_name
                })
        return self.env.cr.dbname, values.get('login'), values.get('password')
