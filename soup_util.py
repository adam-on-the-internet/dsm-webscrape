import re

from bs4 import BeautifulSoup

import request_util


def convert_url_to_soup(url):
    page = request_util.get(url)
    return BeautifulSoup(page.text, "html.parser")


def get_elements_of_type(soup, element_type):
    return soup.find_all(element_type)


def get_elements_of_type_with_text(soup, element_type, text):
    return soup.find_all(element_type, text=re.compile(text))


def get_elements_of_type_with_class(soup, element_type, class_name):
    return soup.find_all(element_type, {"class": class_name})


def get_elements_of_type_with_id(soup, element_type, id):
    return soup.find_all(element_type, {"id": id})


def get_first_text_of_type_with_class(soup, element_type, class_name):
    elements = get_elements_of_type_with_class(soup, element_type, class_name)
    return get_text_from_element(elements[0])


def get_first_text_of_type_with_id(soup, element_type, id):
    elements = get_elements_of_type_with_id(soup, element_type, id)
    return get_text_from_element(elements[0])


def get_text_from_element(element):
    return element.get_text().strip()


def get_first_link(soup):
    elements = soup.find_all('a')
    return get_link_from_element(elements[0])


def get_link_from_element(element):
    return element.get('href')


def remove_divs_with_class(soup, class_name):
    for div in soup.find_all("div", {'class': class_name}):
        div.decompose()


def remove_script(soup):
    remove_tags(soup, "script")


def remove_tags(soup, tag_name):
    for script in soup.select(tag_name):
        script.extract()
