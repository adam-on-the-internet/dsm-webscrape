import request_util

news_post_data_url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/newsPost'


def save_news_post(news_post):
    news_post_json = news_post.to_json()
    request_util.post_json(news_post_data_url, news_post_json)


def get_news_posts():
    existing_news_posts = request_util.get_json(news_post_data_url)
    return existing_news_posts


def get_news_post_urls():
    existing_news_posts = get_news_posts()
    return list(map(get_url_property, existing_news_posts))


def get_url_property(item):
    return item['url']

