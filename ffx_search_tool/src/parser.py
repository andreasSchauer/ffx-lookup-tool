import json
import importlib.resources
from rich.console import Console
from rich.table import Table
from rich import box
from ffx_search_tool.src.table_data import get_table_data

with importlib.resources.open_text("ffx_search_tool.data", "monsters.json") as file:
    monster_data = json.load(file)


console = Console()
table_width = 96

stat_names = ["HP (Overkill)", "MP", "Strength", "Defence", "Magic", "Magic Defence", "Agility", "Luck", "Evasion", "Accuracy"]
action_names = ["Steal (Normal)", "Steal (Rare)", "Drop (Normal)", "Drop (Rare)", "Bribe"]
status_names = ["Silence", "Sleep", "Dark", "Poison (HP Loss)", "Petrify", "Slow", "Zombie", "Power Break", "Magic Break", "Armour Break", "Mental Break", "Threaten", "Death", "Provoke", "Doom (Countdown)", "Delay", "Eject", "Zanmato"]
equipment_names = ["Drop Rate", "Slots Amount", "Number of Abilities", "Weapon Abilities", "Armour Abilities"]



def monster_search(monster_name):
    monster = monster_data[monster_name]
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=table_width, padding=1)
    
    table.add_column(monster_name.title())
    table.add_row(get_stat_table(monster))
    table.add_row(get_element_table(monster))
    table.add_row(get_status_resist_table(monster))
    table.add_row(get_loot_table(monster))
    table.add_row(get_item_table(monster))
    table.add_row(get_bribe_table(monster))
    table.add_row(get_equipment_table(monster))

    console.print(table)



def initialize_table(tab_title, num_columns, tab_header=True, column_names=[]):
    table = Table(title=tab_title, show_lines=True, expand=True, box=box.SQUARE, title_style="bold", show_header=tab_header)
    col_width = int(table_width / num_columns)

    if len(column_names) == 0:
        for i in range(num_columns):
            table.add_column("", width=col_width)
    else:
        for i in range(int(num_columns / len(column_names))):
            for name in column_names:
                table.add_column(name, width=col_width)

    return table



def get_stat_table(monster):
    stats = monster["stats"]
    stat_keys = list(stats.keys())
    
    stat_table = initialize_table("Stats", 4, tab_header=False)

    for i in range(0, len(stats), 2):
        left_stat = stat_names[i]
        right_stat = stat_names[i+1]
        left_val = get_table_data(stat_keys[i], monster)
        right_val = get_table_data(stat_keys[i+1], monster)
        
        stat_table.add_row(left_stat, left_val, right_stat, right_val)

    return stat_table



def get_element_table(monster):
    elements = monster["elem_resists"]
    element_keys = list(elements.keys())

    col_names = ["Element", "Resistance"]
    element_table = initialize_table("Elemental Resistances", 4, column_names=col_names)

    for i in range(0, len(elements), 2):
        left_element = element_keys[i].title()
        right_element = element_keys[i+1].title()
        left_resist = get_table_data(element_keys[i], monster)
        right_resist = get_table_data(element_keys[i+1], monster)

        element_table.add_row(left_element, left_resist, right_element, right_resist)

    return element_table
     


def get_status_resist_table(monster):
    statusses = monster["stat_resists"]
    status_keys = list(statusses.keys())

    col_names = ["Status", "Resistance"]
    status_table = initialize_table("Status Resistances", 4, column_names=col_names)

    for i in range(0, len(statusses), 2):
        left_status = status_names[i]
        right_status = status_names[i+1]
        left_resist = get_table_data(status_keys[i], monster)
        right_resist = get_table_data(status_keys[i+1], monster)
        
        status_table.add_row(left_status, left_resist, right_status, right_resist)

    return status_table



def get_loot_table(monster):
    ap = monster["ap"][0]
    ap_overkill = monster["ap"][1]
    gil = str(monster["gil"])

    loot_table = initialize_table("Loot", 2, tab_header=False)

    loot_table.add_row("AP (Overkill)", f"{ap} ({ap_overkill})")
    loot_table.add_row("Gil", gil)

    return loot_table



def get_item_table(monster):
    items = monster["items"]
    item_keys = list(items.keys())

    item_table = initialize_table("Items", 2, tab_header=False)

    for i in range(len(items)):
        action = action_names[i]
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
    equipment = monster["equipment"]
    equipment_keys = list(equipment.keys())

    equipment_table = initialize_table("Equipment", 2, tab_header=False)

    for i in range(len(equipment)):
        name = equipment_names[i]
        data = get_table_data(equipment_keys[i], monster)
        equipment_table.add_row(name, data)

    return equipment_table



monster_search("dingo")