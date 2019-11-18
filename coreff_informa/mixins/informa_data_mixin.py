# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields


class InformaDataMixin(object):
    """
    Fields for informa informations
    """

    informa_visibility = fields.Boolean(
        compute="_compute_informa_visibility",
        default=lambda rec: rec._default_informa_visibility(),
        store=True,
    )

    informa_company_id = fields.Char(string="Informa id")

    # Identification
    informa_company_name = fields.Char(string="Business Name", readonly=True)
    informa_legal_form = fields.Char(string="Legal Form", readonly=True)
    informa_court_registry_number = fields.Char(
        string="RCS Number", readonly=True
    )
    informa_court_registry_description = fields.Char(
        string="RCS", readonly=True
    )
    informa_incorporation_date = fields.Char(
        string="Registration Date", readonly=True
    )
    informa_activity_code = fields.Char(string="Activity Code", readonly=True)
    informa_activity_description = fields.Char(
        string="Activity Description", readonly=True
    )
    informa_country = fields.Char(string="Country", readonly=True)

    # Notations
    informa_status = fields.Char(string="Status", readonly=True)
    informa_rating = fields.Char(string="Rating", readonly=True)
    informa_rating_short = fields.Char(
        string="Rating / Short Precision", readonly=True
    )
    informa_rating_long = fields.Char(
        string="Rating / Long Precision", readonly=True
    )
    informa_credit_limit = fields.Char(string="Credit Limit", readonly=True)

    # Judgements
    informa_last_judgement_date = fields.Char(
        string="Last Judgement", readonly=True
    )
    informa_last_ccj_date = fields.Char(string="", readonly=True)
    informa_number_of_directors = fields.Char(
        string="Number of Directors", readonly=True
    )

    informa_last_update = fields.Datetime(readonly=True, string="Last Update")

    def _compute_informa_visibility(self):
        company = self.env.user.company_id
        for rec in self:
            if company.coreff_connector_id == self.env.ref(
                "coreff_informa.coreff_connector_informa_api"
            ):
                rec.informa_visibility = True
            else:
                rec.informa_visibility = False

    def _default_informa_visibility(self):
        company = self.env.user.company_id
        if company.coreff_connector_id == self.env.ref(
            "coreff_informa.coreff_connector_informa_api"
        ):
            return True
        else:
            return False

    def update_informa_data(self):
        """
        Update financial information
        """

        for rec in self:
            arguments = {}
            arguments["company_id"] = rec.informa_company_id
            arguments["user_id"] = self.env.user.id
            company = self.env["coreff.api"].get_company(arguments)
            company = company.get("report", {})
            company_summary = company.get("companySummary", {})
            basic_information = company.get("companyIdentification", {}).get(
                "basicInformation", {}
            )
            credit_score = company.get("creditScore", {})

            rec.informa_company_name = company_summary.get("businessName", "")
            rec.informa_legal_form = basic_information.get(
                "legalForm", {}
            ).get("description", "")
            rec.informa_court_registry_number = basic_information.get(
                "companyRegistrationNumber", ""
            )
            rec.informa_court_registry_description = basic_information.get(
                "commercialCourt", ""
            )
            rec.informa_incorporation_date = basic_information.get(
                "companyRegistrationDate", ""
            )
            rec.informa_activity_code = basic_information.get(
                "principalActivity", {}
            ).get("code", "")
            rec.informa_activity_description = basic_information.get(
                "principalActivity", {}
            ).get("description", "")
            rec.informa_country = basic_information.get("country", "")

            rec.informa_status = basic_information.get(
                "companyStatus", {}
            ).get("status", "")
            rec.informa_rating = (
                credit_score.get("currentCreditRating", {})
                .get("providerValue", {})
                .get("maxValue", "")
            )
            rec.informa_rating_short = credit_score.get(
                "currentCreditRating", {}
            ).get("commonDescription", "")
            rec.informa_rating_long = credit_score.get(
                "currentCreditRating", {}
            ).get("providerDescription", "")
            rec.informa_credit_limit = (
                credit_score.get("currentCreditRating", {})
                .get("creditLimit", {})
                .get("value", "")
            )

            rec.informa_last_judgement_date = credit_score.get(
                "latestRatingChangeDate", ""
            )
            # rec.informa_last_ccj_date = company[""][""]
            rec.informa_number_of_directors = len(
                company.get("directors", {}).get("currentDirectors", {})
            )

            rec.informa_last_update = fields.Datetime.now()
