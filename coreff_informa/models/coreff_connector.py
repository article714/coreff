# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from zeep import Client
from odoo import api, models


class CoreffConnector(models.Model):
    _inherit = "coreff.connector"

    @api.model
    def informa_get_companies(self, arguments):
        """
        Get companies
        """
        settings = self.get_company_informa_settings(arguments["user_id"])
        client = Client(settings["url"])

        look_up_input = {}
        look_up_input["Country_Code"] = "ES"
        # if arguments["is_siret"]:
        #     look_up_input["DnB_DUNS_Number"] = arguments["value"]
        # else:
        look_up_input["Name"] = arguments["value"]

        look_up_request = {}
        look_up_request["UserId"] = settings["username"]
        look_up_request["Password"] = settings["password"]
        look_up_request["lookUpInput"] = look_up_input

        result = client.service.ws_LookUp(look_up_request)
        companies = result["CREDITMSGSRSV2"]["LOOKUPTRNRS"]["LOOKUPRS"][
            "LOOKUPRSCOMPANY"
        ]["ArrayOfLOOKUPRSCOMPANYItem"]
        companies.sort(key=lambda x: (x["NME"], x["NON_POST_TOWN"]))
        suggestions = []
        for company in companies:
            suggestion = {}
            suggestion["informa_company_id"] = company["DUNS_NBR"]
            suggestion["name"] = company["NME"]
            # suggestion["siret"] = company["DUNS_NBR"]
            suggestion["street"] = company["ADR_LINE"]
            suggestion["city"] = company["NON_POST_TOWN"]
            suggestion["zip"] = company["POST_CODE"]
            suggestion["phone"] = company["TLCM_NBR"]
            # suggestion["country_id"] = company["country"]
            suggestions.append(suggestion)
        return suggestions

    @api.model
    def informa_get_company(self, arguments):
        """
        Get company information
        """
        pass

    def get_company_informa_settings(self, user_id):
        """
        Get company settings for Informa
        """
        res = {}
        user = self.env["res.users"].browse(user_id)
        company = user.company_id
        res["url"] = company.get_parent_field("informa_url")
        res["username"] = company.get_parent_field("informa_username")
        res["password"] = company.get_parent_field("informa_password")
        return res
