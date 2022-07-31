import util
from models.NewsHeading import NewsHeading


def refine_news_heading(news_heading_element):
    date = util.get_first_text_of_type_with_class(news_heading_element, "div", "news-date")
    title = util.get_first_text_of_type_with_class(news_heading_element, "h3", "news-title")
    url = util.get_first_link(news_heading_element)
    news_heading = NewsHeading(title, url, date)
    return news_heading


def get_press_releases():
    print("## Starting to get press releases")

    dsm_newslist_url = 'https://www.dsm.city/newslist.php'
    soup = util.convert_url_to_soup(dsm_newslist_url)
    news_heading_elements = util.get_elements_of_type_with_class(soup, "div", "news")
    print(f" - Found {len(news_heading_elements)} news headings")

    news_headings = []
    for news_heading_element in news_heading_elements:
        news_heading = refine_news_heading(news_heading_element)
        news_headings.append(news_heading)

    print("## Done getting press releases")

    press_releases = []
    return press_releases

