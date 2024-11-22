from rich import box
from rich.table import Table
from ffx_search_tool.src.data import aeon_abilities, armour_abilities, weapon_abilities
from ffx_search_tool.src.search.item_search import get_item_table
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH
from ffx_search_tool.src.utilities.format_item_data import format_ability_data
from ffx_search_tool.src.utilities.key_search_table import get_key_search_table
from ffx_search_tool.src.utilities.misc import console, make_selection



def aeon_ability_search(ability_name):
    if ability_name not in aeon_abilities:
        options = list(aeon_abilities.keys())
        ability_name = make_selection(options, "Ability not found.")

    item_name = aeon_abilities[ability_name][0]

    get_aeon_ability_table(ability_name)
    get_item_table(item_name)



def get_aeon_ability_table(ability_name):
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    table.add_column(ability_name.title())

    data = format_ability_data(ability_name, "aeon")
    table.add_row(f"Needed to learn: {data}")

    console.print(table)



def auto_ability_search(ability_name):
    if ability_name not in weapon_abilities and ability_name not in armour_abilities:
        ability_name = select_ability()

    if ability_name in weapon_abilities:
        ability_type = "weapon"
        ability_data = weapon_abilities

    if ability_name in armour_abilities:
        ability_type = "armour"
        ability_data = armour_abilities

    get_auto_ability_table(ability_name, ability_type)

    items = ability_data[ability_name]["items"]

    if items is not None:
        item_name = ability_data[ability_name]["items"][0]
        get_item_table(item_name)



def select_ability():
    choice = make_selection(["weapon abilities", "armour abilities"], "Ability not found.", input_msg="Display abilities for weapons or armours?\nChoose by number: ")

    if choice == "weapon abilities":
        options = list(weapon_abilities.keys())

    if choice == "armour abilities":
        options = list(armour_abilities.keys())

    ability_name = make_selection(options, "Now, choose the ability by number: ")

    return ability_name



def get_auto_ability_table(ability_name, ability_type):
    title = ability_title(ability_name, ability_type)
    description = ability_description(ability_name, ability_type)

    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    table.add_column(title)
    table.add_row(description)

    item_data = format_ability_data(ability_name, ability_type)

    if item_data is not None:
        table.add_row(f"Needed to customize: {item_data}")
        table.add_row(get_key_search_table(ability_name, "equipment", ["Reoccurring", "Not Reoccurring", "Bosses"]))
    else:
        alt_text = text_non_customizable(ability_name)
        table.add_row(f"Can't be customized. {alt_text}")

    console.print(table)



def ability_title(ability_name, ability_type):
    return f"{ability_name} ({ability_type}-Ability)".title()


def ability_description(ability_name, ability_type):
    if ability_type == "weapon":
        description = weapon_abilities[ability_name]["description"]

    if ability_type == "armour":
        description = armour_abilities[ability_name]["description"]

    return f"Effect: {description}"



def text_non_customizable(ability_name):
    if ability_name == "capture":
        return "Only available in the Monster Arena Weapon Shop."

    if ability_name == "no ap":
        return "Default Ability on non-upgraded Celestial Weapons."
