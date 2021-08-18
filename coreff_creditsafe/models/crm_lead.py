# ©2021 - Chris Mann (Open User Systems)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo import _
import datetime
import urllib.parse

class CrmLead(models.Model):
    """
    Fields for creditsafe informations
    """
    _inherit = "crm.lead"

    def creditsafe_lookup(self):
        company_name = urllib.parse.quote(self.partner_name)
        creditsafe_url = "https://app.creditsafeuk.com/CSUKLive/webpages/CompanySearch/SearchResults.aspx"
        creditsafe_params = f"?CompanyName={company_name}&IsAdvancedSearch=True&CompanyType=Limited%2c+NonLimited&PageSize=10"

        action = {
            "type"     : "ir.actions.act_url",
            "target"   : "new",
            "url"      : creditsafe_url + creditsafe_params
        }
        return action