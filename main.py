from spells import Spell
import cards

if __name__ == "__main__":
    #spell = Spell.get_spell("Abi-Dalzim’s Horrid Wilting")
    spell = Spell.get_spell("Sleep")
    cards.create_spell_card(spell)
