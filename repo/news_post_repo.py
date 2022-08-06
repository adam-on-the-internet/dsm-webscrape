from util import request_util

datasource_url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/newsPost'


def save_news_post(news_post):
    json_data = news_post.to_json()
    request_util.post_json(datasource_url, json_data)


def get_news_posts():
    return request_util.get_json(datasource_url)


def get_news_post_urls():
    news_posts = get_news_posts()
    return list(map(get_url_property, news_posts))


def get_url_property(item):
    return item['url']

