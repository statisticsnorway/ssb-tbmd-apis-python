import os
from collections import OrderedDict
from types import TracebackType
from typing import Any

import requests
import zeep


class LocalResolverTransport(zeep.transports.Transport):
    """Custom transport class to load local XSD files for Zeep client."""

    def load(self, url: str) -> bytes:
        """Load XSD files from local directory instead of fetching them from the internet.

        Args:
            url (str): The URL of the XSD file to load.

        Returns:
            bytes: The content of the XSD file.
        """
        base_dir = os.path.dirname(__file__)
        xsds_dir = os.path.join(base_dir, "xsds")

        if url == "http://www.w3.org/2001/XMLSchema":
            xsd_path = os.path.join(xsds_dir, "w3_org_2001_XMLSchema.xsd")
            with open(xsd_path, "rb") as f:
                return f.read()
        if url == "https://www.w3.org/2001/xml.xsd":
            xsd_path = os.path.join(xsds_dir, "w3_org_2001_xml.xsd")
            with open(xsd_path, "rb") as f:
                return f.read()
        return super().load(url)


class ZeepClientManager:
    """Context manager for Zeep client to handle WSDL and session management."""

    def __init__(self, wsdl: str) -> None:
        """Initialize the ZeepClientManager with the provided WSDL URL.

        Args:
            wsdl (str): The WSDL URL for the Zeep client.
        """
        self.wsdl = wsdl
        self.session = None
        self.client = None

    def __enter__(self) -> zeep.Client:
        """Create a Zeep client and return it."""
        self.session = requests.Session()
        transport = LocalResolverTransport(session=self.session)
        self.client = zeep.Client(wsdl=self.wsdl, transport=transport)
        return self.client

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the session and clean up resources."""
        if self.session:
            self.session.close()
        self.client = None


def get_zeep_client(tbmd_service: str = "datadok") -> ZeepClientManager:
    """Get a Zeep client for the specified TBMD service.

    Args:
        tbmd_service: The TBMD service to use (default is "datadok").

    Returns:
        ZeepClientManager: A context manager for the Zeep client.

    Raises:
        NotImplementedError: If the specified TBMD service is not implemented.
    """
    wsdls = {
        "datadok": "http://ws.ssb.no/DatadokService/DatadokService.asmx?WSDL",
        "metadb": "http://ws.ssb.no/MetaDbService/MetaDbService.asmx?WSDL",
        "vardok": "http://ws.ssb.no/VardokService/VardokService.asmx?WSDL",
        "statbank": "http://ws.ssb.no/statbankmetaservice/Service.asmx?WSDL",
    }

    tbmd_service = tbmd_service.lower()
    if tbmd_service not in wsdls:
        raise NotImplementedError(f"{tbmd_service} not implemented yet.")

    return ZeepClientManager(wsdl=wsdls[tbmd_service])


def get_zeep_serialize(
    tbmd_service: str = "datadok",
    operation: str = "GetFileDescriptionByPath",
    *args: str,
) -> OrderedDict[str, Any]:
    """Get serialized response from the Zeep client for the specified operation.

    Args:
        tbmd_service (str): The TBMD service to use (default is "datadok").
        operation (str): The operation to perform (default is "GetFileDescriptionByPath").
        *args: Arguments for the operation.

    Returns:
        OrderedDict: The serialized response from the Zeep client.
    """
    with get_zeep_client(tbmd_service) as client:
        response = getattr(client.service, operation)(*args)
    return zeep.helpers.serialize_object(response)
