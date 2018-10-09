import json
import os
import re
from shutil import copy as sh_copy
from spells import Spell

_TEXFOLDER = "./../latex/"
_SMALL_BOX = str(2.95)
_BIG_BOX = str(4.35)

_GENERATED_FOLDER = "./generated/"
_JSON_CACHE_FOLDER = _GENERATED_FOLDER + "json-cache/"


def make_paths(spell):
    """
    Verify that the appropriate folders exists for each class that can use
    the spell. Creates the folders if they do not exist
    """
    for dnd_class in spell["classes"]:
        dnd_class = dnd_class.replace(" ", "-")
        dirname = _TEXFOLDER + "generated/{}/".format(dnd_class)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

def write_preamble(file):
    """
    Place the LaTeX pre-written preamble in top of the spell file
    for it to compile with the LuaLaTeX engine
    """
    with open(_TEXFOLDER + "fillers/spell-preamble.tex") as preamble:
        file.write(preamble.read())

def write_spell_header(file, spell):
    """
    The spell header of the card consists of :
        the spell name, the spell level, the spell school and the spell
        complimentary tag (ritual, feature) if it exists
    """

    with open(_TEXFOLDER + "fillers/header-filler.tex") as filler:
        text = filler.read()

    text = text.replace("<school>", spell["school"].lower())
    text = text = text.replace("<name>", spell["name"])
    text = text.replace("<level>", spell["level"])

    #TODO : CHECK RITUAL OR FEATURE TRAIT

    if spell["level"] == 0:
        text = text.replace("<leveltext>", "\\cantriptext")
    else:
        text = text.replace("<leveltext>", "\\spellleveltext")

    file.write(text + "\n\n")

def write_spell_requirements(file, spell):
    """
    The spell requirements of the card consists of :
        the cost, the range and area of effet, the duration as well as
        the verbal, somatic and eventual material components required
    """

    with open(_TEXFOLDER + "fillers/requirements-filler.tex") as filler:
        text = filler.read()

    components = ""
    components += "\\verbal " if "V" in spell["components"] else "\\nverbal "
    components += "\\somatic " if "S" in spell["components"] else "\\nosomatic "
    components += "\\material" if "M" in spell["components"] else "\\nmaterial"

    text = text.replace("<casttime>", spell["casting_time"])
    text = text.replace("<range>", spell["spell_range"])
    text = text.replace("<duration>", spell["duration"])
    text = text.replace("<components>", components)

    if spell["materials"] is not None:
        text = text.replace("<materials>", spell["materials"])

    if spell["area"] is not None:
        text = text.replace("<area>",
               "\\area{{{}}}{{{}}}".format(spell["area"], spell["area_type"]))

    file.write(text + "\n\n")

def write_spell_details(file, spell):
    """
    The spell details of the card consists of :
        the spell description and its reference w/o the spell upgrade details
    """

    with open(_TEXFOLDER + "fillers/details-filler.tex") as filler:
        text = filler.read()

    #Verify if there is a spell upgrade
    match = re.search("(^At Higher Levels\..*$)|(^.*5th.*11th.*17th.*$)", spell["description"], re.MULTILINE)

    if match:
        spell["description"] = spell["description"][:match.start()].strip()
        text = text.replace("<box_height>", _SMALL_BOX)
    else:
        text = text.replace("<box_height>", _BIG_BOX)

    text = text.replace("<description>", spell["description"])
    text = text.replace("<reference>", spell["reference"])

    file.write(text + "\n\n")

    if match:
        write_spell_upgrade(file, match.group(0))


def write_spell_upgrade(file, upgrade_text):
    """
    The spell upgrade of the card consists of :
        the upgrade details of the spell based on the player level or
        the spell slot used

    The footer exists if and only if the upgrade exists
    """
    ## CHECK IF THE UPGRADE IS BASED ON SPELL SLOTS
    if re.search("^At Higher Levels\.", upgrade_text):
        with open(_TEXFOLDER + "fillers/spellslot-upgrade-filler.tex") as filler:
            text = filler.read()

        text = text.replace("<upgrade>", upgrade_text[18:])
    ## OTHERWISE PROCEED WITH THE PLAYER LEVEL UPGRADE
    else:
        with open(_TEXFOLDER + "fillers/player-upgrade-filler.tex") as filler:
            text = filler.read()

        text = text.replace("<1st>", "coucou")
        text = text.replace("<2nd>", "salut")
        text = text.replace("<3rd>", "tafiole")

    file.write(text + "\n\n")

def create_spell_card(spell, filename):
    print("Generating card for : " + spell["name"])
    make_paths(spell)
    dnd_class = spell["classes"][0].replace(' ', '-')
    filename = _TEXFOLDER + "generated/{}/{}-{}".format(dnd_class, spell["level"], filename.replace(".json", ".tex"))

    with open(filename, "w+") as spell_file:
        write_preamble(spell_file)
        spell_file.write("\n\n\\begin{document}\n\n")

        write_spell_header(spell_file, spell)
        write_spell_requirements(spell_file, spell)
        write_spell_details(spell_file, spell)

        spell_file.write("\\end{document}\n")

    for remaining_class in spell["classes"][1:]:
        remaining_class = remaining_class.replace(' ', '-')
        sh_copy(filename, _TEXFOLDER + "generated/{}/".format(remaining_class))

def generate_cards():
    for _, _, files in os.walk(_JSON_CACHE_FOLDER):
        for filename in files:
            with open(_JSON_CACHE_FOLDER + filename) as json_spell:
                spell_data = json.load(json_spell)
                create_spell_card(spell_data, filename)
