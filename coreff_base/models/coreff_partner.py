# -*- coding: utf-8 -*-
'''
Created on 8 August 2018

@author: J. Carette
@copyright: ©2018 Article 714
@license: AGPL v3
'''

from odoo import api, fields, models, tools, _

class CoreffPartner(models.Model):
    _inherit = 'res.partner'
    
    company_number = fields.Char(string=_(u'SIRET'), index=True)
    siren = fields.Char(string=_(u'SIRET'), index=True)
    nic = fields.Char(string=_(u'NIC'))
    
    company_name = fields.Char(string=_(u'Raison sociale'))
    trade_name = fields.Char(string=_(u'Enseigne'))
    acronym = fields.Char(string=_(u'Sigle'))
    activity_code = fields.Char(string=_(u'Code NAF'), len=5)
    activity_description = fields.Char(string=_(u'Libellé du code NAF'))
    legal_form = fields.Char(string=_(u'Forme juridique'))
    telephone = fields.Char(string=_(u'Téléphone'))
    court_registry_number = fields.Char(string=_(u'Numéro RCS'))
    court_registry_description = fields.Char(string=_(u'Greffe'))
    share_capital = fields.Char(string=_(u'Capital social'))
    incorporation_date = fields.Char(string=_(u'Date d\'immatriculation'))
    
    #postal_address 
        #name = fields.Char(string=_(u'Nom postal'))
        #addition_to_name = fields.Char(string=_(u'Complément de nom'))
        #address = fields.Char(string=_(u'Adresse postale'))
        #addition_to_address = fields.Char(string=_(u'Complément d\'adresse'))
        #special_distribution = fields.Char(string=_(u'Boîte postale'))
        #distribution_line = fields.Char(string=_(u'Code Postal/Ville'))
    
    nationality = fields.Char(string=_(u'Pays'))
    
    status_code = fields.Selection(string=_(u'Code du statut de l\'entreprise'),
        ('D',_(u'Supprimé')),
         ('N',_(u'Non diffusable')),
          ('I',_(u'Inactif')),
           ('A',_(u'Actif économiquement')),
            ('F',_(u'Fermé')),
             ('T',_(u'Transféré')),
              ('S',_(u'Cessé économiquement (INSEE)')),
               ('L',_(u'Liquidé')),
                ('O',_(u'Dormante')))
    status = fields.Char(string=_(u'Statut de l\'entreprise'))
    
    rating = fields.Char(string=_(u'Rating'))
    rating_desc1 = fields.Char(string=_(u'Rating / précision courte'))
    rating_desc2 = fields.Char(string=_(u'Rating / précision longue'))
    credit_limit = fields.Char(string=_(u'Limite de crédit'))
    
    last_judgement_date = fields.Char(string=_(u'Date du dernier jugement'))
    last_ccj_date = fields.Char(string=_(u'Date du dernier privilège'))
    number_of_directors = fields.Integer(string=_(u'Nombre de dirigeants de la société'))
    
    #Next fields need One2Many relation
    #ultimate_parents = fields.One2many(string=_(u'Element père contenant les maisons mères ultimes'))
        #ultimate_parent = fields.One2many(string=_(u'Element père contenant les détails d\'une maison mère ultime'))
            #name
            #number_of_companies = fields.Integer(string=_(u'Nombre d\'entreprises dans le groupe'))
    
    
    #financial_summary = fields.One2many(string=_(u'Element père contenant les chiffres clés de l\'entreprise'))
        #tradin_to_date = fields.One2many(string=_(u'Element père contenant les chiffres clés d\'une période données'))
            #date = fields.Date(string=_(u'Date du bilan conerné'))
            #turnover = fields.Char(string=_(u'Chiffre d\'affaire')) 
            #gross_operating_surplus = fields.Char(string=_(u'Excédent Brut d\'Exploitation (en %)'))
            #networth = fields.Char(string=_(u'Capitaux propres'))
            #employees = fields.Integer(string=_(u'Effectif'))
    
    
    
    

