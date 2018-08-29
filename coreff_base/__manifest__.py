# -*- coding: utf-8 -*-
# @author: J. Carette
# @copyright: ©2018 Article 714
# @license: AGPL v3

{
    'name': u'coref',
    'version': u'10.0.1.0.0',
    'category': u'Applications',
    'author': u'Article714',
    'license': u'AGPL-3',
    'website': u'https://www.article714.org',
    'description': u"""
CORE Financial extensions 
=========================

The aim of this module is to add financial informations 
from CreditSafe to res_partner model. 

Of course you need a CreditSafe account.  

**Credits:** .
""",
    'depends': ['base'],
    'data': ['views/coref_partner_views.xml'],
    'installable': True,
    'images': [],
    'application': True,
}
