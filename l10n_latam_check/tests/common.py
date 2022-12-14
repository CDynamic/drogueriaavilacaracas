# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests.common import tagged


@tagged('post_install_l10n', 'post_install', '-at_install')
class L10nLatamCheckTest(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        if chart_template_ref:
            chart_template = cls.env.ref(chart_template_ref)
        else:
            chart_template = cls.env.ref('l10n_generic_coa.configurable_chart_template', raise_if_not_found=False)

        cls.company_data_3 = cls.setup_company_data(
            'company_3_data', chart_template=chart_template, **{'country_id': cls.env.ref('base.ar').id})

        cls.bank_journal = cls.company_data_3['default_journal_bank']
        cls.deferred_checkbook = cls.env['l10n_latam.checkbook'].create({
            'journal_id': cls.bank_journal.id,
            'next_number': 50,
            'range_to': 100,
            'type': 'deferred',
        })
        cls.current_checkbook = cls.env['l10n_latam.checkbook'].create({
            'journal_id': cls.bank_journal.id,
            'next_number': 100,
            'range_to': 150,
            'type': 'currents',
        })
        cls.electronic_checkbook = cls.env['l10n_latam.checkbook'].create({
            'journal_id': cls.bank_journal.id,
            'next_number': 200,
            'type': 'electronic',
        })

        third_party_checks_journals = cls.env['account.journal'].search([('outbound_payment_method_line_ids.code', '=', 'new_third_party_checks'), ('inbound_payment_method_line_ids.code', '=', 'out_third_party_checks'), ('inbound_payment_method_line_ids.code', '=', 'new_third_party_checks')])
        if len(third_party_checks_journals) == 2:
            cls.third_party_check_journal = third_party_checks_journals[0]
            cls.rejected_check_journal = third_party_checks_journals[1]
        else:
            cls.third_party_check_journal = False
            cls.rejected_check_journal = False
