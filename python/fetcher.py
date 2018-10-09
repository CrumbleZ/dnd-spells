import re
import requests
from itertools import count
from os.path import isfile
from random import choice as random_choice
from scrapy.selector import Selector
from time import sleep
from tokens import COBALT_SESSION
from utils import random_user_agent, sanitize_spell_name


_CLEAR_LINE = "\033[K"

_DDB = "https://www.dndbeyond.com"
_DDB_SPELLS = _DDB + "/spells"

_GENERATED_FOLDER = "./generated/"
_HTML_CACHE_FOLDER = _GENERATED_FOLDER + "html-cache/"
_SPELLS_LIST = "spells_list.lst"


def update_spell_list():
    """
    Fetches every spell name on ddb and stores them in a file.
    """

    # Fetches all spell names on DDB
    spells = []
    dom = Selector(response=requests.get(_DDB_SPELLS))

    while True:
        for spell in dom.css(".name .link::text").extract():
            spells.append(spell)

        next_page = dom.css(".b-pagination-item-next a::attr(href)").extract_first()

        if next_page is not None:
            print(_CLEAR_LINE + "Updating " + next_page, end="\r", flush=True)

            try:
                dom = Selector(response=requests.get(_DDB + next_page))
                continue
            except:
                print("An error occured while fetching spells")
                raise
        break
    print("\nDone updating spells list")

    # Store all fetched spells in a list file
    with open(_GENERATED_FOLDER + _SPELLS_LIST, "w+") as f:
        for spell in spells:
            f.write(spell + "\n")

def get_spell(name, overwrite_existing=False):
    """
    Fetches the given spell and stores its html content into
    a download cache folder.
    """
    #Sanitize the spell's name for url's and filenames
    name = name.strip()
    sanitized_name = sanitize_spell_name(name)

    #Check if the spell is already cached
    if not overwrite_existing:
        if isfile(_HTML_CACHE_FOLDER + sanitized_name + ".html"):
            return

    #Otherwise download it and cache it
    spell_url = _DDB_SPELLS + "/" + sanitized_name
    headers = {
        "User-Agent": random_user_agent(),
        "cookie":"CobaltSession=" + COBALT_SESSION,
    }
    response = requests.get(spell_url, headers=headers)
    if response.status_code == 200:
        dom = Selector(response=response)
        with open(_HTML_CACHE_FOLDER + sanitized_name + ".html", "w+") as html:
            html.write("<h1 class=\"page-title\">{}</h1>\n".format(name))
            html.write(dom.css(".details-more-info").extract_first())
    else:
        print("Failed to fetch {} with status code {}".format(name, response.status_code))

    #Road bump for request, trying to prevent getting blocked
    sleep(.5)

def get_all_spells(overwrite_existing=False):
    with open(_GENERATED_FOLDER + _SPELLS_LIST, "r") as spells_list:
        for spell_name in spells_list:
            print(_CLEAR_LINE + " " * 80, end="\r", flush=True)
            print(_CLEAR_LINE + "Fetching : " + spell_name, end="\r", flush=True)
            get_spell(spell_name, overwrite_existing)
