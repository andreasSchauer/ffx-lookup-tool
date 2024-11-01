import json
import importlib.resources
from rich.console import Console
from rich.table import Table

with importlib.resources.open_text("ffx_search_tool.data", "monsters.json") as file:
    monster_data = json.load(file)


console = Console()

stat_names = ["HP (Overkill)", "MP", "Strength", "Defence", "Magic", "Magic Defence", "Agility", "Luck", "Evasion", "Accuracy"]
item_names = ["Steal (Normal)", "Steal (Rare)", "Drop (Normal)", "Drop (Rare)"]


# stats, dropped weapons/armor and items for defeating, stealing and bribing
def monster_search(monster_name):
    monster = monster_data[monster_name]
    stat_table = get_stat_table(monster)
    item_table = get_item_table(monster)

    console.print(item_table)


def get_stat_table(monster):
    stats = monster["stats"]
    stat_keys = list(stats.keys())
    stat_table = Table(title="Stats", show_header=False)

    for i in range(0, len(stat_keys), 2):
        left_key = stat_keys[i]
        left_stat = stat_names[i]
        right_key = stat_keys[i+1]
        right_stat = stat_names[i+1]

        if left_key == "hp":
            left_val = f"{stats[left_key][0]} ({stats[left_key][1]})"
            right_val = str(stats[right_key])
        else:
            left_val = str(stats[left_key])
            right_val = str(stats[right_key])
        
        stat_table.add_row(left_stat, left_val, right_stat, right_val)
        stat_table.add_section()

    return stat_table


def get_item_table(monster):
    items = monster["items"]
    item_keys = list(items.keys())
    item_table = Table(title="Items", show_header=False)

    for i in range(0, len(item_keys), 2):
        left_name = item_names[i]
        left_key = item_keys[i]
        left_item = items[left_key][0].title()
        left_amt = items[left_key][1]
        right_name = item_names[i+1]
        right_key = item_keys[i+1]
        right_item = items[right_key][0].title()
        right_amt = items[right_key][1]
        
        item_table.add_row(left_name, f"{left_item} x{left_amt}", right_name, f"{right_item} x{right_amt}")
        item_table.add_section()

    return item_table
    

monster_search("varuna")


"""
    stats_table.add_row("HP (Overkill)", f"{stats["hp"][0]} ({stats["hp"][1]})", "MP", str(stats["mp"]))
    stats_table.add_section()
    stats_table.add_row("Strength", str(stats["strength"]), "Defence", str(stats["defence"]))
    stats_table.add_section()
    stats_table.add_row("Magic", str(stats["magic"]), "Magic Defence", str(stats["mag_defence"]))
    stats_table.add_section()
    stats_table.add_row("Agility", str(stats["agility"]), "Luck", str(stats["luck"]))
    stats_table.add_section()
    stats_table.add_row("Evasion", str(stats["evasion"]), "Accuracy", str(stats["accuracy"]))
"""