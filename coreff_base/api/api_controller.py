# -*- coding: utf-8 -*-
'''
Created on 8 August 2018

@author: J. Carette
@copyright: ©2018 Article 714
@license: AGPL v3
'''


import logging

from odoo.exceptions import ValidationError
from odoo.http import route, request, Controller

_logger = logging.getLogger(__name__)

#TODO à compléter
ERROR_CODES = {(100, _(u'Aucune chaîne XML n\'a été envoyée'), _(u'Une chaîne vide a été envoyée à GetData.')),
               (110, _(u'<xmlrequest> n\'a pas été envoyé à GetData'), _(u'<xmlrequest est manquant.')),
               (111, _(u'<xmlrequest> présent plus d\'une fois dans la trame'), _(u'il y a au moins deux <xmlrequest> dans la chaine.'))}


class ApiController(Controller):
    '''
    This controller deals with this kind of URL : 
            /api/getcompanyinformation/<operation>
        
        or
            /api/societe-com/<operation>
        
        operation values can be : companysearch | getcompanyinformation | directorsearch | getdirectorinformation 
    '''
    
    def checkAuthAndRun(self, search_function, unid):
        response = None
        
        #usefull for IP Filtering
        headers = request.httprequest.headers
        if 'X-Forwarded-For' in headers:
            IP_To_Check = headers['X-Forwarded-For']
        else:    
            IP_To_Check = request.httprequest.remote_addr
            
        _logger.info('IP Detected in header : '+ str(IP_To_Check))
        if(True):
            additional_info = {}
            localResult = search_function(self, unid, addtl_info=additional_info)
            if localResult != None:
        
    
    
    
    def getCompanyInformation(self):
    
    
    @route('/api/getcompanyinformation/<string:unid>', auth='public', type='http')
    def apiGetCompanyInformationHandler(self, unid='None'):
        
        return self.checkAuthAndRun(ApiController.getCompanyInformation, unid)    


