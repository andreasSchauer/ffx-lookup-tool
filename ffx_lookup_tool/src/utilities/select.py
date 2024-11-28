import sys
from ffx_lookup_tool.src.data import armour_abilities, items, weapon_abilities
from ffx_lookup_tool.src.constants import ITEM_CATEGORIES, LOCATIONS, DUPLICATES, RONSO_RAGES
from ffx_lookup_tool.src.utilities.key_search_table.filter_monsters import filter_monsters
from ffx_lookup_tool.src.data import aeon_abilities, monsters, monster_arena
from itertools import chain
from ffx_lookup_tool.src.utilities.misc import format_string


def select(key, message=None, monster_name=None):
    match (key):
        case "monster":
            return select_monster(message)
        case "duplicate":
            return select_duplicate(monster_name, message)
        case "boss_fight":
            return select_boss_fight(monster_name, message)
        case "location":
            return select_location(message)
        case "item":
            return select_item(message)
        case "auto_ability":
            return select_auto_ability(message)
        case "aeon_ability":
            return select_aeon_ability(message)
        case "creation":
            return select_creation(message)
        case "rage":
            return select_rage(message)



def select_monster(message=None):
    location = make_selection(LOCATIONS, message, "Choose a location by number to display options: ")
    options = list(chain(*filter_monsters(location, "location")))
    return make_selection(options, input_msg="Now choose a monster by number: ")


def select_duplicate(monster_name, message=None):
    options = DUPLICATES[monster_name]
    return make_selection(options, message, "Choose a monster by number: ")


def select_boss_fight(monster_name, message=None):
    allies = monsters[monster_name]["allies"]
    choice = make_selection(allies, message, "Specify the fight by number: ")
    ally = choice[0]
    return ally


def select_location(message=None):
    return make_selection(LOCATIONS, message)


def select_item(message=None):
    category_options = list(ITEM_CATEGORIES.keys())
    category_key = make_selection(category_options, message, "Choose a category by number to display options: ")
    category = ITEM_CATEGORIES[category_key]

    options = list(items.keys())[category[0]:category[1]]
    return make_selection(options, input_msg="Now choose an item by number: ")


def select_auto_ability(message=None):
    choice = make_selection(["weapon abilities", "armour abilities"], message, "Display abilities for weapons or armours?\nChoose by number: ")

    if choice == "weapon abilities":
        options = list(weapon_abilities.keys())

    if choice == "armour abilities":
        options = list(armour_abilities.keys())

    ability_name = make_selection(options, input_msg="Now, choose the ability by number: ")

    return ability_name


def select_aeon_ability(message=None):
    options = list(aeon_abilities.keys())
    return make_selection(options, message)


def select_creation(message=None):
    options = list(monster_arena.keys())
    return make_selection(options, message)


def select_rage(message=None):
    return make_selection(RONSO_RAGES, message)



def make_selection(options, error_msg=None, input_msg="Choose by number: ", retry=False):
    if not retry:
        for i, option in enumerate(options):
            if isinstance(option, list):
                print(format_string(f"{i + 1}: {option[0]}"))
            else:
                print(format_string(f"{i + 1}: {option}"))

    print("")

    if error_msg:
        print(error_msg)

    try:
        choice = int(input(input_msg)) - 1

        if 0 <= choice < len(options):
            return options[choice]
        else:
            raise ValueError

    except ValueError:
        return make_selection(options, "Invalid input.", "Try again: ", retry=True)
    except KeyboardInterrupt:
        print("\nInput cancelled.")
        sys.exit()