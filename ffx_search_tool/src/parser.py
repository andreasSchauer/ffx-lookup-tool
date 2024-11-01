import json
import importlib.resources
from rich.console import Console
from rich.table import Table
from rich import box
from rich.align import Align

with importlib.resources.open_text("ffx_search_tool.data", "monsters.json") as file:
    monster_data = json.load(file)


console = Console()

stat_names = ["HP (Overkill)", "MP", "Strength", "Defence", "Magic", "Magic Defence", "Agility", "Luck", "Evasion", "Accuracy"]
item_names = ["Steal (Normal)", "Steal (Rare)", "Drop (Normal)", "Drop (Rare)", "Bribe"]


# stats, dropped weapons/armor and items for defeating, stealing and bribing
def monster_search(monster_name):
    monster = monster_data[monster_name]
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, min_width=75)
    
    table.add_column(monster_name.title())

    table.add_row(get_stat_table(monster))
    table.add_row(get_item_table(monster))
    table.add_row(get_bribe_table(monster))

    console.print(table)


def get_stat_table(monster):
    stats = monster["stats"]
    stat_keys = list(stats.keys())
    stat_table = Table(show_lines=True, expand=True, box=box.SQUARE)
    stat_table.add_column("Stats")

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

    return stat_table


def get_item_table(monster):
    items = monster["items"]
    item_keys = list(items.keys())
    item_table = Table(show_lines=True, expand=True, box=box.SQUARE)
    item_table.add_column("Items")

    for i in range(0, len(item_keys), 1):
        left_name = item_names[i]
        left_key = item_keys[i]
        left_item = items[left_key][0].title()
        left_amt = items[left_key][1]
        
        
        item_table.add_row(left_name, f"{left_item} x{left_amt}")

        


    return item_table



def get_bribe_table(monster):
    hp = monster["stats"]["hp"][0]
    hp_factors = [10, 15, 20, 25]
    probabilities = [25, 50, 75, 100]

    bribe_table = Table(show_lines=True, expand=True, box=box.SQUARE)
    bribe_table.add_column("Bribe Success Rate")
    bribe_table.add_row("Amount in Gil", "Success Rate")

    for i in range(len(hp_factors)):
        bribe_table.add_row(f"{hp * hp_factors[i]}", f"{probabilities[i]}%")

    return bribe_table


monster_search("water flan")


