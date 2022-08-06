import requests


def post_json(url, data):
    return requests.post(url, data)


def get_json(url):
    response = get(url)
    return response.json()


def get(url):
    return requests.get(url)
