from rich.table import Table
from rich import box
from ffx_search_tool.src.data import monster_data
from ffx_search_tool.src.constants import DUPLICATES, PHASES, CELL_NAMES, TABLE_WIDTH
from ffx_search_tool.src.utilities import get_table_data, initialize_table, console
from ffx_search_tool.src.ronso_calc import *



def monster_search(monster_name):
    if monster_name in PHASES:
        monster_name = PHASES[monster_name][0]
    
    if monster_name in DUPLICATES:
        monster_name = select_duplicate(monster_name)

    if monster_name not in monster_data:
        raise Exception("Monster not found.")
    
    monster = monster_data[monster_name]
    
    if monster["has_allies"]:
        get_ally_tables(monster_name)
    else:
        get_monster_table(monster_name)



def select_duplicate(monster_name):
    options = DUPLICATES[monster_name]

    for i, option in enumerate(options):
        print(f"{i + 1}: {option.title()}")

    print("Multiple options found.")
    choice = int(input("Choose a monster by number: ")) - 1

    if 0 <= choice < len(options):
        return options[choice]
    else:
        raise Exception("Invalid input")




def get_monster_table(monster_name, kimahri_hp=0, kimahri_str=0, kimahri_mag=0, kimahri_agl=0):
    monster = monster_data[monster_name]
    locations = ", ".join(monster["location"]).title()
    title = f"{monster_name.title()} - {locations}"

    if monster["is_catchable"]:
        title += " - Catchable"

    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    table.add_column(title)

    table.add_row(get_stat_table(monster_name, kimahri_hp, kimahri_str, kimahri_mag, kimahri_agl))
    table.add_row(get_element_table(monster))
    table.add_row(get_status_resist_table(monster))
    table.add_row(get_item_table(monster))

    if monster["items"]["bribe"] is not None:
        table.add_row(get_bribe_table(monster))

    table.add_row(get_equipment_table(monster))

    console.print(table)



def get_ally_tables(monster_name):
    monster = monster_data[monster_name]
    allies = monster["allies"]
    monster_in_multiple_fights = isinstance(allies[0], list)

    if monster_in_multiple_fights:
        select_boss_fight(allies)
        return
        
    if monster_name == "biran ronso" or monster_name == "yenke ronso":
        kimahri_hp, kimahri_str, kimahri_mag, kimahri_agl = get_kimahri_stats()

    for ally in allies:
        if monster_name == "biran ronso" or monster_name == "yenke ronso":
            get_monster_table(ally, kimahri_hp=kimahri_hp, kimahri_str=kimahri_str, kimahri_mag=kimahri_mag, kimahri_agl=kimahri_agl)
        else:
            get_monster_table(ally)


def select_boss_fight(allies):
    for i, option in enumerate(allies):
        print(f"{i + 1}: {option[0].title()}")

    print("Monster appears in multiple boss fights.")
    choice = int(input("Specify the fight by number: ")) - 1

    if 0 <= choice < len(allies):
        monster_search(allies[choice][0])



def get_stat_table(monster_name, kimahri_hp, kimahri_str, kimahri_mag, kimahri_agl):
    monster = monster_data[monster_name]
    stats = monster.copy()["stats"]
    stat_keys = list(stats.keys())
    stat_cell_names = CELL_NAMES["stats"]

    stat_table = initialize_table("Stats", 4, tab_header=False)

    if monster_name == "biran ronso" or monster_name == "yenke ronso":
        stats["hp"] = get_ronso_hp(monster_name, kimahri_str, kimahri_mag)
        stats["strength"] = get_ronso_strength(monster_name, kimahri_hp)
        stats["magic"] = get_ronso_magic(monster_name, kimahri_hp)
        stats["agility"] = get_ronso_agility(monster_name, kimahri_agl)

    for i in range(0, len(stats), 2):
        left_stat = stat_cell_names[i]
        right_stat = stat_cell_names[i+1]
        left_val = get_table_data(stat_keys[i], monster)
        right_val = get_table_data(stat_keys[i+1], monster)
        
        stat_table.add_row(left_stat, left_val, right_stat, right_val)

    return stat_table



def get_element_table(monster):
    elements = monster["elem_resists"]
    element_keys = list(elements.keys())
    element_cell_names = CELL_NAMES["elements"]

    col_names = ["Element", "Resistance"]
    element_table = initialize_table("Elemental Resistances", 4, column_names=col_names)

    for i in range(0, len(elements), 2):
        left_element = element_cell_names[i]
        right_element = element_cell_names[i+1]
        left_resist = get_table_data(element_keys[i], monster)
        right_resist = get_table_data(element_keys[i+1], monster)

        element_table.add_row(left_element, left_resist, right_element, right_resist)

    return element_table
     


def get_status_resist_table(monster):
    statusses = monster["stat_resists"]
    status_keys = list(statusses.keys())
    status_cell_names = CELL_NAMES["statusses"]

    col_names = ["Status", "Resistance"]
    status_table = initialize_table("Status Resistances", 4, column_names=col_names)

    for i in range(0, len(statusses), 2):
        left_status = status_cell_names[i]
        right_status = status_cell_names[i+1]
        left_resist = get_table_data(status_keys[i], monster)
        right_resist = get_table_data(status_keys[i+1], monster)
        
        status_table.add_row(left_status, left_resist, right_status, right_resist)

    return status_table



def get_item_table(monster):
    items = monster["items"]
    item_keys = list(items.keys())
    item_cell_names = CELL_NAMES["items"]

    item_table = initialize_table("Items and Loot", 2, tab_header=False)

    ap = get_table_data("ap", monster)
    gil = get_table_data("gil", monster)
    rage = get_table_data("ronso_rage", monster)

    item_table.add_row("AP (Overkill)", ap)
    item_table.add_row("Gil", gil)
    item_table.add_row("Ronso Rage", rage)

    for i in range(len(items)):
        action = item_cell_names[i]
        item = get_table_data(item_keys[i], monster)
        
        item_table.add_row(action, item)

    

    return item_table



def get_bribe_table(monster):
    hp = monster["stats"]["hp"][0]
    hp_factor = 10
    probability = 25

    col_names = ["Amount in Gil", "Success Rate"]
    bribe_table = initialize_table("Bribe Success Rate", 2, column_names=col_names)

    while probability <= 100:
        bribe_table.add_row(f"{hp * hp_factor}", f"{probability}%")
        hp_factor += 5
        probability += 25

    return bribe_table



def get_equipment_table(monster):
    if monster["equipment"]["drop_rate"] == 0:
        return
    
    equipment = monster["equipment"]
    equipment_keys = list(equipment.keys())
    equipment_cell_names = CELL_NAMES["equipment"]

    equipment_table = initialize_table("Equipment", 2, tab_header=False)

    for i in range(len(equipment)):
        name = equipment_cell_names[i]
        data = get_table_data(equipment_keys[i], monster)
        equipment_table.add_row(name, data)

    return equipment_table