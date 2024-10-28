import os
import requests
import zeep
from collections import OrderedDict
from typing import Any

class LocalResolverTransport(zeep.transports.Transport):
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

class ZeepClientManager:
    def __init__(self, wsdl):
        self.wsdl = wsdl
        self.session = None
        self.client = None

    def __enter__(self):
        self.session = requests.Session()
        transport = LocalResolverTransport(session=self.session)
        self.client = zeep.Client(wsdl=self.wsdl, transport=transport)
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session:
            self.session.close()
        self.client = None

        
def get_zeep_client(tbmd_service: str = "datadok") -> ZeepClientManager:
    wsdls = {
        "datadok": "http://ws.ssb.no/DatadokService/DatadokService.asmx?WSDL",
        "metadb":  "http://ws.ssb.no/MetaDbService/MetaDbService.asmx?WSDL",
        "vardok":  "http://ws.ssb.no/VardokService/VardokService.asmx?WSDL",
        "statbank":  "http://ws.ssb.no/statbankmetaservice/Service.asmx?WSDL",
    }
    
    tbmd_service = tbmd_service.lower()
    if tbmd_service not in wsdls:
        raise NotImplementedError(f"{tbmd_service} not implemented yet.")
        
    return ZeepClientManager(wsdl=wsdls[tbmd_service])


def get_zeep_serialize(tbmd_service: str = "datadok",
                       service: str = "GetFileDescriptionByPath",
                       *args) -> OrderedDict[str, Any]:
    with get_zeep_client(tbmd_service) as client:
        response = getattr(client.service, service)(*args)
    return zeep.helpers.serialize_object(response)