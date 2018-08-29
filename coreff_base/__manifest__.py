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
    'depends': ['base'],
    'data': ['views/coreff_partner_views.xml'],
    'installable': True,
    'images': [],
    'application': True,
}
