from odoo.tests import common


class IntegrationTestSuite(common.TransactionCase):
    """
    Integration tests for Coreff base module
    """

    def setUp(self):
        super().setUp()
        # disable tracking
        self.env = self.env(context=dict(
            self.env.context, tracking_disable=True))

    def test_coreff_base_is_installed(self):
        """
        is module installed?
        """
        mod_model = self.env["ir.module.module"]
        self.assertIsNotNone(mod_model)

        found_modules = mod_model.search(
            [
                ("name", "=", "coreff_base"),
                ("state", "=", "installed"),
            ]
        )

        self.assertEqual(len(found_modules), 1,
                         "coreff_base Module not installed")
