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
    return util.post_json(url, news_post_json)


def refine_news_heading(news_heading_element):
    date = util.get_first_text_of_type_with_class(news_heading_element, "div", "news-date")
    title = util.get_first_text_of_type_with_class(news_heading_element, "h3", "news-title")
    url = util.get_first_link(news_heading_element)
    news_heading = NewsHeading(title, url, date)
    return news_heading


def get_discovered_news_headings(news_headings):
    # TODO actually decide which are "new"
    new_news_headings = [news_headings[0]]
    return new_news_headings


def get_news_posts_for_headings(new_news_headings):
    posts = []
    for heading in new_news_headings:
        page_url = f"https://www.dsm.city/{heading.url}"
        soup = util.convert_url_to_soup(page_url)
        page_title = util.get_first_text_of_type_with_id(soup, "h2", "page-title")
        page_content = util.get_elements_of_type_with_id(soup, "div", "post")[0]

        # TODO can we strip out the comments?
        util.remove_script(page_content)
        util.remove_divs_with_class(page_content, "editcenterBtns")
        post = NewsPost(heading.title, heading.url, heading.date, page_title, page_url, page_content)
        posts.append(post)
    return posts


def get_news_headings():
    dsm_newslist_url = 'https://www.dsm.city/newslist.php'
    soup = util.convert_url_to_soup(dsm_newslist_url)
    news_heading_elements = util.get_elements_of_type_with_class(soup, "div", "news")
    news_headings = []
    for news_heading_element in news_heading_elements:
        news_heading = refine_news_heading(news_heading_element)
        news_headings.append(news_heading)
    return news_headings

