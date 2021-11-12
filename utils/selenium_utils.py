"""
Idea is to provide a google search and pull images from the specific search
utils include
 - downloading imgs to file
 - selecting imgs from webdriver page
 - collecting urls from imgs
 - loading config
"""
import random
from typing import Optional, NoReturn
import time
import uuid
from os import path
import requests
import yaml

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException, ElementNotInteractableException
)

__author__ = 'jwiebe1017'
__version__ = '1.0.0'
__credits__ = ['stackoverflow', 'me, myself, and I', 'you I guess?']


# typehints
DRIVER = webdriver.chrome.webdriver.WebDriver
WEBELEMENT = webdriver.remote.webelement.WebElement


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


def collect_images_from_driver(
        driver: DRIVER,
        element: str,
        range_of_images: int,
        collected_images: list = None
) -> list:
    """
    given a selenium driver, provide the CLASS_NAME elements found in-page
    :param range_of_images: minimum number of images to provide
    :param collected_images: allows for recursion, list of collected_images
    :param driver: selenium active driver object
    :param element: element to search for
    :return: list of collected images
    """
    if collected_images is None:
        collected_images = driver.find_elements(By.CLASS_NAME, element)
    if range_of_images > len(collected_images):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        collected_images = driver.find_elements(By.CLASS_NAME, element)
        collect_images(driver, range_of_images, collected_images)
    return collected_images


def click_on_element(driver: DRIVER, element: WEBELEMENT) -> NoReturn:
    """
    attempts to click on an element, will scroll until the element
    appears to be present and sleep random.uniform(1,3) between attempts
    :param driver: selenium webdriver object
    :param element: selenium webelement object with .click() attribute
    :return: NoReturn, will click on the element
    """
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
    time.sleep(random.uniform(1, 3))
    try:  # hit it straight away and sleep if successful before continuing
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        time.sleep(random.uniform(1, 3))
    except (ElementClickInterceptedException, ElementNotInteractableException):
        # clickintercept, scroll the page around element in present with more sleeps
        click_on_element(driver, element)
    return


def return_img_url(driver: DRIVER, base_element: str, elem_num: int, thumbnail_class_element: str,
                   img_class_element: str) -> str:
    """
    given a list of selenium WebElements representing google imgs, click through one, and provide the 'src' as string
    :param driver: selenium active driver object
    :param base_element: element to search for
    :param elem_num: which img to click to and retrieve the src from
    :param thumbnail_class_element: thumbnail element, CLASS_NAME var
    :param img_class_element: img element, CLASS_NAME var
    :return: src, as a string
    """
    # start with a sleep to let the page load, more for n+1 img pulls
    time.sleep(random.uniform(1, 3))
    # collect images from page, scroll and recollect as necessary
    available_images = collect_images_from_driver(driver, base_element, elem_num)
    # click on the element in the page, scroll and sleep as necessary
    click_on_element(driver, available_images[elem_num])

    # pull the actual image
    pic = driver.find_elements(By.CLASS_NAME, thumbnail_class_element)
    return pic[0].find_elements(  # pic is len(2) list, google provides link in only one based on which img it is
        By.CLASS_NAME,
        img_class_element
    )[0].get_attribute('src') if elem_num == 0 else pic[1].find_elements(
        By.CLASS_NAME,
        img_class_element
    )[0].get_attribute('src')


def get_img_content(img_url: str) -> bytes:
    """
    given a src url, return the img as bytes
    :param img_url: url to image src
    :return: bytes representing the img
    """
    # 'bad return' to keep things rolling if theres a little floop here
    return requests.get(img_url).content if requests.get(img_url).status_code is 200 else b'BAD RETURN'


def write_to_file(
        img_content: bytes,
        file_loc: str,
        filename: Optional[str] = None,
        file_ext: Optional[str] = '.png') -> NoReturn:
    """
    Writes bytes objects to file, optional params if things change or need to be specified
    :param img_content: bytes rep of content to write to file
    :param file_loc: file location to save out to
    :param filename: optional, will generate random chars from uuid if not specified
    :param file_ext: optional, default is .png
    :return: NoReturn, saves the file
    """
    file_name = f'{filename}{file_ext}' if filename else f'{uuid.uuid4()}{file_ext}'
    full_filepath = path.join(file_loc, file_name)
    with open(full_filepath, 'wb') as f:
        f.write(img_content)
