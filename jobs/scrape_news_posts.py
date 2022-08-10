from repo import news_post_repo
from util import soup_util
from models.News.NewsHeading import NewsHeading
from models.News.NewsPost import NewsPost


def get_news_posts():
    found_news_posts = find_news_posts()
    save_news_posts(found_news_posts)
    return found_news_posts


def save_news_posts(found_news_posts):
    for news_post in found_news_posts:
        news_post_repo.save_news_post(news_post)
        print(f"   + {news_post.get_message()}")


def find_news_posts():
    found_news_headings = find_news_headings()
    return build_news_posts(found_news_headings)


def find_news_headings():
    all_news_headings = get_all_news_headings()
    found_news_headings = get_found_news_headings(all_news_headings)
    return found_news_headings


def build_news_heading(news_heading_element):
    date = soup_util.get_first_text_of_type_with_class(news_heading_element, "div", "news-date")
    title = soup_util.get_first_text_of_type_with_class(news_heading_element, "h3", "news-title")
    partial_url = soup_util.get_first_link(news_heading_element)
    full_url = f"https://www.dsm.city/{partial_url}"
    news_heading = NewsHeading(title, full_url, date)
    return news_heading


def get_found_news_headings(news_headings):
    found_news_headings = []
    existing_urls = news_post_repo.get_news_post_urls()
    for heading in news_headings:
        if heading.url not in existing_urls:
            found_news_headings.append(heading)
    return found_news_headings


def build_news_posts(news_headings):
    news_posts = []
    for news_heading in news_headings:
        news_post = build_news_post(news_heading)
        news_posts.append(news_post)
    return news_posts


def build_news_post(heading):
    heading_title = heading.title
    heading_date = heading.date
    url = heading.url
    page = soup_util.convert_url_to_soup(url)
    page_title = get_page_title(page)
    page_content = get_page_content(page)
    return NewsPost(url, heading_title, heading_date, page_title, page_content)


def get_page_content(page):
    content = soup_util.get_elements_of_type_with_id(page, "div", "post")[0]
    # TODO can we strip out the comments?
    soup_util.remove_script(content)
    soup_util.remove_divs_with_class(content, "editcenterBtns")
    return str(content)


def get_page_title(page):
    return soup_util.get_first_text_of_type_with_id(page, "h2", "page-title")


def get_all_news_headings():
    news_headings = []
    news_heading_elements = scrape_news_headings()
    for news_heading_element in news_heading_elements:
        news_heading = build_news_heading(news_heading_element)
        news_headings.append(news_heading)
    return news_headings


def scrape_news_headings():
    dsm_city_news_post_url = 'https://www.dsm.city/newslist.php'
    page = soup_util.convert_url_to_soup(dsm_city_news_post_url)
    news_heading_elements = soup_util.get_elements_of_type_with_class(page, "div", "news")
    return news_heading_elements

