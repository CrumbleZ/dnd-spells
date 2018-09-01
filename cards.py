import os
from spells import Spell

def make_paths(spell):
    """
    Verify that the appropriate folders exists for each class that can use
    the spell. Creates the folders if they do not exist
    """
    for dnd_class in spell.classes:
        dirname = "./latex/generated/{}".format(dnd_class.replace(' ', '-'))
        if not os.path.exists(dirname):
            os.makedirs(dirname)

def write_preamble(file):
    """
    Place the LaTeX pre-written preamble in top of the spell file
    for it to compile with the LuaLaTeX engine
    """
    with open("./latex/fillers/spell-preamble.tex") as preamble:
        file.write(preamble.read())

def write_spell_header(file, spell):
    """
    The spell header of the card consists of :
        the spell name, the spell level, the spell school and the spell
        complimentary tag (ritual, feature) if it exists
    """

    with open("./latex/fillers/header-filler.tex") as filler:
        text = filler.read()

    text = text.replace("<school>", spell.school.lower())
    text = text = text.replace("<name>", spell.name)
    text = text.replace("<level>", spell.level)

    #TODO : CHECK RITUAL OR FEATURE TRAIT

    if spell.level == 0:
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

    with open("./latex/fillers/requirements-filler.tex") as filler:
        text = filler.read()

    components = ""
    components += "\\verbal " if "V" in spell.components else "\\nverbal "
    components += "\\somatic " if "S" in spell.components else "\\nosomatic "
    components += "\\material" if "M" in spell.components else "\\nmaterial"

    text = text.replace("<casttime>", spell.casting_time)
    text = text.replace("<rage>", spell.spell_range)
    text = text.replace("<duration>", spell.duration)
    text = text.replace("<components>", components)

    if spell.materials is not None:
        text = text.replace("<materials", spell.materials)

    if spell.area is not None:
        text = text.replace("<area>", "\\area{{{}}}{{{}}}".format(spell.area, spell.area_type))

    file.write(text + "\n\n")

def write_spell_details(file, spell):
    """
    The spell details of the card consists of :
        the spell description and its reference w/o the spell upgrade details
    """

    with open("./latex/fillers/details-filler.tex") as filler:
        text = filler.read()

    #TODO : IMPORTANT manage text length
    text = text.replace("<description>", spell.description)
    text = text.replace("<reference>", spell.reference)

    file.write(text + "\n\n")

def write_spell_upgrade(file, spell):
    """
    The spell upgrade of the card consists of :
        the upgrade details of the spell based on the player level or
        the spell slot used

    The footer exists if and only if the upgrade exists
    """
    return None


def create_spell_card(spell):
    make_paths(spell)
    dnd_class = spell.classes[0].replace(' ', '-')
    filename = "./latex/{}/{}-{}.tex".format(dnd_class, spell.level, spell.dirname())

    with open(filename, "w+") as spell_file:
        write_preamble(spell_file)
        spell_file.write("\n\n\\begin{document}\n\n")

        write_spell_header(spell_file, spell)
        write_spell_requirements(spell_file, spell)
        write_spell_details(spell_file, spell)
        write_spell_upgrade(spell_file, spell)

        spell_file.write("\\end{document}\n")
    #TODO : Create spell upgrade footer if it exists
