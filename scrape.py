from scrape_press_releases import get_press_releases


def run_scrape():
    press_releases = get_press_releases()
    # TODO add more scrape elements
    print_conclusion(press_releases)


def print_conclusion(press_releases):
    item_count = len(press_releases)
    print(f" ~~ Found {item_count} new items ~~ ")
