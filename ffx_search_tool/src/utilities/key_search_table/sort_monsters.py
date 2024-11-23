from functools import cmp_to_key
from ffx_search_tool.src.data import monsters
from ffx_search_tool.src.utilities.constants import REPLACEMENTS


def sort_monsters(filtered_list, item_name, key):
    return sorted(filtered_list, key=cmp_to_key(lambda mon1, mon2: compare_monsters(mon1, mon2, item_name, key)), reverse=True)


def compare_monsters(x, y, item_name, key):
    if x in REPLACEMENTS:
        mon1 = REPLACEMENTS[x]
    else:
        mon1 = monsters[x]

    if y in REPLACEMENTS:
        mon2 = REPLACEMENTS[y]
    else:
        mon2 = monsters[y]
    
    match (key):
        case "steal":
            return compare_steal_drop(mon1, mon2, item_name, "steal_common", "steal_rare")
        case "drop":
            return compare_steal_drop(mon1, mon2, item_name, "drop_common", "drop_rare")
        case "bribe":
            return compare_bribe_items(mon1, mon2)
        case "equipment":
            return compare_equipment(mon1, mon2)



def compare_steal_drop(mon1, mon2, item_name, key_1, key_2):
    m1_common = mon1["items"][key_1]
    m1_rare = mon1["items"][key_2]
    m2_common = mon2["items"][key_1]
    m2_rare = mon2["items"][key_2]

    m1_item = determine_preferable_slot(m1_common, m1_rare, item_name)
    m2_item = determine_preferable_slot(m2_common, m2_rare, item_name)

    m1_item_is_common = m1_item == m1_common
    m2_item_is_common = m2_item == m2_common

    if m1_item[1] > m2_item[1]:
        return 1

    if m1_item_is_common == m2_item_is_common:
        if m1_item[1] == m2_item[1]:
            return 0
        else:
            return -1
        
    if m1_item_is_common and not m2_item_is_common:
        if m1_item[1] == m2_item[1]:
            return 1
    
    return -1



def determine_preferable_slot(common, rare, item_name):
    if isinstance(common[0], list):
        item_common = common[1][0]
        item_rare = rare[1][0]
        amount_common = common[1][1]
        amount_rare = rare[1][1]

    else:
        item_common = common[0]
        item_rare = rare[0]
        amount_common = common[1]
        amount_rare = rare[1]

    if item_common == item_rare and amount_common == amount_rare:
        return common
    
    if item_common == item_rare and amount_rare > amount_common:
        return rare
    
    if item_rare != item_name:
        return common

    if item_common != item_name:
        return rare



def compare_bribe_items(mon1, mon2):
    mon1_amount = mon1["items"]["bribe"][1]
    mon2_amount = mon2["items"]["bribe"][1]

    if mon1_amount > mon2_amount:
        return 1
    elif mon1_amount == mon2_amount:
        return 0
    else:
        return -1


def compare_equipment(mon1, mon2):
    mon1_rate = mon1["equipment"]["drop_rate"]
    mon2_rate = mon2["equipment"]["drop_rate"]

    if mon1_rate > mon2_rate:
        return 1
    elif mon1_rate == mon2_rate:
        return 0
    else:
        return -1