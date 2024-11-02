def get_table_data(key, monster):
    if key in monster["stats"]:
        return get_stat_table_data(key, monster["stats"])
    
    if key in monster["elem_resists"]:
        return get_element_table_data(key, monster["elem_resists"])
    
    if key in monster["stat_resists"]:
        return get_status_resist_table_data(key, monster)
    
    if key in monster["items"]:
        return get_item_table_data(key, monster["items"])
    
    if key in monster["equipment"]:
        return get_equipment_table_data(key, monster["equipment"])



def get_stat_table_data(key, stats):
    if key == "hp":
        return f"{stats[key][0]} ({stats[key][1]})"
    
    return str(stats[key])



def get_element_table_data(key, elements):
    return get_elem_resist(elements[key])



def get_status_resist_table_data(key, monster):
    statusses = monster["stat_resists"]

    if key == "doom":
        doom_countdown = statusses["doom"][1]
        doom_res = get_stat_resist(statusses["doom"][0])

        if doom_res == "Immune":
            return doom_res
        else:
            return f"{doom_res} ({doom_countdown})"
        
    if key == "poison":
        poison_factor = statusses["poison"][1]
        monster_hp = monster["stats"]["hp"][0]
        poison_hp = round(monster_hp * poison_factor)
        poison_res = get_stat_resist(statusses["poison"][0])

        if poison_res == "Immune":
            return poison_res
        else:
            return f"{poison_res} ({poison_hp})"
        
    return get_stat_resist(statusses[key])



def get_item_table_data(key, items):
    return f"{items[key][0].title()} x{items[key][1]}"



def get_equipment_table_data(key, equipment):
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



def get_stat_resist(resistance):
    match (resistance):
        case 100:
            return "Immune"
        case 0:
            return "-"
        case _:
            return str(resistance)
    
   