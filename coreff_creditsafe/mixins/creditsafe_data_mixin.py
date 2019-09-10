# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields


class CreditSafeDataMixin(object):
    """
    Fields for creditsafe informations
    """

    creditsafe_company_id = fields.Char(string="Creditsafe id")

    # Identification
    creditsafe_company_name = fields.Char(string="Business Name")
    creditsafe_legal_form = fields.Char(string="Legal Form")
    creditsafe_court_registry_number = fields.Char(string="RCS Number")
    creditsafe_court_registry_description = fields.Char(string="RCS")
    creditsafe_incorporation_date = fields.Char(string="Registration Date")
    creditsafe_activity_code = fields.Char(string="Activity Code")
    creditsafe_activity_description = fields.Char(
        string="Activity Description"
    )
    creditsafe_country = fields.Char(string="Country")

    # Notations
    creditsafe_status = fields.Char(string="Status")
    creditsafe_rating = fields.Char(string="Rating")
    creditsafe_rating_short = fields.Char(string="Rating / Short Precision")
    creditsafe_rating_long = fields.Char(string="Rating / Long Precision")
    creditsafe_credit_limit = fields.Char(string="Credit Limit")

    # Judgements
    creditsafe_last_judgement_date = fields.Char(string="Last Judgement")
    creditsafe_last_ccj_date = fields.Char(string="")
    creditsafe_number_of_directors = fields.Char(string="Number of Directors")

    creditsafe_last_update = fields.Datetime(
        readonly=True, string="Last Update"
    )

    def update_creditsafe_data(self):
        """
        Update financial information
        """

        for rec in self:
            company = self.env["creditsafe.api"].get_company(
                rec.creditsafe_company_id
            )
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
