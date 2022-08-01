from scrape_press_releases import get_press_releases
from scrape_council_meetings import get_council_meetings


def run_scrape():
    press_releases = get_press_releases()
    council_meetings = get_council_meetings()
    # TODO add more scrape elements
    print_conclusion(press_releases, council_meetings)


def print_conclusion(press_releases, council_meetings):
    item_count = len(press_releases) + len(council_meetings)
    print(f" ~~ Found {item_count} new items ~~ ")
