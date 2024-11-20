from ffx_search_tool.src.data import monsters
from ffx_search_tool.src.utilities.format_monster_data import format_num



def format_item_data(item_name, mon_or_reward, key):
    match (key):
        case "steal":
            return format_steal_drop_data(item_name, mon_or_reward, "steal_common", "steal_rare")
        case "drop":
            return format_steal_drop_data(item_name, mon_or_reward, "drop_common", "drop_rare")
        case "bribe":
            return format_bribe_data(mon_or_reward)
        case "reward":
            return format_reward_data(mon_or_reward)



def format_steal_drop_data(item_name, monster_name, common, rare):
    items = monsters[monster_name]["items"]

    if isinstance(items[common][0], list):
        return format_drop_list(item_name, monster_name, common, rare)

    item_is_common = items[common][0] == item_name
    item_is_rare = items[rare][0] == item_name
    common_amount = 0
    rare_amount = 0

    if item_is_common:
        common_amount = items[common][1]

    if item_is_rare:
        rare_amount = items[rare][1]

    if common_amount >= rare_amount:
        return f"{monster_name.title()}: {common_amount}x"

    if not common_amount:
        return f"{monster_name.title()}: {rare_amount}x (Rare)"
    
    return f"{monster_name.title()}: {common_amount}x / {rare_amount}x (Rare)"



def format_drop_list(item_name, monster_name, common, rare):
    items = monsters[monster_name]["items"]
    item_is_common = items[common][1][0] == item_name
    item_is_rare = items[rare][1][0] == item_name
    common_amount = 0
    rare_amount = 0

    if item_is_common:
        common_amount = items[common][1][1]

    if item_is_rare:
        rare_amount = items[rare][1][1]

    if common_amount >= rare_amount:
        return f"{monster_name.title()}: {common_amount}x"

    if not common_amount:
        return f"{monster_name.title()}: {rare_amount}x (Rare)"
    
    return f"{monster_name.title()}: {common_amount}x / {rare_amount}x (Rare)"




def format_bribe_data(monster_name):
    bribe_amount = monsters[monster_name]["items"]["bribe"][1]
    hp = monsters[monster_name]["stats"]["hp"][0]
    bribe_max = format_num(hp * 25)
    return f"{monster_name.title()}: {bribe_amount}x ({bribe_max} Gil)"



def format_reward_data(reward_dict):
    return f"{reward_dict["reward"][1]}x"