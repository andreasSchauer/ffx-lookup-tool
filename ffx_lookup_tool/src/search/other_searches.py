from ffx_lookup_tool.src.data import primers, celestials, monsters, monster_arena, rewards, items
from ffx_lookup_tool.src.constants import RONSO_RAGES, ITEM_CATEGORIES
from ffx_lookup_tool.src.utilities.misc import initialize_table, initialize_wrapper_table, console, format_item, format_string
from ffx_lookup_tool.src.utilities.select import select
from ffx_lookup_tool.src.utilities.short_mon_table import get_short_mon_table


def get_primer_table():
    wrapper_table = initialize_wrapper_table("Al Bhed Primers")
    primer_table = initialize_table("", 3, column_names=["Primer", "Translation", "Location"])
    wrapper_table.add_row(primer_table)

    for primer in primers:
        num = primer["num"]
        translation = primer["translation"]
        location = primer["location"]

        if isinstance(location, list):
            location = " / ".join(location)

        primer_table.add_row(num, translation, location)

    console.print(wrapper_table)


def get_celestial_table():
    wrapper_table = initialize_wrapper_table("Celestial Items and Weapons")
    celestial_table = initialize_table("", 2, column_names=["Item / Weapon", "Location"])
    wrapper_table.add_row(celestial_table)

    for celestial in celestials:
        item = format_string(celestial["item"])
        location = celestial["location"]
        celestial_table.add_row(item, location)

    console.print(wrapper_table)



def ronso_rage_search(ronso_rage):
    if ronso_rage not in RONSO_RAGES:
        ronso_rage = select("rage", "Rage not found.")
    
    title = format_string(ronso_rage)
    ronso_table = initialize_wrapper_table(title)

    monster_list = get_rage_monsters(ronso_rage)

    for monster in monster_list:
        ronso_table.add_row(get_short_mon_table(monster))

    console.print(ronso_table)


def get_rage_monsters(ronso_rage):
    monster_list = []

    for monster_name in monsters.keys():
        monster = monsters[monster_name]
        rage = monster["ronso_rage"]

        if rage is not None and (rage == ronso_rage or ronso_rage in rage):
            monster_list.append(monster_name)

    return monster_list



def arena_creation_search(creation_name):
    if creation_name not in monster_arena:
        creation_name = select("creation", "Creation not found.")

    creation = monster_arena[creation_name]
    
    title = format_string(creation_name)
    monster_table = initialize_wrapper_table(title)
    monster_table.add_row(get_short_mon_table(creation_name))

    if "monsters" in creation:
        for monster_name in creation["monsters"]:
            monster_table.add_row(get_short_mon_table(monster_name))

    console.print(monster_table)



def get_reward_table(**conditions):
    if not any(conditions.values()):
        conditions = {key: True for key in conditions}

    reward_table = initialize_wrapper_table("Rewards")

    for key in conditions.keys():
        if conditions[key]:
            reward_table.add_row(get_rewards(key))

    console.print(reward_table)


def get_rewards(key):
    reward_list = rewards[key]["data"]
    title = rewards[key]["title"]
    first_col_title = rewards[key]["first_col_title"]

    table = initialize_table(title, 2, column_names=[first_col_title, "Reward"])

    for reward in reward_list:
        table.add_row(reward["condition"], format_item(reward["reward"]))

    return table



def get_items_table(**conditions):
    if not any(conditions.values()):
        conditions = {key: True for key in conditions}

    items_table = initialize_wrapper_table("Items")

    for key in conditions.keys():
        if conditions[key]:
            items_table.add_row(get_items(key))

    console.print(items_table)


def get_items(key):
    category = ITEM_CATEGORIES[key]
    items_list = list(items.keys())[category[0]:category[1]]
    title = format_string(key)

    table = initialize_table(title, 2, column_names=["Item", "Effect"])

    for i in range(len(items_list)):
        item = items_list[i]
        effect = items[item]
        table.add_row(format_string(item), effect)

    return table