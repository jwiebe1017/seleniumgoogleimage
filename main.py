"""
Idea is to provide a google search and pull images from the specific search
TODO: make this a class
TODO: figure out the 'input' part - gui? hopefully not... in config for now :*(
TODO: pull and download somewhere, probably stick that shit in the config
"""
from typing import Optional

import yaml

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_config(loc: Optional[str] = None) -> dict:
    """
    Loads in-project config file, optional filelocation can be passed as well.
    :param loc: [OPTIONAL] file location
    :return: dict of yaml data
    """
    with open(loc if loc else 'config.yml') as f:
        return yaml.safe_load(f)


def build_url(base_url: str, replacement_key: str, search_string: str) -> str:
    """
    Given a base url with placeholder called out, replace it with the search params.
    :param base_url: base url with replacement val hanging in there
    :param replacement_key: the replacement val
    :param search_string: what to replace the val with, i.e. search input
    :return: string with search items in there
    """
    final_string = search_string if ' ' not in search_string else search_string.replace(' ', '+')
    return base_url.replace(replacement_key, final_string)


data = get_config()
query = build_url(data['BASE_URL'], data['QUERY_REPL'], data['TEMP_SEARCH_STR'])

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(query)
