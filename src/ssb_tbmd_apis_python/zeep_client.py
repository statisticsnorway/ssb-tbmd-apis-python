import os
import requests
from zeep import Client
from zeep.transports import Transport

class LocalResolverTransport(Transport):
    def load(self, url):
        base_dir = os.path.dirname(__file__)
        xsds_dir = os.path.join(base_dir, 'xsds')
        
        if url == 'http://www.w3.org/2001/XMLSchema':
            xsd_path = os.path.join(xsds_dir, 'w3_org_2001_XMLSchema.xsd')
            with open(xsd_path, 'rb') as f:
                return f.read()
        if url == 'https://www.w3.org/2001/xml.xsd':
            xsd_path = os.path.join(xsds_dir, 'w3_org_2001_xml.xsd')
            with open(xsd_path, 'rb') as f:
                return f.read()
        return super().load(url)

def get_transport():
    session = requests.Session()
    transport = LocalResolverTransport(session=session)
    return transport

def get_zeep_client():
    wsdl_datadok = "http://ws.ssb.no/DatadokService/DatadokService.asmx?WSDL"
    return Client(wsdl=wsdl_datadok, transport=get_transport())