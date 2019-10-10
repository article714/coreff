# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
import logging


class CreditSafeDataMixin(object):
    """
    Fields for creditsafe informations
    """

    creditsafe_visibility = fields.Boolean(
        compute="_compute_creditsafe_visibility",
        default=lambda rec: rec._default_creditsafe_visibility(),
    )

    creditsafe_company_id = fields.Char(string="Creditsafe id")

    # Identification
    creditsafe_company_name = fields.Char(
        string="Business Name", readonly=True
    )
    creditsafe_legal_form = fields.Char(string="Legal Form", readonly=True)
    creditsafe_court_registry_number = fields.Char(
        string="RCS Number", readonly=True
    )
    creditsafe_court_registry_description = fields.Char(
        string="RCS", readonly=True
    )
    creditsafe_incorporation_date = fields.Char(
        string="Registration Date", readonly=True
    )
    creditsafe_activity_code = fields.Char(
        string="Activity Code", readonly=True
    )
    creditsafe_activity_description = fields.Char(
        string="Activity Description", readonly=True
    )
    creditsafe_country = fields.Char(string="Country", readonly=True)

    # Notations
    creditsafe_status = fields.Char(string="Status", readonly=True)
    creditsafe_rating = fields.Char(string="Rating", readonly=True)
    creditsafe_rating_short = fields.Char(
        string="Rating / Short Precision", readonly=True
    )
    creditsafe_rating_long = fields.Char(
        string="Rating / Long Precision", readonly=True
    )
    creditsafe_credit_limit = fields.Char(string="Credit Limit", readonly=True)

    # Judgements
    creditsafe_last_judgement_date = fields.Char(
        string="Last Judgement", readonly=True
    )
    creditsafe_last_ccj_date = fields.Char(string="", readonly=True)
    creditsafe_number_of_directors = fields.Char(
        string="Number of Directors", readonly=True
    )

    creditsafe_last_update = fields.Datetime(
        readonly=True, string="Last Update"
    )

    def _compute_creditsafe_visibility(self):
        company = self.env.user.company_id
        for rec in self:
            if company.coreff_connector_id == self.env.ref(
                "coreff_creditsafe.coreff_connector_creditsafe_api"
            ):
                rec.creditsafe_visibility = True
            else:
                rec.creditsafe_visibility = False

    def _default_creditsafe_visibility(self):
        company = self.env.user.company_id
        if company.coreff_connector_id == self.env.ref(
            "coreff_creditsafe.coreff_connector_creditsafe_api"
        ):
            return True
        else:
            return False

    def update_creditsafe_data(self):
        """
        Update financial information
        """

        for rec in self:
            arguments = {}
            arguments["company_id"] = rec.creditsafe_company_id
            arguments["user_id"] = self.env.user.id
            company = self.env["coreff.api"].get_company(arguments)
            company = company.get("report", {})
            company_summary = company.get("companySummary", {})
            basic_information = company.get("companyIdentification", {}).get(
                "basicInformation", {}
            )
            credit_score = company.get("creditScore", {})

            rec.creditsafe_company_name = company_summary.get(
                "businessName", ""
            )
            rec.creditsafe_legal_form = basic_information.get(
                "legalForm", {}
            ).get("description", "")
            rec.creditsafe_court_registry_number = basic_information.get(
                "companyRegistrationNumber", ""
            )
            rec.creditsafe_court_registry_description = basic_information.get(
                "commercialCourt", ""
            )
            rec.creditsafe_incorporation_date = basic_information.get(
                "companyRegistrationDate", ""
            )
            rec.creditsafe_activity_code = basic_information.get(
                "principalActivity", {}
            ).get("code", "")
            rec.creditsafe_activity_description = basic_information.get(
                "principalActivity", {}
            ).get("description", "")
            rec.creditsafe_country = basic_information.get("country", "")

            rec.creditsafe_status = basic_information.get(
                "companyStatus", {}
            ).get("status", "")
            rec.creditsafe_rating = (
                credit_score.get("currentCreditRating", {})
                .get("providerValue", {})
                .get("maxValue", "")
            )
            rec.creditsafe_rating_short = credit_score.get(
                "currentCreditRating", {}
            ).get("commonDescription", "")
            rec.creditsafe_rating_long = credit_score.get(
                "currentCreditRating", {}
            ).get("providerDescription", "")
            rec.creditsafe_credit_limit = (
                credit_score.get("currentCreditRating", {})
                .get("creditLimit", {})
                .get("value", "")
            )

            rec.creditsafe_last_judgement_date = credit_score.get(
                "latestRatingChangeDate", ""
            )
            # rec.creditsafe_last_ccj_date = company[""][""]
            rec.creditsafe_number_of_directors = len(
                company.get("directors", {}).get("currentDirectors", {})
            )

            rec.creditsafe_last_update = fields.Datetime.now()
