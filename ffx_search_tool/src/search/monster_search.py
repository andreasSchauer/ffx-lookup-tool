from rich.table import Table
from rich import box
from ffx_search_tool.data.monster_data import monster_data
from ffx_search_tool.src.constants import DUPLICATES, CELL_NAMES, TABLE_WIDTH
from ffx_search_tool.src.utilities import get_table_data, initialize_table, console



def get_monster_table(monster_name):
    monster = monster_data[monster_name]
    title = monster_name.title()

    if monster["is_catchable"]:
        title += " - Catchable"

    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    
    table.add_column(title)
    table.add_row(get_stat_table(monster))
    table.add_row(get_element_table(monster))
    table.add_row(get_status_resist_table(monster))
    table.add_row(get_loot_table(monster))
    table.add_row(get_item_table(monster))

    if monster["items"]["bribe"] is not None:
        table.add_row(get_bribe_table(monster))

    table.add_row(get_equipment_table(monster))

    console.print(table)



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



def get_stat_table(monster):
    stats = monster["stats"]
    stat_keys = list(stats.keys())
    stat_cell_names = CELL_NAMES["stats"]

    stat_table = initialize_table("Stats", 4, tab_header=False)

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



def get_loot_table(monster):
    ap = get_table_data("ap", monster)
    gil = get_table_data("gil", monster)

    loot_table = initialize_table("Loot", 2, tab_header=False)

    loot_table.add_row("AP (Overkill)", ap)
    loot_table.add_row("Gil", gil)

    return loot_table



def get_item_table(monster):
    items = monster["items"]
    item_keys = list(items.keys())
    item_cell_names = CELL_NAMES["items"]

    item_table = initialize_table("Items", 2, tab_header=False)

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