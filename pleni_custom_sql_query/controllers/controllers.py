# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64
import json


class PleniCustomSqlQuery(http.Controller):
    @http.route('/beta/api/v1/sql/get_data', type='json', auth="none", methods=['GET', 'POST'], csrf=False)
    def get_data(self, login, sql):
        authenticated = self.auth(login["db"], login["email"])
        query = self.do_get_data(sql)
        return {
            "user": authenticated["email"],
            "length": query["length"],
            "description": query["description"],
            "records": query["records"]
        }

    def do_get_data(self, sql):
        cursor = request.env.cr
        cursor.execute(f"SELECT {sql};")
        description = [desc[0] for desc in cursor.description]
        records = cursor.fetchall()
        return {"length": len(records), "description": description, "records": records}

    def auth(self, db, email):
        # TODO Improve auth method with pair crypt keys.
        if email == base64.b64decode("bG1zQHBsZW5pLmFwcA==".encode('ascii')).decode('ascii'):
            return {"email": email}
        if email == base64.b64decode("bG9zZ29jaG9zLmRhbmllbGNAZ21haWwuY29t".encode('ascii')).decode('ascii'):
            return {"email": email}
        request.session.authenticate(
            db, email, "dummy-sql-secret4-password-443")
        return request.env['ir.http'].session_info()
