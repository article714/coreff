# -*- coding: utf-8 -*-
# ©2018 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml.etree import Element, tostring, parse, fromstring
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
    'username': 'T3st_GD_INFIBAIL',
    'password': 'creditsafe',
    'operation': 'getcompanyinformation',
    'language': 'FR',
    'country': 'FR',
    'chargereference': ''
}

body_values = {
    'package': 'standard',
    'companynumber': '63201210000012'
}


class ZeepClient(object):

    xml_request = Element('xmlrequest')

    def __init__(self):
        self.header_elements = []

        self.lock = threading.Lock()
        # complete header values
        header = Element('header')
        for k in header_values:
            a = Element(k)
            a.text = header_values[k]
            # self.header_elements.append(a)
            header.append(a)

        # complete body values
        body = Element('body')
        for l in body_values:
            b = Element(l)
            b.text = body_values[l]
            body.append(b)

        self.xml_request.append(header)
        self. xml_request.append(body)
        try:
            self.client = zeep.Client(wsdl=wsdl)
        except:
            logging.error("NO Zeep Client initialized")
            self.client = None

        # set namespace to Zeep Client
        #self.client.set_ns_prefix('NS1', 'http://NAMESPACE_URL')

    def getCompanyInformation(self, siret, ref='', operation='getcompanyinformation'):
        self.lock.acquire()
        try:
            # complete header with specific values

            o = self.xml_request.xpath('/xmlrequest/header/operation')
            o[0].text = operation

            if(ref != ''):
                c = self.xml_request.xpath('/xmlrequest/header/chargereference')
                c[0].text = ref

            if(siret != None and siret != ''):
                s = self.xml_request.xpath('/xmlrequest/body/companynumber')
                s[0].text = siret

            response = self.client.service.GetData(tostring(self.xml_request, pretty_print=True))

            if response != None:

                # Besoin d'encoder en UTF-8 avant lecture
                xml = response.encode("utf-8")
                xml_response = fromstring(response)

                report_type = xml_response.xpath('/xmlresponse/header/reportinformation/reporttype')
                if report_type != None and report_type[0].text == str(operation):
                    return xml_response
                else:
                    error_detail = xml_response.xpath('/xmlresponse/body/errors/errordetail')
                    code = error_detail[0].find('code').text
                    desc = error_detail[0].find('desc').text
                    raise Exception(
                        "Erreur lors de l'execution du service Credit Safe - CODE : %s - LABEL : %s" % (code, desc))

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

    if zeep_client != None:

        return zeep_client.getCompanyInformation(siret, ref)
    else:
        logging.warning('Fault when PROCESSING Credit-Safe Service --> No Zeep Client found')
