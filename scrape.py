from scrape_press_releases import get_press_releases
from scrape_council_meetings import get_council_meetings


def run_scrape():
    press_releases = get_press_releases()
    council_meetings = get_council_meetings()
    # TODO add more scrape elements
    print_conclusion(press_releases, council_meetings)


def set_env_output(name, value):
    print(f"Output - {name} : {value}")
    print(f"::set-output name={name}::{value}")


def print_conclusion(press_releases, council_meetings):
    item_count = len(press_releases) + len(council_meetings)
    set_env_output("COUNT", item_count)
    set_env_output("FOUND_UPDATE", item_count > 0)
    print(f" ~~ Found {item_count} updated items ~~ ")
