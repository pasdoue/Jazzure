import importlib.metadata
from typing import List, Union

import requests
from R2Log import logger
from bs4 import BeautifulSoup


def check_azure_sdk_loaded(return_list: bool = False) -> Union[bool|List[str]]:
    pip_installed = [dist.metadata.get("Name","") for dist in sorted(importlib.metadata.distributions(), key=lambda d: d.metadata["Name"].lower())]
    if return_list:
        return [pkg_name for pkg_name in pip_installed if pkg_name.startswith("azure-") ]
    else:
        if not any(pkg_name.startswith("azure-") for pkg_name in pip_installed):
            return False
        return True


class Pypi_Crawler:
    """
        Class to walk through Pypi and discover all SDK developed by Microsoft for Azure.
        They are all maintained by generic user called 'azure-sdk' (for once that Microsoft do something right :D)
    """

    PACKAGES_URL = "https://pypi.org/user/azure-sdk/"

    @classmethod
    def get_pypi_packages(cls) -> List[str]:
        res = []
        response = requests.get(cls.PACKAGES_URL, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        div = soup.find("div", attrs={"class":"left-layout__main"})
        number_projects_title = div.find_next("h2")
        number_projects = number_projects_title.text.split(' ')[0].strip()
        logger.info(f"There are actually : {number_projects} packages")

        div = div.find_next("div")
        for link in div.find_all("a", href=True):
            package_name = link.get("href", "").split('/')[-2]
            res.append(package_name)
        return list(set(res))





















