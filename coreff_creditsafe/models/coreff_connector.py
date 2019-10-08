# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
import requests
from odoo import api, models


class CoreffConnector(models.Model):
    _inherit = "coreff.connector"

    @api.model
    def creditsafe_authenticate(self, url, username, password):
        """
        Auto authent to access CreditSafe
        """
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

            self.env["coreff.credentials"].update_token(content["token"])
            return content["token"]
        if response.status_code == 401:
            return False
        else:
            raise Exception(response)

    @api.model
    def creditsafe_get_companies(
        self, countries, language, is_siret, value, retry=False
    ):
        """
        Get companies
        """
        settings = self.get_company_settings()
        url = settings["url"]
        token = settings["token"]

        if url and token:
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": token,
            }

            call_url = "{}/companies?countries={}&language={}&page=1&pageSize=200".format(
                url, countries, language
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
            elif response.status_code == 403:
                if not retry:
                    res = self.creditsafe_authenticate(
                        settings["url"],
                        settings["username"],
                        settings["password"],
                    )
                    if res:
                        self.creditsafe_get_companies(
                            countries, language, is_siret, value, True
                        )
                else:
                    raise Exception(response)
            else:
                raise Exception(response)

    @api.model
    def creditsafe_get_company(self, company_id, retry=False):
        """
        Get company information
        """
        settings = self.get_company_settings()
        url = settings["url"]
        token = settings["token"]

        if url and token:
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": token,
            }

            call_url = "{}/companies/{}".format(url, company_id)

            response = requests.get(call_url, headers=headers)

            if response.status_code == 200:
                content = response.json()
                return content
            elif response.status_code == 403:
                if not retry:
                    res = self.creditsafe_authenticate(
                        settings["url"],
                        settings["username"],
                        settings["password"],
                    )
                    if res:
                        self.creditsafe_get_company(company_id, True)
                else:
                    raise Exception(response)
            else:
                raise Exception(response)

    def get_company_settings(self):
        res = {}
        company = self.env.user.company_id
        res["url"] = company.get_parent_field("creditsafe_url")
        res["username"] = company.get_parent_field("creditsafe_username")
        res["password"] = company.get_parent_field("creditsafe_password")
        res["token"] = self.env["coreff.credentials"].get_token(
            res["url"], res["username"]
        )
        return res
