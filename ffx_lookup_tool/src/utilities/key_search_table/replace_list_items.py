from ffx_lookup_tool.src.constants import REPLACEMENTS



def replace_list_items(list, item_name, key):
    new_list = []

    for monster_name in list:
        alt_name = check_replacement(monster_name, item_name, key)

        if alt_name not in new_list:
            new_list.append(alt_name)

    return new_list



def check_replacement(monster_name, item_name, key):
    for repl_name in REPLACEMENTS.keys():
        mon_in_replacements = monster_name in REPLACEMENTS[repl_name]["mons"]
        if mon_in_replacements and should_be_replaced(repl_name, item_name, key):
            return repl_name

    return monster_name



def should_be_replaced(monster_name, search_term, key):
    if key == "steal" or key == "drop":
        return item_in_replacements(monster_name, search_term, key)

    if key == "equipment":
        return ability_in_replacements(monster_name, search_term)



def item_in_replacements(monster_name, item_name, key):
    if key == "steal":
        key_1 = "steal_common"
        key_2 = "steal_rare"
    if key == "drop":
        key_1 = "drop_common"
        key_2 = "drop_rare"

    items = REPLACEMENTS[monster_name]["items"]

    return item_name == items[key_1][0] or item_name == items[key_2][0]



def ability_in_replacements(monster_name, ability_name):
    equipment = REPLACEMENTS[monster_name]["equipment"]
    ability_lists = [equipment["wpn_abilities"], equipment["armour_abilities"]]

    for list in ability_lists:
        for item in list:
            if ability_name == item["ability"]:
                return True

    return False