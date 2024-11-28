from ffx_lookup_tool.src.data import monsters, monster_arena, remiem_temple
from ffx_lookup_tool.src.constants import DUPLICATES, SYNONYMS, MONSTER_TABLE_CELL_NAMES
from ffx_lookup_tool.src.utilities.format_monster_data import format_monster_data
from ffx_lookup_tool.src.utilities.select import select
from ffx_lookup_tool.src.utilities.misc import initialize_table, initialize_wrapper_table, console, format_num, format_string
from ffx_lookup_tool.src.utilities.ronso_calc import *
import sys



def monster_search(monster_name, include_allies=False):
    monster_name = validate_monster_name(monster_name, include_allies)
    kimahri_stats = validate_ronso_cases(monster_name)
    monster = monsters[monster_name]
    
    if monster["has_allies"] and include_allies:
        get_ally_tables(monster_name, kimahri_stats)
    else:
        get_monster_table(monster_name, kimahri_stats)


def validate_monster_name(monster_name, include_allies=False):
    monster_synonyms = None
    
    if monster_name in SYNONYMS:
        monster_synonyms = SYNONYMS[monster_name]

        if include_allies:
            monster_name = monster_synonyms[0]
        else:
            print_synonyms(monster_synonyms)
            sys.exit()

    if monster_name in DUPLICATES:
        monster_name = select("duplicate", "Multiple options found.", monster_name)

    if monster_name not in monsters and monster_synonyms is None:
        monster_name = select("monster", "Monster not found.")

    return monster_name


def print_synonyms(monster_synonyms):
    for synonym in monster_synonyms:
        get_monster_table(synonym)


def validate_ronso_cases(monster_name):
    if monster_name == "biran ronso" or monster_name == "yenke ronso":
        return get_kimahri_stats()

    return None


def get_monster_table(monster_name, kimahri_stats=None):
    monster = monsters[monster_name]
    title = get_monster_table_title(monster_name)
    table = initialize_wrapper_table(title)

    table.add_row(get_stat_table(monster_name, kimahri_stats))
    table.add_row(get_element_table(monster_name))
    table.add_row(get_status_resist_table(monster_name))
    table.add_row(get_item_table(monster_name))

    if monster["items"]["bribe"] is not None:
        table.add_row(get_bribe_table(monster_name))

    if monster["equipment"]["drop_rate"] != 0:
        table.add_row(get_equipment_table(monster_name))

    if monster_name in monster_arena:
        table.add_row(get_arena_table(monster_name))

    if monster_name in remiem_temple:
        table.add_row(get_remiem_table(monster_name))

    console.print(table)


def get_monster_table_title(monster_name):
    monster = monsters[monster_name]
    locations = ", ".join(monster["location"])
    title = format_string(f"{monster_name} - {locations}")

    if monster["is_catchable"]:
        title += " - Can be captured"

    return title


def get_ally_tables(monster_name, kimahri_stats=None):
    monster = monsters[monster_name]
    allies = monster["allies"]
    monster_in_multiple_fights = isinstance(allies[0], list)

    if monster_in_multiple_fights:
        ally = select("boss_fight", "Monster appears in multiple boss fights.", monster_name)
        monster_search(ally)
        sys.exit()

    for ally in allies:
        if kimahri_stats is not None:
            get_monster_table(ally, kimahri_stats)
        else:
            get_monster_table(ally)



def get_stat_table(monster_name, kimahri_stats=None):
    monster = monsters[monster_name]
    stats = monster.copy()["stats"]
    stat_keys = list(stats.keys())
    stat_cell_names = MONSTER_TABLE_CELL_NAMES["stats"]

    stat_table = initialize_table("Stats", 4, tab_header=False)

    if kimahri_stats is not None:
        stats["hp"] = get_ronso_hp(monster_name, kimahri_stats["str"], kimahri_stats["mag"])
        stats["strength"] = get_ronso_strength(monster_name, kimahri_stats["hp"])
        stats["magic"] = get_ronso_magic(monster_name, kimahri_stats["hp"])
        stats["agility"] = get_ronso_agility(monster_name, kimahri_stats["agl"])

    for i in range(0, len(stats), 2):
        left_stat = stat_cell_names[i]
        right_stat = stat_cell_names[i+1]
        left_val = format_monster_data(stat_keys[i], monster_name)
        right_val = format_monster_data(stat_keys[i+1], monster_name)
        
        stat_table.add_row(left_stat, left_val, right_stat, right_val)

    return stat_table



