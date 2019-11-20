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
    )

    informa_company_id = fields.Char(string="Informa id")

    informa_out_bus_ind = fields.Char()
    informa_tot_empl = fields.Char()
    informa_incn_yr = fields.Char()
    informa_finl_embt_ind = fields.Char()
    informa_dnb_ratg = fields.Char()
    informa_max_cr = fields.Char()
    informa_pnt_name = fields.Char()
    informa_pnt_duns = fields.Char()
    informa_stmt_dt = fields.Char()
    informa_stmt_crcy_cd = fields.Char()
    informa_cash_liq_aset = fields.Char()
    informa_tot_curr_aset = fields.Char()
    informa_tot_aset = fields.Char()
    informa_tot_curr_liab = fields.Char()
    informa_tot_liab = fields.Char()
    informa_net_wrth = fields.Char()
    informa_stmt_from_dt = fields.Char()
    informa_stmt_to_dt = fields.Char()
    informa_sls = fields.Char()
    informa_net_incm = fields.Char()
    informa_qk_rato = fields.Char()
    informa_curr_rato = fields.Char()
    informa_prev_net_wrth = fields.Char()
    informa_prev_sls = fields.Char()
    informa_prev_stmt_dt = fields.Char()
    informa_pnt_ctry_cd = fields.Char()

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
                rec.informa_pnt_name = company["PNT_NAME"]
                rec.informa_pnt_duns = company["PNT_DUNS"]
                rec.informa_stmt_dt = company["STMT_DT"]
                rec.informa_stmt_crcy_cd = company["STMT_CRCY_CD"]
                rec.informa_cash_liq_aset = company["CASH_LIQ_ASET"]
                rec.informa_tot_curr_aset = company["TOT_CURR_ASET"]
                rec.informa_tot_aset = company["TOT_ASET"]
                rec.informa_tot_curr_liab = company["TOT_CURR_LIAB"]
                rec.informa_tot_liab = company["TOT_LIAB"]
                rec.informa_net_wrth = company["NET_WRTH"]
                rec.informa_stmt_from_dt = company["STMT_FROM_DT"]
                rec.informa_stmt_to_dt = company["STMT_TO_DT"]
                rec.informa_sls = company["SLS"]
                rec.informa_net_incm = company["NET_INCM"]
                rec.informa_qk_rato = company["QK_RATO"]
                rec.informa_curr_rato = company["CURR_RATO"]
                rec.informa_prev_net_wrth = company["PREV_NET_WRTH"]
                rec.informa_prev_sls = company["PREV_SLS"]
                rec.informa_prev_stmt_dt = company["PREV_STMT_DT"]
                rec.informa_pnt_ctry_cd = company["PNT_CTRY_CD"]

                rec.informa_last_update = fields.Datetime.now()
