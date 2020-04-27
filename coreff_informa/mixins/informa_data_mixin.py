# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import datetime
from odoo import fields


class InformaDataMixin(object):
    """
    Fields for informa informations
    """

    informa_visibility = fields.Boolean(
        compute="_compute_informa_visibility",
        default=lambda rec: rec._default_informa_visibility(),
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda rec: rec.env["res.currency"].search(
            [("name", "=", "EUR")]
        ),
        readonly=True,
    )

    informa_company_id = fields.Char(string="Informa id")

    informa_out_bus_ind = fields.Char(
        string="Business Termination Indicator", readonly=True
    )
    informa_tot_empl = fields.Integer(string="Total Employees", readonly=True)
    informa_incn_yr = fields.Integer(string="Constitution Year", readonly=True)
    informa_finl_embt_ind = fields.Char(
        string="Bankruptcy Indicator / Payment Suspension", readonly=True
    )
    informa_dnb_ratg = fields.Char(string="D&B® Rating", readonly=True)
    informa_max_cr = fields.Char(
        string="Maximum Recommended Credit Guide", readonly=True
    )
    informa_pnt_nme = fields.Char(string="Parent Company", readonly=True)
    informa_pnt_duns = fields.Char(
        string="D-U-N-S® D&B® Matrix", readonly=True
    )
    informa_stmt_dt = fields.Date(string="Balance Date", readonly=True)
    informa_stmt_crcy_cd = fields.Char(
        string=" Balance Currency Code (latest figures available)",
        readonly=True,
    )
    informa_cash_liq_aset = fields.Float(
        string="Treasury and Liquid Assets (latest figures available)",
        readonly=True,
    )
    informa_tot_curr_aset = fields.Float(
        string="Current Assets (latest figures available)", readonly=True
    )
    informa_tot_aset = fields.Float(
        string="Total Assets (latest figures available)", readonly=True
    )
    informa_tot_curr_liab = fields.Float(
        string="Total Current Liabilities (latest figures available)",
        readonly=True,
    )
    informa_tot_liab = fields.Float(
        string="Total Liabilities (latest figures available)", readonly=True
    )
    informa_net_wrth = fields.Float(string="Net Worth", readonly=True)
    informa_stmt_from_dt = fields.Date(
        string="Exercise Start Date", readonly=True
    )
    informa_stmt_to_dt = fields.Date(
        string="Exercise Closing Date", readonly=True
    )
    informa_sls = fields.Float(string="Sales", readonly=True)
    informa_net_incm = fields.Float(
        string="Net Benefits (latest figures available)", readonly=True
    )
    informa_qk_rato = fields.Char(string="Liquidity Ratio", readonly=True)
    informa_curr_rato = fields.Char(string="Solvency Ratio", readonly=True)
    informa_prev_net_wrth = fields.Float(
        string="Previous Net Equity", readonly=True
    )
    informa_prev_sls = fields.Float(string="Previous Sales", readonly=True)
    informa_prev_stmt_dt = fields.Date(
        string="Previous Balance Date", readonly=True
    )
    informa_pnt_ctry_cd = fields.Char(
        string="Parent Company Country", readonly=True
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

            if company:
                rec.informa_out_bus_ind = company["OUT_BUS_IND"]
                rec.informa_tot_empl = company["TOT_EMPL"]
                rec.informa_incn_yr = company["INCN_YR"]
                rec.informa_finl_embt_ind = company["FINL_EMBT_IND"]
                rec.informa_dnb_ratg = company["DNB_RATG"]
                rec.informa_max_cr = company["MAX_CR"]
                rec.informa_pnt_nme = company["PNT_NME"]
                rec.informa_pnt_duns = company["PNT_DUNS"]
                rec.informa_stmt_dt = (
                    datetime.datetime.strptime(
                        company["STMT_DT"], "%Y%m%d"
                    ).date()
                    if company["STMT_DT"] is not None
                    else None
                )
                rec.informa_stmt_crcy_cd = company["STMT_CRCY_CD"]
                rec.informa_cash_liq_aset = company["CASH_LIQ_ASET"]
                rec.informa_tot_curr_aset = company["TOT_CURR_ASET"]
                rec.informa_tot_aset = company["TOT_ASET"]
                rec.informa_tot_curr_liab = company["TOT_CURR_LIAB"]
                rec.informa_tot_liab = company["TOT_LIAB"]
                rec.informa_net_wrth = company["NET_WRTH"]
                rec.informa_stmt_from_dt = (
                    datetime.datetime.strptime(
                        company["STMT_FROM_DT"], "%Y%m%d"
                    ).date()
                    if company["STMT_FROM_DT"] is not None
                    else None
                )
                rec.informa_stmt_to_dt = (
                    datetime.datetime.strptime(
                        company["STMT_TO_DT"], "%Y%m%d"
                    ).date()
                    if company["STMT_TO_DT"] is not None
                    else None
                )
                rec.informa_sls = company["SLS"]
                rec.informa_net_incm = company["NET_INCM"]
                rec.informa_qk_rato = company["QK_RATO"]
                rec.informa_curr_rato = company["CURR_RATO"]
                rec.informa_prev_net_wrth = company["PREV_NET_WRTH"]
                rec.informa_prev_sls = company["PREV_SLS"]
                rec.informa_prev_stmt_dt = (
                    datetime.datetime.strptime(
                        company["PREV_STMT_DT"], "%Y%m%d"
                    ).date()
                    if company["PREV_STMT_DT"] is not None
                    else None
                )
                rec.informa_pnt_ctry_cd = company["PNT_CTRY_CD"]

                rec.informa_last_update = fields.Datetime.now()
