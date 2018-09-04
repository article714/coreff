# -*- coding: utf-8 -*-
# ©2018 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml.etree import Element, tostring
import logging
import re

import threading


try:
    import zeep
except:
    logging.exception("Cannot find Zeep, some CreditSafe features won't be available")

from odoo import exceptions


#---------------------------------
# global vars
wsdl = 'https://www.creditsafe.fr/getdata/service/CSFRServices.asmx?wsdl'

#<header> 
#<username>Login</username> 
#<password>Password</password> 
#<operation>Operation</operation> 
#<language>Langue</language>
#<country>Pays</country>
#<chargereference>Reference utilisateur</chargereference>
#</header>

header_values = {
    'username': 'InfibailTEST',
    'password': 'Infibail8746915',
    'operation': 'getcompanyinformation',
    'language': 'FR',
    'country': 'FR',
    'chargereference': ''    
}

body_values = {
    'package': 'standard',
    'companynumber': ''
}


class ZeepClient(object):

    xml_request = Element('xmlrequest')

    def __init__(self):
        self.header_elements = []

        self.lock = threading.Lock()
        #complete header values
        header = Element('header')
        for k in header_values:
            a = Element(k)
            a.text = header_values[k]
            #self.header_elements.append(a)
            header.append(a)

        #complete body values
        body = Element('body')
        for l in body_values:
            b = Element(l)
            b.text = body_values[l]
            body.append(b)
        
        self.xml_request.append(header)
        self. xml_request.append(body)
        self.client = zeep.Client(wsdl=wsdl)

        #set namespace to Zeep Client
        #self.client.set_ns_prefix('NS1', 'http://NAMESPACE_URL')

    def getCompanyInformation(self, siret, ref = '', operation = 'getcompanyinformation'):
        self.lock.acquire()
        try:
            #complete header with specific values
            
            o = self.xml_request.xpath('/xmlrequest/header/operation')
            o[0].text = operation
            
            if(ref != ''):
                c = self.xml_request.xpath('/xmlrequest/header/chargereference')
                c[0].text = ref
             
            if(siret != None and siret != ''):
                s = self.xml_request.xpath('/xmlrequest/body/companynumber')
                s[0].text = siret
            
            logging.info('XML_REQUEST : '+tostring(self.xml_request, pretty_print=True))
            xml_response = self.client.service.GetData(tostring(self.xml_request, pretty_print=True))
            logging.info('XML_RRESPONSE : '+str(xml_response))
            return xml_response

        
        except zeep.exceptions.Fault as e:
            logging.warning('Fault when PROCESSING Credit-Safe Service --> %s' % str(e))
            return None
        except Exception as e:
            # This means something went wrong.
            logging.exception('ERROR WHEN PROCESSING Credit-Safe Service --> %s' % str(e))
            return None
        finally:
            self.lock.release()



zeep_client = ZeepClient()


def get_company_information_by_siret(siret, ref):
    logging.info("GET_COMPANY_INFORMATION_BY_SIRET")
    
    if zeep_client != None:
   
        return zeep_client.getCompanyInformation(siret, ref)
    else:
        logging.warning('Fault when PROCESSING Credit-Safe Service --> No Zeep Client found')