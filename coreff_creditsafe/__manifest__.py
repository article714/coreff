# -*- coding: utf-8 -*-
# @author: J. Carette
# @copyright: ©2018 Article 714
# @license: AGPL v3

{
    'name': u'CoreFF: CreditSafe',
    'version': u'10.0.1.0.0',
    'category': u'CoreFF',
    'author': u'Article714',
    'license': u'AGPL-3',
    'website': u'https://www.article714.org',
    'description': u"""
CoreFF - CreditSafe 
===================

The aim of this module is to get financial informations 
from CreditSafe and add them to res_partner model. 

Of course, you need a CreditSafe account and set its properties
into "financial informations" configuration menu.   

**Credits:** .
""",
    'depends': ['coreff_base'],
    'data': ['views/coreff_config_view.xml'],
    'installable': True,
    'images': [],
    'application': True,
}
