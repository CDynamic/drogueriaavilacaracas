# -*- coding: utf-8 -*-

from odoo import models, fields, api


class setting_initial_accounting(models.Model):
    _inherit = "res.company"

    # @api.depends('account_dashboard_onboarding_state')
    def button_account_dashboard_onboarding_state(self):
        self.account_dashboard_onboarding_state = 'not_done'
        self.account_invoice_onboarding_state = 'not_done'
        pass
