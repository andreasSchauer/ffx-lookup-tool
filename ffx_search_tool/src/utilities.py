from rich.console import Console
from rich.table import Table
from rich import box
from ffx_search_tool.src.constants import TABLE_WIDTH
from ffx_search_tool.src.data import monster_data, monster_arena_data, remiem_temple_data


console = Console()


def initialize_table(tab_title, num_columns, tab_header=True, column_names=[]):
    table = Table(title=tab_title, show_lines=True, expand=True, box=box.SQUARE, title_style="bold", show_header=tab_header)
    col_width = int(TABLE_WIDTH / num_columns)

    if len(column_names) == 0:
        for i in range(num_columns):
            table.add_column("", width=col_width)
    else:
        for i in range(int(num_columns / len(column_names))):
            for name in column_names:
                table.add_column(name, width=col_width)

    return table



def get_table_data(key, monster_name):
    monster = monster_data[monster_name]

    if key in monster["stats"]:
        return get_stat_table_data(key, monster_name)
    
    if key in monster["elem_resists"]:
        return get_element_table_data(key, monster_name)
    
    if key in monster["stat_resists"]:
        return get_status_resist_table_data(key, monster_name)
    
    if key in monster["items"]:
        return get_item_table_data(key, monster_name)
    
    if key in monster["equipment"]:
        return get_equipment_table_data(key, monster_name)
    
    if key == "ap":
        return get_ap_data(monster_name)
    
    if key == "ronso_rage":
        return get_rage_data(monster_name)
    
    if key == "steals":
        return get_steals_data(monster_name)
    
    if key == "drops":
        return get_drops_data(monster_name)
    
    if key == "bribe_max":
        return get_bribe_max_data(monster_name)
    
    if key == "location":
        return get_location_data(monster_name)
    
    if monster_name in monster_arena_data and key in monster_arena_data[monster_name]:
        return get_arena_data(key, monster_name)
    
    if monster_name in remiem_temple_data and key in remiem_temple_data[monster_name]:
        return get_remiem_data(key, monster_name)
    
    return str(monster[key])




def get_stat_table_data(key, monster_name):
    stats = monster_data[monster_name]["stats"]
    if key == "hp":
        return f"{stats[key][0]} ({stats[key][1]})"
    
    return str(stats[key])





def get_element_table_data(key, monster_name):
    elem_resists = monster_data[monster_name]["elem_resists"]
    return get_elem_resist(elem_resists[key])


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
        case "varies":
            return "Varies"




def get_status_resist_table_data(key, monster_name):
    monster = monster_data[monster_name]
    statusses = monster["stat_resists"]

    if key == "doom":
        doom_res = get_stat_resist(statusses["doom"][0])
        doom_countdown = statusses["doom"][1]

        if doom_res == "Immune":
            return doom_res
        else:
            return f"{doom_res} ({doom_countdown})"
        
    if key == "poison":
        poison_res = get_stat_resist(statusses["poison"][0])
        poison_factor = statusses["poison"][1]

        if poison_res == "Immune":
            return poison_res

        monster_hp = monster["stats"]["hp"][0]
        poison_hp = round(monster_hp * poison_factor) 

        return f"{poison_res} ({poison_hp})"
        
    if key == "zombie" and isinstance(statusses["zombie"], list):
        zombie_res = get_stat_resist(statusses["zombie"][0])
        life_res = get_stat_resist(statusses["zombie"][1])
        return f"{zombie_res} ({life_res})"
        
    return get_stat_resist(statusses[key])


def get_stat_resist(resistance):
    match (resistance):
        case [100]:
            return str(resistance[0])
        case 100:
            return "Immune"
        case 0:
            return "-"
        case "auto":
            return "Auto"
        case _:
            return str(resistance)




def get_item_table_data(key, monster_name):
    items = monster_data[monster_name]["items"]
    if items[key] is None:
        return "-"
    
    if isinstance(items[key][0], list):
        data = ""

        for item in items[key]:
            data += f"{item[0].title()} x{item[1]}, "

        return data[:-2]
    
    return f"{items[key][0].title()} x{items[key][1]}"




def get_equipment_table_data(key, monster_name):
    equipment = monster_data[monster_name]["equipment"]
    match (key):
        case "drop_rate":
            return f"{round(equipment["drop_rate"] * 100)}%"
        
        case "slots_amount" | "attached_abilities":
            return equipment[key]
        
        case "wpn_abilities" | "armour_abilities":
            return get_ability_list(key, equipment)


def get_ability_list(key, equipment):
    abilities = equipment[key]
    ability_list = []

    for ability in abilities:
        to_add = ability["ability"].title()

        if "characters" in ability:
            to_add += f" ({ability["characters"]})"

        ability_list.append(to_add)

    return ", ".join(ability_list)



   
def get_ap_data(monster_name):
    ap = monster_data[monster_name]["ap"][0]
    ap_overkill = monster_data[monster_name]["ap"][1]

    return f"{ap} ({ap_overkill})"



def get_rage_data(monster_name):
    rage = monster_data[monster_name]["ronso_rage"]

    if rage is None:
        return "-"
    
    if isinstance(rage, list):
        rage = ", ".join(rage)

    return rage.title()


def get_steals_data(monster_name):
    steal_normal = get_table_data("steal_normal", monster_name)
    steal_rare = get_table_data("steal_rare", monster_name)
    steal = f"{steal_normal} ({steal_rare})"

    if steal == "- (-)":
        return "-"

    return steal



def get_drops_data(monster_name):
    drop_normal = get_table_data("drop_normal", monster_name)
    drop_rare = get_table_data("drop_rare", monster_name)

    monster = monster_data[monster_name]

    if monster["items"]["drop_normal"] is not None and isinstance(monster["items"]["drop_normal"][0], list):
        drop = f"{drop_normal}\n({drop_rare})"
    else:
        drop = f"{drop_normal} ({drop_rare})"

    if drop == "- (-)":
        return "-"

    return drop



def get_bribe_max_data(monster_name):
    item = get_table_data("bribe", monster_name)
    monster = monster_data[monster_name]

    if item == "-":
        return "-"
    
    gil_amount = f"{monster["stats"]["hp"][0] * 25} Gil"

    return f"{item} ({gil_amount})"


def get_location_data(monster_name):
    locations = monster_data[monster_name]["location"]
    return ", ".join(locations).title()


def get_arena_data(key, monster_name):
    monster = monster_arena_data[monster_name]
    match (key):
        case "condition":
            return monster["condition"]
        case "reward":
            item = monster["reward"][0].title()
            amount = monster["reward"][1]
            return f"{item} x{amount}"
        case "monsters":
            return ", ".join(monster["monsters"]).title()
    

def get_remiem_data(key, monster_name):
    monster = remiem_temple_data[monster_name]
    item = monster[key][0].title()
    amount = monster[key][1]
    return f"{item} x{amount}"
    

