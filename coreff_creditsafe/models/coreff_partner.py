# -*- coding: utf-8 -*-
'''
Created on 2018, Sept 1

@author: J. Carette
@copyright: ©2018 Article 714
@license: AGPL v3
'''

import logging


from odoo import api, fields, models, _
from creditsafe_data_wsdl import get_company_information_by_siret

_logger = logging.getLogger(__name__)

class CoreffPartner(models.Model):
    _inherit = 'res.partner'

    #All specific fields from CreditSafe services
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
    
    code_status = fields.Selection(selection=[('D', _(u'Supprimé')),
                                    ('N', _(u'Non diffusable')),
                                    ('I', _(u'Inactif')),
                                    ('A', _(u'Actif économiquement')),
                                    ('F', _(u'Fermé')),
                                    ('T', _(u'Transféré')),
                                    ('S', _(u'Cessé économiquement (INSEE)')),
                                    ('L', _(u'Liquidé')),
                                    ('O', _(u'Dormante'))],
                                    string=_(u'Code statut de l\'entreprise'))
    
    
    label_status = fields.Char(string=_(u'Statut de l\'entreprise'))
    
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
    
   
 
    @api.one
    def interactive_update(self):
        super(CoreffPartner, self).interactive_update()
        _logger.info('INTERACTIVE UPDATE')      
        self.get_company_information()

    #-------------------------
    @api.one
    def get_company_information(self):
        _logger.info('GET COMPANY INFO FOR SIRET NUMEBR : '+str(self.company_name))
        get_company_information_by_siret(self.company_name, 'CS-IB-'+self.company_name);
    
