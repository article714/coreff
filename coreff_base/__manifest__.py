# coding: utf-8

# @author: J. Carette
# @author: C. Guychard
# @copyright: ©2018-2019 Article 714
# @license: AGPL v3

{
    'name': u'CoreFF: Basic Module',
    'version': u'12.0.1.0.0',
    'category': u'CoreFF',
    'author': u'Article714',
    'license': u'AGPL-3',
    'website': u'https://www.article714.org',
    'summary': u'Manage Core Financial Data: base module',
    'depends': ['base','l10n_fr'],
    'data': ['security/coreff_security.xml',
             'views/coreff_partner_views.xml',
             'views/coreff_config_views.xml',
             'views/tree_view_assets.xml'],

    'qweb': ['static/src/xml/create_from_button.xml'], 

    'installable': True,
    'images': [],
    'application': False,
}