def get_element_table(monster_name):
    monster = monsters[monster_name]
    elements = monster["elem_resists"]
    element_keys = list(elements.keys())
    element_cell_names = MONSTER_TABLE_CELL_NAMES["elements"]

    col_names = ["Element", "Resistance"]
    element_table = initialize_table("Elemental Resistances", 4, column_names=col_names)

    for i in range(0, len(elements), 2):
        left_element = element_cell_names[i]
        right_element = element_cell_names[i+1]
        left_resist = format_monster_data(element_keys[i], monster_name)
        right_resist = format_monster_data(element_keys[i+1], monster_name)

        element_table.add_row(left_element, left_resist, right_element, right_resist)

    return element_table
     


def get_status_resist_table(monster_name):
    monster = monsters[monster_name]
    statusses = monster["stat_resists"]
    status_keys = list(statusses.keys())
    status_cell_names = MONSTER_TABLE_CELL_NAMES["statusses"]

    col_names = ["Status", "Resistance"]
    status_table = initialize_table("Status Resistances", 4, column_names=col_names)

    for i in range(0, len(statusses), 2):
        left_status = status_cell_names[i]
        right_status = status_cell_names[i+1]
        left_resist = format_monster_data(status_keys[i], monster_name)
        right_resist = format_monster_data(status_keys[i+1], monster_name)
        
        status_table.add_row(left_status, left_resist, right_status, right_resist)

    return status_table



def get_item_table(monster_name):
    item_table = initialize_table("Items and Loot", 2, tab_header=False)
    item_table.add_row("AP (Overkill)", format_monster_data("ap", monster_name))
    item_table.add_row("Gil", format_monster_data("gil", monster_name))
    item_table.add_row("Ronso Rage", format_monster_data("ronso_rage", monster_name))

    monster = monsters[monster_name]
    items = monster["items"]
    item_keys = list(items.keys())
    item_cell_names = MONSTER_TABLE_CELL_NAMES["items"]

    for i in range(len(items)):
        action = item_cell_names[i]
        key = item_keys[i]

        if items[key] is None:
            continue

        item = format_monster_data(key, monster_name)
        item_table.add_row(action, item)

    return item_table



def get_bribe_table(monster_name):
    monster = monsters[monster_name]
    
    hp = monster["stats"]["hp"][0]
    hp_factor = 10
    probability = 25

    col_names = ["Amount in Gil", "Success Rate"]
    bribe_table = initialize_table("Bribe Success Rate", 2, column_names=col_names)

    while probability <= 100:
        bribe_amount = format_num(hp * hp_factor)
        bribe_table.add_row(f"{bribe_amount}", f"{probability}%")
        hp_factor += 5
        probability += 25

    return bribe_table



def get_equipment_table(monster_name):
    monster = monsters[monster_name]    
    equipment = monster["equipment"]
    equipment_keys = list(equipment.keys())
    equipment_cell_names = MONSTER_TABLE_CELL_NAMES["equipment"]

    equipment_table = initialize_table("Equipment", 2, tab_header=False)

    for i in range(len(equipment)):
        name = equipment_cell_names[i]
        data = format_monster_data(equipment_keys[i], monster_name)
        equipment_table.add_row(name, data)

    return equipment_table



def get_arena_table(monster_name):
    monster = monster_arena[monster_name]
    arena_table = initialize_table("Monster Arena Reward", 2, tab_header=False)

    arena_table.add_row("Unlock Condition", format_monster_data("condition", monster_name))

    if "monsters" in monster:
        arena_table.add_row("Monsters To Catch", format_monster_data("monsters", monster_name))

    arena_table.add_row("Reward", format_monster_data("reward", monster_name))

    return arena_table



def get_remiem_table(monster_name):
    remiem_table = initialize_table("Battle Rewards", 2, tab_header=False)
    remiem_table.add_row("First Victory Reward", format_monster_data("first reward", monster_name))
    remiem_table.add_row("Recurring Victory Reward", format_monster_data("recurring reward", monster_name))

    return remiem_table