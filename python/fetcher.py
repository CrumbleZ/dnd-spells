import requests
from itertools import count
from scrapy.selector import Selector

_CLEAR_LINE = "\033[K"
_DDB = "https://www.dndbeyond.com"
_GENERATED_FOLDER = "./generated/"
_SPELLS_LIST = "spells_list.lst"


def update_spell_list():
    """
    Fetches every spell name on ddb and stores them in a file.
    """
    # Fetches all spell on DDB
    spells = []
    dom = Selector(response=requests.get(_DDB + "/spells"))

    while True:
        for spell in dom.css(".name .link::text").extract():
            spells.append(spell)

        next_page = dom.css(".b-pagination-item-next a::attr(href)").extract_first()

        if next_page is not None:
            print(_CLEAR_LINE + "Fetching " + next_page, end="\r", flush=True)

            try:
                dom = Selector(response=requests.get(_DDB + next_page))
                continue
            except:
                print("An error occured while fetching spells")
                raise
        break
    print("\nDone fetching spells")

    # Store all fetched spells in a csv file
    with open(_GENERATED_FOLDER + _SPELLS_LIST, "w+") as f:
        for spell in spells:
            f.write(spell + "\n")
