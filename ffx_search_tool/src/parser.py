import json
import importlib.resources
from rich.console import Console
from rich.table import Table
from rich import box
from rich.align import Align

with importlib.resources.open_text("ffx_search_tool.data", "monsters.json") as file:
    monster_data = json.load(file)


console = Console()
table_width = 96

stat_names = ["HP (Overkill)", "MP", "Strength", "Defence", "Magic", "Magic Defence", "Agility", "Luck", "Evasion", "Accuracy"]
action_names = ["Steal (Normal)", "Steal (Rare)", "Drop (Normal)", "Drop (Rare)", "Bribe"]
status_names = ["Silence", "Sleep", "Dark", "Poison (HP Loss)", "Petrify", "Slow", "Zombie", "Power Break", "Magic Break", "Armour Break", "Mental Break", "Threaten", "Death", "Provoke", "Doom (Countdown)", "Delay", "Eject", "Zanmato"]


# stats, dropped weapons/armor and items for defeating, stealing and bribing
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



def get_stat_table(monster):
    stats = monster["stats"]
    stat_keys = list(stats.keys())
    col_width = int(table_width / 4)

    stat_table = Table(title="Stats",show_lines=True, expand=True, box=box.SQUARE, show_header=False, title_style="bold")

    stat_table.add_column(width=col_width)
    stat_table.add_column(width=col_width)
    stat_table.add_column(width=col_width)
    stat_table.add_column(width=col_width)


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



def get_element_table(monster):
    elements = monster["elem_resists"]
    element_keys = list(elements.keys())
    col_width = int(table_width / 2)

    element_table = Table(title="Elemental Resistances",show_lines=True, expand=True, box=box.SQUARE, title_style="bold")
    element_table.add_column("Element", width=col_width)
    element_table.add_column("Resistance", width=col_width)

    for i in range(len(element_keys)):
        element = element_keys[i]
        resist = get_elem_resist(elements[element])

        element_table.add_row(element.title(), resist)

    return element_table
                

def get_elem_resist(factor):
    match (factor):
        case 1.5:
            return "Weak"
        case 0.5:
            return "Halved"
        case 0:
            return "Immune"
        case -1:
            return "Absorbed"
        case 1:
            return "-"



def get_status_resist_table(monster):
    statusses = monster["stat_resists"]
    status_keys = list(statusses.keys())
    col_width = int(table_width / 4)

    status_table = Table(title="Status Resistances",show_lines=True, expand=True, box=box.SQUARE, title_style="bold")
    status_table.add_column("Status", width=col_width)
    status_table.add_column("Resistance", width=col_width)
    status_table.add_column("Status", width=col_width)
    status_table.add_column("Resistance", width=col_width)

    for i in range(0, len(status_keys), 2):
        left_key = status_keys[i]
        left_status = status_names[i]
        right_key = status_keys[i+1]
        right_status = status_names[i+1]

        if left_key == "doom":
            doom_countdown = statusses["doom"][1]
            doom_res = get_stat_resist(statusses["doom"][0])

            if doom_res == "Immune":
                left_val = doom_res
            else:
                left_val = f"{doom_res} ({doom_countdown})"
        else:
            left_val = get_stat_resist(statusses[left_key])

        if right_key == "poison":
            poison_factor = statusses["poison"][1]
            monster_hp = monster["stats"]["hp"][0]
            poison_hp = round(monster_hp * poison_factor)
            poison_res = get_stat_resist(statusses["poison"][0])

            if poison_res == "Immune":
                right_val = poison_res
            else:
                right_val = f"{poison_res} ({poison_hp})"
        else:
            right_val = get_stat_resist(statusses[right_key])

        status_table.add_row(left_status, left_val, right_status, right_val)

    return status_table


def get_stat_resist(resistance):
    if resistance == 100:
        return "Immune"
    else:
        return str(resistance)



def get_loot_table(monster):
    ap = monster["ap"][0]
    ap_overkill = monster["ap"][1]
    gil = str(monster["gil"])
    col_width = int(table_width / 2)

    loot_table = Table(title="Loot",show_lines=True, expand=True, box=box.SQUARE, show_header=False, title_style="bold")

    loot_table.add_column(width=col_width)
    loot_table.add_column(width=col_width)

    loot_table.add_row("AP (Overkill)", f"{ap} ({ap_overkill})")
    loot_table.add_row("Gil", gil)

    return loot_table



def get_item_table(monster):
    items = monster["items"]
    item_keys = list(items.keys())
    col_width = int(table_width / 2)

    item_table = Table(title="Items",show_lines=True, expand=True, box=box.SQUARE, show_header=False, title_style="bold")

    item_table.add_column(width=col_width)
    item_table.add_column(width=col_width)

    for i in range(len(item_keys)):
        action = action_names[i]
        item_key = item_keys[i]
        item = items[item_key][0].title()
        amount = items[item_key][1]
        
        item_table.add_row(action, f"{item} x{amount}")

    return item_table



def get_bribe_table(monster):
    hp = monster["stats"]["hp"][0]
    hp_factors = [10, 15, 20, 25]
    probabilities = [25, 50, 75, 100]
    col_width = int(table_width / 2)

    bribe_table = Table(title="Bribe Success Rate",show_lines=True, expand=True, box=box.SQUARE, title_style="bold")
    bribe_table.add_column("Amount in Gil", width=col_width)
    bribe_table.add_column("Success Rate", width=col_width)

    for i in range(len(hp_factors)):
        bribe_table.add_row(f"{hp * hp_factors[i]}", f"{probabilities[i]}%")

    return bribe_table



def get_equipment_table(monster):
    equipment = monster["equipment"]
    weapon_abilities = equipment["wpn_abilities"]
    armour_abilities = equipment["armour_abilities"]
    drop_rate = str(equipment["drop_rate"])
    slots_amount = equipment["slots_amount"]
    attached_abilities = equipment["attached_abilities"]
    weapon_vals = []
    armour_vals = []
    col_width = int(table_width / 2)

    equipment_table = Table(title="Equipment",show_lines=True, expand=True, box=box.SQUARE, title_style="bold", show_header=False)

    equipment_table.add_column(width=col_width)
    equipment_table.add_column(width=col_width)

    equipment_table.add_row("Drop Rate", drop_rate)
    equipment_table.add_row("Slots Amount", slots_amount)
    equipment_table.add_row("Number of Abilities", attached_abilities)

    for weapon_ability in weapon_abilities:
        to_add = weapon_ability["ability"].title()

        if "characters" in weapon_ability:
            to_add += f" ({weapon_ability["characters"]})"

        weapon_vals.append(to_add)

    for armour_ability in armour_abilities:
        to_add = armour_ability["ability"].title()

        if "characters" in armour_ability:
            to_add += f" ({armour_ability["characters"]})"

        if to_add.startswith("Sos "):
            to_add = to_add.replace("Sos", "SOS")

        armour_vals.append(to_add)

    equipment_table.add_row("Weapon Abilities", ", ".join(weapon_vals))
    equipment_table.add_row("Armour Abilities", ", ".join(armour_vals))

    return equipment_table


monster_search("varuna")

