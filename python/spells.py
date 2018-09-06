
import re, os
import requests
from scrapy.selector import Selector

class Spell:

    _GENERATED_FOLDER = "./generated/"
    _DL_CACHE_FOLDER = _GENERATED_FOLDER + "dl_cache/"
    _SPELL_HTML_CACHE = _DL_CACHE_FOLDER + "spells.html"

    def __init__(self, name, level, school, casting_time, spell_range, area, area_type,
                 components, materials, duration, description, reference, classes):
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

    def dirname(self):
        return re.sub("[^-a-zA-Z0-9\ ]", '', self.name).lower().replace(" ", "-")

    @staticmethod
    def url_name(name):
        name = re.sub("[^-a-zA-Z0-9\ ]", '', spell_name)
        return name.lower().replace(" ", "-")

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
        ref_code = {"Basic Rules": "PHB","Elemental Evil Player's Companion" : "XGE",}
        return "{} {}".format(ref_code[book], page)

    @staticmethod
    def extract_classes(dom):
        return [c.lower() for c in dom.css(".class-tag::text").extract()]

    @staticmethod
    def get_spell(spell_name):
<<<<<<< HEAD
        """fetches a spell on dndbeyond.com
        caches the request for future use"""

        if os.path.isfile(Spell._SPELL_HTML_CACHE):
            with open(Spell._SPELL_HTML_CACHE) as f:
                dom = Selector(text=f.read())
        else:
            spell_name = re.sub("[^-a-zA-Z0-9\ ]", '', spell_name)
            spell_name = spell_name.lower().replace(" ", "-")
            spell_url = "https://www.dndbeyond.com/spells/{}".format(spell_name)
            response = requests.get(spell_url)
            with open(Spell._SPELL_HTML_CACHE, "w+") as f:
                f.write(response.text)
            dom = Selector(response=response)

=======
        """fetches a spell on dndbeyond.com"""
        print("---- Spell object : " + spell_name)
        spell_name = re.sub("[^-a-zA-Z0-9\ ]", '', spell_name)
        spell_name = spell_name.lower().replace(" ", "-")
        spell_url = "https://www.dndbeyond.com/spells/{}".format(spell_name)
        response = requests.get(spell_url)

        #source = open("./spell.txt")
        #dom = Selector(text=source.read())
        #source.close()

        dom = Selector(response=response)
>>>>>>> Attempts to fetch all spells
        name = Spell.extract_name(dom)
        level = Spell.extract_level(dom)
        school = Spell.extract_school(dom)
        casting_time = Spell.extract_casting_time(dom)
        spell_range = Spell.extract_spell_range(dom)
        area = Spell.extract_area(dom)
        area_type = Spell.extract_area_type(dom)
        components = Spell.extract_components(dom)
        materials = Spell.extract_materials(dom)
        duration = Spell.extract_duration(dom)
        description = Spell.extract_description(dom)

        reference = Spell.extract_reference(dom)
        classes = Spell.extract_classes(dom)

        return Spell(name, level, school, casting_time, spell_range, area, area_type,
                     components, materials, duration, description, reference, classes)

    @staticmethod
    def get_all_spells():
        spells = set()
        page_number = 1
        flag = True

        while flag:
            print("fetching spell page " + str(page_number))
            spell_page_url = "https://www.dndbeyond.com/spells?page={}".format(page_number)
            dom = Selector(response=requests.get(spell_page_url))

            for spell in dom.css(".name .link::text").extract():
                if spell in spells:
                    flag = False
                    break
                spells.add(Spell.get_spell(spell))

            page_number += 1

        print("done fetching spells")
        return spells
