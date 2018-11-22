# -*- coding: utf-8 -*-
# @author: J. Carette
# @copyright: ©2018 Article 714
# @license: AGPL v3

{
    'name': u'CoreFF: Basic Module',
    'version': u'10.0.1.0.0',
    'category': u'CoreFF',
    'author': u'Article714',
    'license': u'AGPL-3',
    'website': u'https://www.article714.org',
    'description': u"""
CoreFF - Core Financial Functions 
=================================

The aim of this module is to add financial informations 
from CreditSafe to res_partner model. 

Of course, you need a CreditSafe account.  

**Credits:** .
""",
    'depends': ['base',
                'web', 'web_sheet_full_width', 'web_dialog_size', 'web_no_bubble', 'web_translate_dialog',
                'web_tree_dynamic_colored_field','web_notify',
                'l10n_fr_siret'],
    'data': ['security/coreff_security.xml',
             'security/base_access_model.xml',
             'actions/window_actions.xml',
             'views/coreff_partner_views.xml',
             'views/coreff_config_views.xml',
             'views/coreff_menus.xml'],
    'installable': True,
    'images': [],
    'application': True,
}
