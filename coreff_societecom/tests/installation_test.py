from odoo.tests import common


class IntegrationTestSuite(common.TransactionCase):
    """
    Integration tests for Coreff Societe.com module
    """

    def setUp(self):
        super().setUp()
        # disable tracking
        self.env = self.env(context=dict(
            self.env.context, tracking_disable=True))

    def test_coreff_societecom_is_installed(self):
        """
        is module installed?
        """
        mod_model = self.env["ir.module.module"]
        self.assertIsNotNone(mod_model)

        found_modules = mod_model.search(
            [
                ("name", "=", "coreff_societecom"),
                ("state", "=", "installed"),
            ]
        )

        self.assertEqual(len(found_modules), 1,
                         "coreff_societecom Module not installed")
