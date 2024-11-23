from rich.table import Table
from rich import box
from ffx_search_tool.src.data import primers, celestials, monsters, monster_arena, rewards
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH, RONSO_RAGES
from ffx_search_tool.src.utilities.misc import initialize_table, console, make_selection, format_item
from ffx_search_tool.src.utilities.short_mon_table import get_short_mon_table


def get_primer_table():
    wrapper_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    wrapper_table.add_column("Al Bhed Primers")
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
    wrapper_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    wrapper_table.add_column("Celestial Items and Weapons")
    celestial_table = initialize_table("", 2, column_names=["Item / Weapon", "Location"])
    wrapper_table.add_row(celestial_table)

    for celestial in celestials:
        item = celestial["item"].title()
        location = celestial["location"]
        celestial_table.add_row(item, location)

    console.print(wrapper_table)



def ronso_rage_search(ronso_rage):
    if ronso_rage not in RONSO_RAGES:
        ronso_rage = make_selection(RONSO_RAGES, "Rage not found.")
    
    ronso_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    ronso_table.add_column(ronso_rage.title())

    monster_list = []

    for monster_key in monsters.keys():
        monster = monsters[monster_key]
        rage = monster["ronso_rage"]

        if rage is not None and (rage == ronso_rage or ronso_rage in rage):
            monster_list.append(monster_key)

    for monster in monster_list:
        ronso_table.add_row(get_short_mon_table(monster))

    console.print(ronso_table)



def get_monster_arena_table(creation_name):
    if creation_name not in monster_arena:
        options = list(monster_arena.keys())
        creation_name = make_selection(options, "Creation not found.")

    creation = monster_arena[creation_name]
    
    monster_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    monster_table.add_column(creation_name.title())
    monster_table.add_row(get_short_mon_table(creation_name))

    if "monsters" in creation:
        for monster_name in creation["monsters"]:
            monster_table.add_row(get_short_mon_table(monster_name))

    console.print(monster_table)



def get_reward_table(**conditions):
    if not any(conditions.values()):
        conditions = {key: True for key in conditions}

    reward_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    reward_table.add_column("Rewards")

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