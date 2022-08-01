import requests
from bs4 import BeautifulSoup


def convert_url_to_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, "html.parser")


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
    return elements[0].get('href')


def remove_divs_with_class(soup, class_name):
    for div in soup.find_all("div", {'class': class_name}):
        div.decompose()


def remove_script(soup):
    for script in soup.select('script'):
        script.extract()


def post_json(url, data):
    return requests.post(url, data)


def get_json(url):
    response = get(url)
    return response.json()


def get(url):
    return requests.get(url)
