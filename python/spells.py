import json
import logging
import os
import re
import requests
from scrapy.selector import Selector
from tokens import COBALT_SESSION

_GENERATED_FOLDER = "./generated/"
_HTML_CACHE_FOLDER = _GENERATED_FOLDER + "html-cache/"
_JSON_CACHE_FOLDER = _GENERATED_FOLDER + "json-cache/"
_LOGS_FOLDER = _GENERATED_FOLDER + "logs/"

logging.basicConfig(filename=_LOGS_FOLDER + "spells.log", filemode="a+")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Spell:

    ref_code = {
        "Basic Rules": "PHB",
        "Player's Handbook": "PHB",
        "Elemental Evil Player's Companion" : "XGE",
        "Xanathar's Guide to Everything" : "XGE",
        "Sword Coast Adventurer's Guide" : "SCAG"}

    def __init__(self, name, level, school, casting_time, spell_range, area,
                 area_type, components, materials, duration, description,
                 reference, classes):
        self.name = name
        self.level = level
        self.school = school
        self.casting_time = casting_time
        self.spell_range = spell_range
        self.area = area
        self.area_type = area_type
        self.components = components
        self.materials = materials
        self.duration = duration
        self.description = description
        self.reference = reference
        self.classes = classes

    def __str__(self):
        print(self.name)
        print("level {} {} spell".format(self.level, self.school))
        print("-------------------------------------------------")
        print("CAST {}".format(self.casting_time))
        print("RANGE {} / {} {}".format(self.spell_range, self.area, self.area_type))
        print("DURATION {}".format(self.duration))
        print("{} ({})".format(self.components, self.materials))
        print("-------------------------------------------------")
        print(self.description)
        print("-------------------------------------------------")
        print(self.reference, self.classes)
        return ""

    @staticmethod
    def extract_name(dom):
        return dom.css(".page-title::text").extract_first().strip()

    @staticmethod
    def extract_level(dom):
        return dom.css(".ddb-statblock-item-level .ddb-statblock-item-value::text").extract_first().strip()[0]

    @staticmethod
    def extract_school(dom):
        return dom.css(".ddb-statblock-item-school .ddb-statblock-item-value::text").extract_first().strip()

    @staticmethod
    def extract_casting_time(dom):
        return dom.css(".ddb-statblock-item-casting-time .ddb-statblock-item-value::text").extract_first().strip()

    @staticmethod
    def extract_spell_range(dom):
        return dom.css(".ddb-statblock-item-range-area .ddb-statblock-item-value::text").extract_first().strip()

    @staticmethod
    def extract_area(dom):
        area = dom.css(".aoe-size::text").extract_first()
        return area.strip()[1:] if area else None

    @staticmethod
    def extract_area_type(dom):
        area_type = dom.css(".aoe-size").extract_first()
        if area_type:
            area_type = re.search("<i class=\"i-aoe-(\w+)\"", area_type.strip()).group(1)
            return area_type
        return None

    @staticmethod
    def extract_components(dom):
        return dom.css(".component-asterisks::text").extract_first().strip()[:-1]

    @staticmethod
    def extract_materials(dom):
        materials = dom.css(".components-blurb::text").extract_first()
        return materials.strip()[5:-1] if materials else None

    @staticmethod
    def extract_duration(dom):
        return dom.css(".ddb-statblock-item-duration .ddb-statblock-item-value::text").extract_first().strip()

    @staticmethod
    def extract_description(dom):
        description = "".join("{}\n\n".format(p) for p in dom.css(".more-info-content p").extract())
        description = re.sub("<.+?>", '', description)
        return description

    @staticmethod
    def extract_reference(dom):
        book = dom.css(".spell-source::text").extract_first().strip()
        page = dom.css(".page-number::text").extract_first()
        page = re.search("\d+", page.strip()).group(0) if page else "?"
        if book in Spell.ref_code:
            return "{} {}".format(Spell.ref_code[book], page)
        else:
            logger.info("Unknown reference : {}".format(book))
            return "UNK {}".format(page)

    @staticmethod
    def extract_classes(dom):
        return [c.lower() for c in dom.css(".class-tag::text").extract()]



def html_to_json(html, jsonfile):
    """
    Converts a spell described in a DDB html file
    into a json file.
    """
    dom = Selector(text=html)

    name = Spell.extract_name(dom)

    try:
        level = Spell.extract_level(dom)
    except:
        level = "?"
        logger.info("BAD FORMAT : The level of '{}' is unknown".format(name))

    try:
        school = Spell.extract_school(dom)
    except:
        school = "DM choice"
        logger.info("BAD FORMAT  : The school of '{}' is unknown".format(name))

    try:
        casting_time = Spell.extract_casting_time(dom)
    except:
        casting_time = "DM choice"
        logger.info("BAD FORMAT  : The casting time  of '{}' is unknown".format(name))

    try:
        spell_range = Spell.extract_spell_range(dom)
    except:
        spell_range = "DM choice"
        logger.info("BAD FORMAT  : The range of '{}' is unknown".format(name))

    try:
        area = Spell.extract_area(dom)
    except:
        "DM choice"
        logger.info("BAD FORMAT  : The area size of '{}' is unknown".format(name))

    try:
        area_type = Spell.extract_area_type(dom)
    except:
        area_type = None
        logger.info("BAD FORMAT : Area type of '{}' is unknown".format(name))

    try:
        components = Spell.extract_components(dom)
    except:
        components = "DM choice"
        logger.info("BAD FORMAT : Components of '{}' are unknown".format(name))

    try:
        materials = Spell.extract_materials(dom)
    except:
        materials = "DM choice"
        logger.info("BAD FORMAT : materials of '{}' are unknown".format(name))

    try:
        duration = Spell.extract_duration(dom)
    except:
        duration = "DM choice"
        logger.info("BAD FORMAT : Duration of '{}' is unknown".format(name))

    try:
        description = Spell.extract_description(dom)
    except:
        description = "DESCRIPTION PLACEHOLDER"
        logger.info("BAD FORMAT : Description of '{}' could not be found".format(name))

    try:
        reference = Spell.extract_reference(dom)
    except:
        reference = "UNK"
        logger.info("BAD FORMAT : Reference of '{}' is unknown".format(name))

    try:
        classes = Spell.extract_classes(dom)
    except:
        classes = []
        logger.info("BAD FORMAT : Classes of '{}' could not be parsed".format(name))

    spell = Spell(name, level, school, casting_time, spell_range, area,
                  area_type, components, materials, duration, description,
                  reference, classes)

    with open(_JSON_CACHE_FOLDER + jsonfile, "w+") as j:
        json.dump(spell.__dict__, j)


def jsonify():
    for _, _, files in os.walk(_HTML_CACHE_FOLDER):
        for name in files:
            with open(_HTML_CACHE_FOLDER + name) as f:
                html_to_json(f.read(), name.replace(".html", ".json"))
