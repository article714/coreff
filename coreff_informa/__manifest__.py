# -*- coding: utf-8 -*-
# @author: J. Carette
# @copyright: ©2018 Article 714
# @license: AGPL v3

{
    'name': u'CoreFF: Informa',
    'version': u'10.0.1.0.0',
    'category': u'CoreFF',
    'author': u'Article714',
    'license': u'AGPL-3',
    'website': u'https://www.article714.org',
    'description': u"""
CoreFF - INFORMA 
===================

The aim of this module is to get financial informations 
from Informa and add them to res_partner model. 

Of course, you need an Informa account and set its properties
into "financial informations" configuration menu.   

**Credits:** .
""",
    'depends': ['coreff_base'],
    'data': ['views/coreff_config_view.xml'],
    'qweb': ['static/src/xml/create_from_button.xml'],
    'installable': True,
    'images': [],
    'application': True,
}
