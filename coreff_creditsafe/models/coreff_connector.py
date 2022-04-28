# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import json
import logging
from requests import Session
from odoo.tools.config import config
from odoo import api, models


class CustomSessionProxy(Session):
    def __init__(self):
        super().__init__()

        proxy_http = config.get("proxy_http")
        proxy_https = config.get("proxy_https")

        self.proxies = {
            "http": proxy_http,
            "https": proxy_https,
        }


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

        with CustomSessionProxy() as session:
            response = session.post(
                "{}/authenticate".format(url),
                data=json.dumps(data),
                headers=headers,
            )

            if response.status_code == 200:
                content = response.json()

                self.env["coreff.credentials"].update_token(
                    url, username, content["token"]
                )
                return content["token"]
            if response.status_code == 401:
                return False
            else:
                return self.format_error(response)

    @api.model
    def creditsafe_get_companies_criterias(self, arguments, retry=False):
        """
        Get companies criterias
        """
        settings = self.get_company_creditsafe_settings(arguments["user_id"])
        url = settings["url"]
        token = settings["token"]

        if url:
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": token if token else "",
            }

            call_url = "{}/companies/searchcriteria".format(url)

            code = False
            if arguments["country_id"]:
                code = (
                    self.env["res.country"]
                    .search([("id", "=", arguments["country_id"])])[0]
                    .code
                )
                call_url += "&countries={}".format(code)

            with CustomSessionProxy() as session:
                logging.info(call_url)
                logging.info(headers)
                response = session.get(call_url, headers=headers)

                if response.status_code == 200:
                    content = response.json()

                    def get_criterias(d):
                        c = []
                        for k in d:
                            if "required" in d[k]:
                                c.append(k)
                            else:
                                for i in get_criterias(d[k]):
                                    if i == "simpleValue":
                                        c.append(k)
                                    else:
                                        c.append(i)
                        return c

                    criterias = []
                    for i in content["criteriaSets"]:
                        criterias += get_criterias(i)

                    return criterias
                elif response.status_code in (401, 403):
                    if not retry:
                        res = self.creditsafe_authenticate(
                            settings["url"],
                            settings["username"],
                            settings["password"],
                        )
                        if res:
                            return self.creditsafe_get_companies_criterias(
                                arguments, True
                            )
                        else:
                            return self.format_error(response)
                    else:
                        return self.format_error(response)
                else:
                    return self.format_error(response)

    @api.model
    def creditsafe_get_companies(self, arguments, retry=False):
        """
        Get companies
        """
        settings = self.get_company_creditsafe_settings(arguments["user_id"])
        url = settings["url"]
        token = settings["token"]

        criterias = self.creditsafe_get_companies_criterias(arguments)
        logging.info(criterias)

        if url:
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": token if token else "",
            }

            call_url = "{}/companies?language=en&page=1&pageSize=200".format(
                url
            )
            if "status" in criterias:
                call_url += "&status=Active"

            if "regNo" in criterias and arguments["valueIsCompanyCode"]:
                call_url += "&regNo={}".format(arguments["value"])
            elif "name" in criterias:
                call_url += "&name={}".format(arguments["value"])

            if "countries" in criterias and arguments["country_id"]:
                code = (
                    self.env["res.country"]
                    .search([("id", "=", arguments["country_id"])])[0]
                    .code
                )
                call_url += "&countries={}".format(code)

            if "officeType" in criterias and arguments.get(
                "is_head_office", True
            ):
                call_url += "&officeType=headOffice"

            with CustomSessionProxy() as session:
                logging.info(call_url)
                response = session.get(call_url, headers=headers)

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
                        suggestion["creditsafe_company_id"] = company.get(
                            "id", ""
                        )
                        suggestion["name"] = company.get("name", "")
                        suggestion["coreff_company_code"] = company.get(
                            "regNo", ""
                        )
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
                        suggestion["vat"] = company.get("vatNo", [""])[0]
                        suggestion["phone"] = company.get(
                            "phoneNumbers", [""]
                        )[0]
                        suggestions.append(suggestion)
                    return suggestions
                elif response.status_code in (401, 403):
                    if not retry:
                        res = self.creditsafe_authenticate(
                            settings["url"],
                            settings["username"],
                            settings["password"],
                        )
                        if res:
                            return self.creditsafe_get_companies(
                                arguments, True
                            )
                        else:
                            return self.format_error(response)
                    else:
                        return self.format_error(response)
                else:
                    return self.format_error(response)

    @api.model
    def creditsafe_get_company(self, arguments, retry=False):
        """
        Get company information
        """
        settings = self.get_company_creditsafe_settings(arguments["user_id"])
        url = settings["url"]
        token = settings["token"]

        if url:
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": token if token else "",
            }

            call_url = "{}/companies/{}?language={}".format(
                url, arguments["company_id"], settings["language"]
            )

            with CustomSessionProxy() as session:
                response = session.get(call_url, headers=headers)

                if response.status_code == 200:
                    content = response.json()
                    return content
                elif response.status_code in (401, 403):
                    if not retry:
                        res = self.creditsafe_authenticate(
                            settings["url"],
                            settings["username"],
                            settings["password"],
                        )
                        if res:
                            return self.creditsafe_get_company(arguments, True)
                        else:
                            return self.format_error(response)
                    else:
                        return self.format_error(response)
                else:
                    return self.format_error(response)

    def get_company_creditsafe_settings(self, user_id):
        """
        Get company settings for CreditSafe
        """
        res = {}
        user = self.env["res.users"].browse(user_id)
        company = user.company_id
        res["url"] = company.get_parent_creditsafe_field("creditsafe_url")
        res["username"] = company.get_parent_creditsafe_field(
            "creditsafe_username"
        )
        res["password"] = company.get_parent_creditsafe_field(
            "creditsafe_password"
        )
        res["language"] = company.get_parent_creditsafe_field(
            "creditsafe_language"
        )
        res["token"] = (
            self.env["coreff.credentials"]
            .get_credentials(res["url"], res["username"])
            .token
        )
        return res

    def format_error(self, response):
        """
        Format api response
        """
        res = {}
        res["title"] = "[{}] : {}".format(
            response.status_code, response.reason
        )
        res["body"] = response.content
        return {"error": res}
