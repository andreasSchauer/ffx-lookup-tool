from rich import box
from rich.table import Table
from ffx_search_tool.src.data import aeon_abilities, armour_abilities, weapon_abilities
from ffx_search_tool.src.search.item_search import get_item_table
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH, CHARACTER_SPECIFIC_ABILITIES
from ffx_search_tool.src.utilities.format_item_data import format_ability_item_data
from ffx_search_tool.src.utilities.key_search_table.key_search_table import get_key_search_table, key_search_table_title
from ffx_search_tool.src.utilities.misc import console, make_selection, initialize_table, format_string



def aeon_ability_search(ability_name):
    if ability_name not in aeon_abilities:
        options = list(aeon_abilities.keys())
        ability_name = make_selection(options, "Ability not found.")

    item_name = aeon_abilities[ability_name][0]

    get_aeon_ability_table(ability_name)
    get_item_table(item_name)



def get_aeon_ability_table(ability_name):
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    table.add_column(format_string(ability_name))

    data = format_ability_item_data(ability_name, "aeon")
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
    col_names = ["Reoccurring", "Not Reoccurring", "Bosses"]
    title = ability_title(ability_name, ability_type)
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    table.add_column(title)

    item_data = format_ability_item_data(ability_name, ability_type)
    table.add_row(get_ability_info_table(ability_name, ability_type, item_data))

    if item_data is not None:
        if ability_name in CHARACTER_SPECIFIC_ABILITIES:
            title1 = key_search_table_title(ability_name, "equipment", format_characters=True, include_names=True)
            title2 = key_search_table_title(ability_name, "equipment", format_characters=True)

            table.add_row(get_key_search_table(ability_name, "equipment", col_names, title=title1, characters=True))
            table.add_row(get_key_search_table(ability_name, "equipment", col_names, title=title2))
        else:
            table.add_row(get_key_search_table(ability_name, "equipment", col_names))
        
    console.print(table)



def get_ability_info_table(ability_name, ability_type, item_data):
    table = initialize_table("Basic Info", 2, column_names=["Effect", "Needed to Customize"])
    effect = ability_effect(ability_name, ability_type)
    items_needed = get_customize_text(ability_name, item_data)

    table.add_row(effect, items_needed)

    return table
    


def ability_title(ability_name, ability_type):
    return format_string(f"{ability_name} ({ability_type}-Ability)")


def ability_effect(ability_name, ability_type):
    if ability_type == "weapon":
        description = weapon_abilities[ability_name]["description"]

    if ability_type == "armour":
        description = armour_abilities[ability_name]["description"]

    return description


def get_customize_text(ability_name, item_data):
    if item_data is not None:
        return item_data

    if ability_name == "capture":
        return "Can't be customized. Only available in the Monster Arena Weapon Shop."

    if ability_name == "no ap":
        return "Can't be customized. Default Ability on non-upgraded Celestial Weapons."