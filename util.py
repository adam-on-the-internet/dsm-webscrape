import requests
from bs4 import BeautifulSoup


def convert_url_to_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, "html.parser")


def get_elements_of_type_with_class(soup, element_type, class_name):
    return soup.find_all(element_type, {"class": class_name})


def get_first_text_of_type_with_class(soup, element_type, class_name):
    elements = get_elements_of_type_with_class(soup, element_type, class_name)
    return elements[0].get_text().strip()


def get_first_link(soup):
    elements = soup.find_all('a')
    return elements[0].get('href')

