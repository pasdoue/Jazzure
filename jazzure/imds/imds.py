from pathlib import Path
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from R2Log import logger

"""
Github resource : https://github.com/microsoft/azureimds/tree/master
Microsoft doc : https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service
https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/managed-identities-status
https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-managed-identities-work-vm
https://learn.microsoft.com/en-us/azure/api-management/authentication-managed-identity-policy  #some identity endpoints listed here

Managed identities code : https://stackoverflow.com/questions/54470209/how-to-get-a-token-for-specific-user-assigned-managed-service-identity-for-azure
public static async Task<HttpResponseMessage> GetToken(string resource, string apiversion, string clientId)  
{
    HttpClient client = new HttpClient();   
    client.DefaultRequestHeaders.Add("Secret", Environment.GetEnvironmentVariable("MSI_SECRET"));
    return await client.GetAsync(String.Format("{0}/?resource={1}&api-version={2}&clientid={3}", Environment.GetEnvironmentVariable("MSI_ENDPOINT"), resource, apiversion,clientId));
}
"""


"""
Attested data : https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux#attested-data

Invoke-RestMethod -Headers @{"Metadata"="true"} -Method GET -Uri "http://169.254.169.254/metadata/attested/document?api-version=2020-09-01" | Format-List *

encoding  : pkcs7
signature :
MIIMbQYJKoZIhvcNAQcCoIIMXjCCDFoCAQExDzANBgkqhkiG9w0BAQsFADCCAVMGCSqGSIb3DQEHAaCCAUQEggFAeyJsaWNlbnNlVHlwZSI6IldpbmRvd3NfQ2x...m7BR78ya3R9dr307SJcxI6q72bMffYHjhfta9lcM3gt32Gi7RpI=

cat signature | base64 -d | strings | head -n1
@{"licenseType":"Windows_Client","nonce":"20260925-084217","plan":{"name":"","product":"","publisher":""},"sku":"win11-25h2-pro","subscriptionId":"dfee8600-0000-1111-ae65-d00dd0dd0dd0",
"timeStamp":{"createdOn":"09/25/26 02:42:17 -0000","expiresOn":"09/25/26 08:42:17 -0000"},"vmId":"4549e797-1111-0000-2222-2e6a2fa3d6f6"}
"""
from typing import List


class IMDS:

    SERVER_BASE_URL = "http://169.254.169.254"
    ROOT_URL = "/metadata"

    ATTESTED_URL = "/attested" # introduced 2018-10-01
    IDENTITY_URL = "/identity" # introduced 2018-02-01
    INSTANCE_URL = "/instance" # introduced 2017-04-02
    LOADBALANCER_URL = "/loadbalancer" # introduced 2020-10-01
    SCHEDULEDEVENTS_URL = "/scheduledevents" # introduced 2017-08-01
    VERSIONS_URL = "/versions"

    ONLINE_DATE_STR_FORMAT = "%Y-%d-%m"

    AVAILABLE_SCRIPT_LANGUAGES = ["python", "powershell", "curl"]

    def __int__(self):
        pass

    """
        Parse online endpoint versions as they are documented only online...
        For better fun, Microsoft introduced both date format "%Y-%d-%m" and "%Y-%m-%d" but the most encountered is "%Y-%d-%m"
        F*** Microcro
    """

    @staticmethod
    def parse_date(date_string):
        formats = ["%Y-%m-%d","%Y-%d-%m"]
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                pass
        # Handle invalid dates
        return None

    @staticmethod
    def sort_key(date_string):
        parsed = IMDS.parse_date(date_string)
        if parsed is None:
            # Put invalid dates at the end
            return datetime.max
        return parsed

    @staticmethod
    def parse_online_doc_loadbalancer_versions() -> List[str]:
        """
            Allow to list available API version for this endpoint
        """
        versions = []
        url = 'https://learn.microsoft.com/en-us/azure/load-balancer/howto-load-balancer-imds'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find(id="schema-breakdown")
        table = title.find_next("table")
        if table:
            # Find the column index of "Version"
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            version_index = headers.index("Version introduced")
            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                if len(cells) > version_index:
                    versions.append(cells[version_index].get_text(strip=True))
        else:
            logger.error(f"Impossible to find array of version on online doc")
        return sorted(versions, key=IMDS.sort_key)

    @staticmethod
    def parse_online_doc_scheduled_events_versions() -> List[str]:
        """
            Allow to list available API version for this endpoint
        """
        versions = []
        url = 'https://learn.microsoft.com/en-us/azure/virtual-machines/windows/scheduled-events'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find(id="version-and-region-availability")
        table = title.find_next("table")
        if table:
            # Find the column index of "Version"
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            version_index = headers.index("Version")
            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                if len(cells) > version_index:
                    versions.append(cells[version_index].get_text(strip=True))
        else:
            logger.error(f"Impossible to find array of version on online doc")
        return sorted(versions, key=IMDS.sort_key)

    @staticmethod
    def parse_online_doc_instance_versions() -> List[str]:
        """
            Allow to list available API version for this endpoint
        """
        versions = []
        url = 'https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find(id="instance-metadata")
        table = title.find_next("table").find_next("table")
        if table:
            # Find the column index of "Version"
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            version_index = headers.index("Version introduced")
            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                if len(cells) > version_index:
                    versions.append(cells[version_index].get_text(strip=True))
        else:
            logger.error(f"Impossible to find array of version on online doc")
        return sorted(versions, key=IMDS.sort_key)

    @staticmethod
    def parse_online_doc_attested_data_versions() -> List[str]:
        """
            Allow to list available API version for this endpoint
        """
        versions = []
        url = 'https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find(id="attested-data")
        table = title.find_next("table").find_next("table")
        if table:
            # Find the column index of "Version"
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            version_index = headers.index("Version introduced")
            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                if len(cells) > version_index:
                    versions.append(cells[version_index].get_text(strip=True))
        else:
            logger.error(f"Impossible to find array of version on online doc")
        return sorted(versions, key=IMDS.sort_key)

    #TODO : code online date check for identity (need to find it first :/ )

    def generate_script(self, language: str) -> None:
        if not language.lower() in self.AVAILABLE_SCRIPT_LANGUAGES:
            raise ValueError(f"Invalid script language : {language}. Please chose between those ones : {','.join(self.AVAILABLE_SCRIPT_LANGUAGES)}")

        env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True)

        if language == "powershell":
            template_filename = "powershell.ps1"
        elif language == "python":
            template_filename = "python.py"
        elif language == "curl":
            template_filename = "curl.sh"

        template = env.get_template(f"{template_filename}.j2")
        output = template.render(name="my-app",environment="production")

        Path(f"{template_filename}").write_text(output)



