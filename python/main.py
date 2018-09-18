from spells import Spell
import cards

if __name__ == "__main__":
    #spell = Spell.get_spell("Abi-Dalzim’s Horrid Wilting")
    spell = Spell.get_spell("Arcane Gate")
    cards.create_spell_card(spell)

    #for spell in Spell.get_all_spells():
    #    cards.create_spell_card(spell)
