import util
from models.NewsHeading import NewsHeading
from models.NewsPost import NewsPost


def get_press_releases():
    news_headings = get_news_headings()
    new_news_headings = get_discovered_news_headings(news_headings)
    posts = get_news_posts_for_headings(new_news_headings)
    for post in posts:
        save_news_post(post)
        print(f" - {post.get_message()}")
    return posts


def save_news_post(news_post):
    url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/newsPost'
    news_post_json = news_post.to_json()
    util.post_json(url, news_post_json)


def get_existing_news_post_urls():
    url = 'https://aoti-basic-express-app.herokuapp.com/dsmScrape/newsPost'
    existing_news_posts = util.get_json(url)
    return list(map(get_url, existing_news_posts))


def refine_news_heading(news_heading_element):
    date = util.get_first_text_of_type_with_class(news_heading_element, "div", "news-date")
    title = util.get_first_text_of_type_with_class(news_heading_element, "h3", "news-title")
    url = util.get_first_link(news_heading_element)
    news_heading = NewsHeading(title, url, date)
    return news_heading


def get_url(news_post):
    return news_post['heading_url']


def get_discovered_news_headings(news_headings):
    new_news_headings = []
    existing_urls = get_existing_news_post_urls()
    for heading in news_headings:
        if heading.url not in existing_urls:
            new_news_headings.append(heading)
    return new_news_headings


def get_news_posts_for_headings(new_news_headings):
    posts = []
    for heading in new_news_headings:
        post = get_news_post_for_heading(heading)
        posts.append(post)
    return posts


def get_news_post_for_heading(heading):
    page_url = f"https://www.dsm.city/{heading.url}"
    soup = util.convert_url_to_soup(page_url)
    page_title = util.get_first_text_of_type_with_id(soup, "h2", "page-title")
    page_content = util.get_elements_of_type_with_id(soup, "div", "post")[0]
    # TODO can we strip out the comments?
    util.remove_script(page_content)
    util.remove_divs_with_class(page_content, "editcenterBtns")
    post = NewsPost(heading.title, heading.date, heading.url, page_title, page_url, str(page_content))
    return post


def get_news_headings():
    dsm_newslist_url = 'https://www.dsm.city/newslist.php'
    soup = util.convert_url_to_soup(dsm_newslist_url)
    news_heading_elements = util.get_elements_of_type_with_class(soup, "div", "news")
    news_headings = []
    for news_heading_element in news_heading_elements:
        news_heading = refine_news_heading(news_heading_element)
        news_headings.append(news_heading)
    return news_headings

