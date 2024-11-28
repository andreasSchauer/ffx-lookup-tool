from ffx_lookup_tool.src.data import aeon_abilities, armour_abilities, weapon_abilities
from ffx_lookup_tool.src.search.item_search import get_item_table
from ffx_lookup_tool.src.constants import CHARACTER_SPECIFIC_ABILITIES
from ffx_lookup_tool.src.utilities.format_item_data import format_ability_item_data
from ffx_lookup_tool.src.utilities.key_search_table.key_search_table import get_key_search_table, key_search_table_title
from ffx_lookup_tool.src.utilities.misc import initialize_wrapper_table, console, initialize_table, format_string
from ffx_lookup_tool.src.utilities.select import select



def aeon_ability_search(ability_name):
    if ability_name not in aeon_abilities:
        ability_name = select("aeon_ability", "Ability not found.")

    item_name = aeon_abilities[ability_name][0]

    get_aeon_ability_table(ability_name)
    get_item_table(item_name)



def get_aeon_ability_table(ability_name):
    title = format_string(ability_name)
    table = initialize_wrapper_table(title)

    data = format_ability_item_data(ability_name, "aeon")
    table.add_row(f"Needed to learn: {data}")

    console.print(table)



def auto_ability_search(ability_name):
    if ability_name not in weapon_abilities and ability_name not in armour_abilities:
        ability_name = select("auto_ability", "Ability not found.")

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



def get_auto_ability_table(ability_name, ability_type):
    title = ability_title(ability_name, ability_type)
    table = initialize_wrapper_table(title)

    item_data = format_ability_item_data(ability_name, ability_type)
    table.add_row(get_ability_info_table(ability_name, ability_type, item_data))

    if item_data is not None:
        col_names = ["Reoccurring", "Not Reoccurring", "Bosses"]

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