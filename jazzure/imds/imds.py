from pathlib import Path
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from R2Log import logger
from rich.prompt import Prompt

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
from typing import List, Tuple

TEMPLATE_FOLDER = Path(__file__).parent / "templates"


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

    AVAILABLE_OS = ["windows", "linux"]

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
        versions = list(set(versions))
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
        versions = list(set(versions))
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
        versions = list(set(versions))
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
        versions = list(set(versions))
        return sorted(versions, key=IMDS.sort_key)

    #TODO : code online date check for identity (need to find it first :/ )

    @staticmethod
    def get_all_versions() -> Tuple[List[str], List[str], List[str], List[str]]:
        logger.info(f"Collecting all IMDS endpoints versions")
        attested_v = IMDS.parse_online_doc_attested_data_versions()
        instance_v = IMDS.parse_online_doc_instance_versions()
        loadbalancer_v = IMDS.parse_online_doc_loadbalancer_versions()
        scheduled_events_v = IMDS.parse_online_doc_scheduled_events_versions()
        logger.success(f"All versions retrieved")
        return attested_v, instance_v, loadbalancer_v, scheduled_events_v

    @staticmethod
    def print_all_versions() -> None:
        a, i, l, s = IMDS.get_all_versions()
        logger.info(f"Available versions for attested : {a}")
        logger.info(f"Available versions for instance : {i}")
        logger.info(f"Available versions for loadbalancer : {l}")
        logger.info(f"Available versions for scheduled_events : {s}")

    @staticmethod
    def generate_script(vm_os: str) -> None:
        if not vm_os.lower() in IMDS.AVAILABLE_OS:
            raise ValueError(f"Invalid OS : {vm_os}. Please chose between those ones : {','.join(IMDS.AVAILABLE_OS)}")

        env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER.absolute()), trim_blocks=True, lstrip_blocks=True)

        template_filename = "powershell.ps1"
        if vm_os == "linux":
            template_filename = "curl.sh"

        #select versions for all endpoints
        a, i, l, s = IMDS.get_all_versions()
        logger.info(f"You will be prompted to chose a version for all IMDS endpoints. 'all' & 'latest' are accepted too")
        a_v = Prompt.ask(prompt="Attested version to use", choices=a + ["all", "latest"], show_choices=True)
        i_v = Prompt.ask(prompt="Instance version to use", choices=i + ["all", "latest"], show_choices=True)
        l_v = Prompt.ask(prompt="Loadbalancer version to use", choices=l + ["all", "latest"], show_choices=True)
        s_v = Prompt.ask(prompt="Scheduled events version to use", choices=s + ["all", "latest"], show_choices=True)

        if a_v == "latest":
            a_v = [a[-1]]
        elif a_v == "all":
            a_v = a
        else:
            a_v = [a_v]
        if i_v == "latest":
            i_v = [i[-1]]
        elif i_v == "all":
            i_v = i
        else:
            i_v = [i_v]
        if l_v == "latest":
            l_v = [l[-1]]
        elif l_v == "all":
            l_v = l
        else:
            l_v = [l_v]
        if s_v == "latest":
            s_v = [s[-1]]
        elif s_v == "all":
            s_v = s
        else:
            s_v = [s_v]

        a_versions = ", ".join(f"'{version}'" for version in a_v)
        i_versions = ", ".join(f"'{version}'" for version in i_v)
        l_versions = ", ".join(f"'{version}'" for version in l_v)
        s_versions = ", ".join(f"'{version}'" for version in s_v)
        template = env.get_template(f"{template_filename}.j2")
        output = template.render(a_v=a_versions, i_v=i_versions, l_v=l_versions, s_v=s_versions)

        out_file = Path(__file__).parent / f"{template_filename}"
        out_file.write_text(output)
        logger.success(f"Template generated here : {out_file}")


def run(args):
    if args.gen_script:
        IMDS.generate_script(vm_os=args.vm_os)
    elif args.get_endpoints_versions:
        IMDS.print_all_versions()


def register_parser(subparsers):
    parser = subparsers.add_parser("imds", help="IMDS manager")

    get_versions = parser.add_argument_group('Get API versions for all endpoints')
    get_versions.add_argument("--get-endpoints-versions", action="store_true", help=f"Print versions for all endpoints")

    gen_script_group = parser.add_argument_group('Generate script')
    gen_script_group.add_argument("--gen-script", action="store_true", help=f"Generate script based on templates available inside {TEMPLATE_FOLDER}")
    gen_script_group.add_argument("--vm-os", choices=["windows", "linux"], help=f"Will determine if generated script will be powershell or curl")

    # will allow to execute 'run' function from main.py and all subpackages can use same logic to expose its own args if needed
    parser.set_defaults(func=run)

    return parser
