# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import json
import requests
from odoo import api, models

LOGGER = logging.getLogger(__name__)


class CreditSafeApi(models.Model):
    """
    API for CreditSafe service
    """

    _name = "creditsafe.api"
    _description = "CreditSafe API"

    @api.model
    def authenticate(self):
        """
        Auto authent to access CreditSafe
        """
        params = self.env["ir.config_parameter"].sudo()
        username = params.get_param("coreff_creditsafe.creditsafe_username")
        password = params.get_param("coreff_creditsafe.creditsafe_password")
        url = params.get_param("coreff_creditsafe.creditsafe_url")

        if username and password and url:
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
            }

            data = {"username": username, "password": password}

            response = requests.post(
                "{}/authenticate".format(url),
                data=json.dumps(data),
                headers=headers,
            )

            if response.status_code == 200:
                content = response.json()
                params.set_param(
                    "coreff_creditsafe.creditsafe_token", content["token"]
                )
            else:
                raise Exception(response)

    @api.model
    def get_companies(self, countries, language, is_siret, value):
        """
        Get companies
        """
        params = self.env["ir.config_parameter"].sudo()
        creditsafe_url = params.get_param("coreff_creditsafe.creditsafe_url")
        creditsafe_token = params.get_param(
            "coreff_creditsafe.creditsafe_token"
        )

        if creditsafe_url and creditsafe_token:
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": creditsafe_token,
            }

            call_url = "{}/companies?countries={}&language={}&page=1&pageSize=200".format(
                creditsafe_url, countries, language
            )

            if is_siret:
                call_url += "&regNo={}".format(value)
            else:
                call_url += "&name={}".format(value)

            response = requests.get(call_url, headers=headers)

            if response.status_code == 200:
                content = response.json()
                content["companies"].sort(
                    key=lambda x: (
                        x.get("name"),
                        x.get("address", {}).get("city", ""),
                    )
                )

                suggestions = []
                for company in content.get("companies", {}):
                    suggestion = {}
                    suggestion["creditsafe_company_id"] = company.get("id", "")
                    suggestion["name"] = company.get("name", "")
                    suggestion["siret"] = company.get("regNo", "")
                    suggestion["street"] = company.get("address", {}).get(
                        "street", ""
                    )
                    suggestion["city"] = company.get("address", {}).get(
                        "city", ""
                    )
                    suggestion["zip"] = company.get("address", {}).get(
                        "postCode", ""
                    )
                    suggestion["country_id"] = company.get("country", "")
                    suggestions.append(suggestion)

                return suggestions
            else:
                raise Exception(response)

    @api.model
    def get_company(self, company_id):
        """
        Get company information
        """
        params = self.env["ir.config_parameter"].sudo()
        creditsafe_url = params.get_param("coreff_creditsafe.creditsafe_url")
        creditsafe_token = params.get_param(
            "coreff_creditsafe.creditsafe_token"
        )

        if creditsafe_url and creditsafe_token:
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": creditsafe_token,
            }

            call_url = "{}/companies/{}".format(creditsafe_url, company_id)

            response = requests.get(call_url, headers=headers)

            if response.status_code == 200:
                content = response.json()
                return content
            else:
                raise Exception(response)
