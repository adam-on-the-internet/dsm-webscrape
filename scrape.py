from util import workflow_util
from jobs.scrape_council_meetings import get_council_meetings
from jobs.scrape_news_posts import get_news_posts
from jobs.scrape_calendar import get_calendar_events
from jobs.scrape_agendas import get_agendas


def run_scrape():
    print()
    print("# Beginning Scrape...")
    item_count = find_items()
    print_conclusion(item_count)


def find_items():
    print(" - Looking for News Posts...")
    news_posts = get_news_posts()

    print(" - Looking for Calendar Events...")
    calendar_events = get_calendar_events()

    print(" - Looking for Council Meetings...")
    council_meetings = get_council_meetings()

    print(" - Looking for Council Meeting Agendas...")
    agendas = get_agendas()

    # TODO add more scrape elements

    item_count = len(news_posts) + len(council_meetings) + len(calendar_events) + len(agendas)
    return item_count


def print_conclusion(item_count):
    setup_env_for_updates(item_count)
    if item_count > 0:
        print()
        print(f"!! Found {item_count} updated item(s) !!")
        print("!! Details: https://www.dsmpeoplestownhall.com/#/dsm-city-updates !!")
    else:
        print()
        print(".. No updated items found ..")
        print(".. Done ..")


def setup_env_for_updates(item_count):
    print()
    workflow_util.set_env_output("COUNT", item_count)
    workflow_util.set_env_output("FOUND_UPDATE", item_count > 0)

