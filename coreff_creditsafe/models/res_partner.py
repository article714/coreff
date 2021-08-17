# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo import _
import datetime

class ResPartner(models.Model):
    """
    Fields for creditsafe informations
    """
    _inherit = "res.partner"

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
    creditsafe_share_capital = fields.Float(
        string="Share Capital", readonly=True
    )
    creditsafe_latest_turnover = fields.Float(
        string="Latest Turnover", readonly=True
    )
    creditsafe_incorporation_date = fields.Datetime(
        string="Registration Date", readonly=True
    )
    creditsafe_activity_code = fields.Char(
        string="Activity Code", readonly=True
    )
    creditsafe_activity_description = fields.Char(
        string="Activity Description", readonly=True
    )
    #CHRIS MANN: Add field for mainActivity classification
    creditsafe_activity_classification = fields.Char(
        string="Activity Classification", readonly=True
    )
    creditsafe_country = fields.Char(string="CreditSafe Country", readonly=True)

    # Notations
    creditsafe_status = fields.Char(string="Company Status", readonly=True)
    creditsafe_rating = fields.Integer(string="Rating", readonly=True)
    creditsafe_rating_short = fields.Char(
        string="Rating / Short Precision", readonly=True
    )
    creditsafe_rating_long = fields.Char(
        string="Rating / Long Precision", readonly=True
    )
    creditsafe_credit_limit = fields.Integer(string="CreditSafe Credit Limit", readonly=True)
    creditsafe_contract_limit = fields.Integer(string="CreditSafe Contract Limit", readonly=True)

    # Judgements
    creditsafe_last_change_date = fields.Datetime(
        string="Status Change Date", readonly=True
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
            formattedDatetime = datetime.datetime.strptime(basic_information.get("companyRegistrationDate", ""),"%Y-%m-%dT%H:%M:%SZ")
            rec.creditsafe_incorporation_date = formattedDatetime
            #rec.creditsafe_activity_code = basic_information.get(
            #    "principalActivity", {}
            #).get("code", "")
            #rec.creditsafe_activity_description = basic_information.get(
            #    "principalActivity", {}
            #).get("description", "")
            #CHRIS MANN: Get companySummary>mainActivity>code,description,classification
            rec.creditsafe_activity_code = company_summary.get(
                "mainActivity", {}
            ).get("code", "")
            rec.creditsafe_activity_description = company_summary.get(
                "mainActivity", {}
            ).get("description", "")
            rec.creditsafe_activity_classification = company_summary.get(
                "mainActivity", {}
            ).get("classification", "")
            #CHRIS MANN: Get website and store on partner record
            websites = company.get(
                "contactInformation", {}
            ).get("websites", {})
            if len(websites) > 0: rec.website = websites[0]

            rec.creditsafe_country = basic_information.get("country", "")

            rec.creditsafe_status = basic_information.get(
                "companyStatus", {}
            ).get("status", "")
            rec.creditsafe_rating = (
                credit_score.get("currentCreditRating", {})
                .get("providerValue", {})
                .get("value", 0)
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
                .get("value", 0)
            )
            rec.creditsafe_contract_limit = (
                credit_score.get("currentContractLimit", {})
                .get("value", 0)
            )

            #CHRIS MANN: Format string to datetime to store in Odoo field
            formattedDatetime = datetime.datetime.strptime(credit_score.get("latestRatingChangeDate", ""),"%Y-%m-%dT%H:%M:%SZ")
            rec.creditsafe_last_change_date = formattedDatetime
            # rec.creditsafe_last_ccj_date = company[""][""]
            rec.creditsafe_number_of_directors = len(
                company.get("directors", {}).get("currentDirectors", {})
            )
            rec.creditsafe_last_update = fields.Datetime.now()
            rec.creditsafe_share_capital = (
                company.get("shareCapitalStructure", {})
                .get("issuedShareCapital", {})
                .get("value", 0)
            )
            #CHRIS MANN: Add latestTurnoverFigure field from companySummary
            rec.creditsafe_latest_turnover = (
                company_summary.get("latestTurnoverFigure", {})
                .get("value", 0)
            )

    def retrieve_directors_data(self):
        """
        Retrieve directors contact data for company and store
        """
        for rec in self:
            arguments = {}
            arguments["company_id"] = rec.creditsafe_company_id
            arguments["user_id"] = self.env.user.id
            company = self.env["coreff.api"].get_company(arguments)
            company = company.get("report", {})
            directors = company.get("directors", {}).get(
                "currentDirectors", {}
            )
            #For each director, iterate through retrieving record
            #Next do a check for duplicates and if none present,
            #store the record as a new contact linked to this company.
            for director in directors:
                self.get_director(director)

    def get_director(self,director):
        #Search for any duplicate contacts before taking action - Match name and postcode
        result = self.env["res.partner"].search([
            ("name","ilike",director.get("firstName", "") + " " + director.get("surname", "")),
            ("zip","ilike",director.get("postalCode", "")
        )])
        if len(result)==0:
            #Mappings for directors to Odoo res.partner
            position = director.get("positions", {})[0].get("positionName", "")
            address = director.get("address", {})
            self.env["res.partner"].create({
                "name": director.get("firstName", "") + " " + director.get("surname", ""),
                "zip": director.get("postalCode", ""),
                "parent_id": self.id,
                "company_type": "person",
                "function": position,
                "ref": director.get("id", ""),
                "street": address.get("street", ""),
                "city": address.get("city", ""),
                "zip": address.get("postalCode", ""),
                "phone": address.get("telephone", ""),
                "type": "other",
                "title": self.get_title(director.get("title", "")),
                "state_id": self.get_state(address.get("province", "")),
                "country_id": self.get_country(address.get("country", "")),
                })
            return True
        else:
            raise UserError(_("Duplicate contact with same post/zipcode already detected for {}"
                              .format(director.get("firstName", "") + " " + director.get("surname", ""))))

    def get_title(self,title):
        #Search for res.partner.title that matches the submitted string with a dot added
        if len(title) > 0:
            result = self.env["res.partner.title"].search([("shortcut","ilike",title + ".")])
            return result.id
        else:
            return False

    def get_state(self,state):
        #Search for res.country that matches the submitted string
        if len(state) > 0:
            result = self.env["res.country.state"].search([("name","=",state)])
            return result.id
        else:
            return False

    def get_country(self,country_code):
        #Search for res.country.state that matches the submitted string
        #If no match found, use country of parent company
        if len(country_code) > 0:
            result = self.env["res.country"].search([("code","=",country_code)])
            return result.id
        else:
            return self.country_id.id
