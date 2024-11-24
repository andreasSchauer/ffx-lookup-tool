from ffx_search_tool.src.data import monsters, monster_arena, remiem_temple
from ffx_search_tool.src.utilities.constants import REPLACEMENTS
from ffx_search_tool.src.utilities.misc import format_num, format_item, format_string


def format_monster_data(key, monster_name):
    monster = monsters[monster_name]

    if key in monster["stats"]:
        return format_stats(key, monster_name)
    
    if key in monster["elem_resists"]:
        return format_elem_resists(key, monster_name)
    
    if key in monster["stat_resists"]:
        return format_status_resists(key, monster_name)
    
    if key in monster["items"]:
        return format_item_list(key, monster_name)
    
    if key in monster["equipment"]:
        return format_equipment_list(key, monster_name)
    
    if key == "ap":
        return format_ap(monster_name)
    
    if key == "gil":
        return format_num(monster["gil"])
    
    if key == "ronso_rage":
        return format_rage(monster_name)
    
    if key == "steals":
        return format_steals(monster_name)
    
    if key == "drops":
        return format_drops(monster_name)
    
    if key == "bribe_max":
        return format_bribe_max(monster_name)
    
    if key == "location":
        return format_location(monster_name)
    
    if monster_name in monster_arena and key in monster_arena[monster_name]:
        return format_arena_data(key, monster_name)
    
    if monster_name in remiem_temple and key in remiem_temple[monster_name]:
        return format_remiem_items(key, monster_name)
    
    return format_string(str(monster[key]))




def format_stats(key, monster_name):
    stats = monsters[monster_name]["stats"]
    if key == "hp":
        hp = format_num(stats["hp"][0])
        hp_overkill = format_num(stats["hp"][1])
        return f"{hp} ({hp_overkill})"
    
    if key == "mp":
        return format_num(stats["mp"])
    
    return str(stats[key])





def format_elem_resists(key, monster_name):
    elem_resists = monsters[monster_name]["elem_resists"]
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




def format_status_resists(key, monster_name):
    monster = monsters[monster_name]
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
        poison_hp = format_num(round(monster_hp * poison_factor))

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




def format_item_list(key, monster_name):
    items = monsters[monster_name]["items"]
    if items[key] is None:
        return "-"
    
    if isinstance(items[key][0], list):
        data = ""

        for item in items[key]:
            data += f"{format_item(item)}, "

        return data[:-2]
    
    return format_item(items[key])




def format_equipment_list(key, monster_name):
    equipment = monsters[monster_name]["equipment"]
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
        to_add = ability["ability"]

        if "characters" in ability:
            to_add += f" ({ability["characters"]})"

        ability_list.append(to_add)

    return format_string(", ".join(ability_list))



   
def format_ap(monster_name):
    ap = format_num(monsters[monster_name]["ap"][0])
    ap_overkill = format_num(monsters[monster_name]["ap"][1])

    return f"{ap} ({ap_overkill})"



def format_rage(monster_name):
    rage = monsters[monster_name]["ronso_rage"]

    if rage is None:
        return "-"
    
    if isinstance(rage, list):
        rage = ", ".join(rage)

    return format_string(rage)


def format_steals(monster_name):
    steal_common = format_monster_data("steal_common", monster_name)
    steal_rare = format_monster_data("steal_rare", monster_name)
    steal = f"{steal_common} ({steal_rare})"

    if steal == "- (-)":
        return "-"

    return steal



def format_drops(monster_name):
    drop_common = format_monster_data("drop_common", monster_name)
    drop_rare = format_monster_data("drop_rare", monster_name)

    monster = monsters[monster_name]

    if monster["items"]["drop_common"] is not None and isinstance(monster["items"]["drop_common"][0], list):
        drop = f"{drop_common}\n({drop_rare})"
    else:
        drop = f"{drop_common} ({drop_rare})"

    if drop == "- (-)":
        return "-"

    return drop



def format_bribe_max(monster_name):
    item = format_monster_data("bribe", monster_name)
    monster = monsters[monster_name]

    if item == "-":
        return "-"
    
    gil_amount = f"{format_num(monster["stats"]["hp"][0] * 25)} Gil"

    return format_string(f"{item} ({gil_amount})")


def format_location(monster_name):
    locations = monsters[monster_name]["location"]
    return format_string(", ".join(locations))


def format_arena_data(key, monster_name):
    monster = monster_arena[monster_name]
    match (key):
        case "condition":
            return monster["condition"]
        case "reward":
            return format_item(monster["reward"])
        case "monsters":
            return format_string(", ".join(monster["monsters"]))
    

def format_remiem_items(key, monster_name):
    monster = remiem_temple[monster_name]
    return format_item(monster[key])



def format_drop_rate(monster_name):
    if monster_name in REPLACEMENTS:
        drop_rate = REPLACEMENTS[monster_name]["equipment"]["drop_rate"]
    else:
        drop_rate = monsters[monster_name]["equipment"]["drop_rate"]

    drop_percentage = int(drop_rate * 100)
    return format_string(f"{monster_name} ({drop_percentage}%)")