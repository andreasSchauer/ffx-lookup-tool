from ffx_search_tool.src.utilities.constants import COMMON_SPHERES, REPLACEMENTS
from ffx_search_tool.src.utilities.format_monster_data import format_drop_rate
from ffx_search_tool.src.utilities.misc import initialize_table
from ffx_search_tool.src.utilities.filter_monsters import filter_monsters
from ffx_search_tool.src.utilities.sort_monsters import sort_monsters
from ffx_search_tool.src.utilities.format_item_data import format_item_data



# possible keys: steal, drop, bribe, equipment

def get_key_search_table(search_term, key, col_names, title=None, characters=False):
    if key == "drop" and search_term in COMMON_SPHERES:
        return f"Most monsters drop {search_term.title()}s. If you run out while stat maxing, use a distiller on Kottos to get 20 or 40 (Overkill) per battle."

    monster_lists = key_search_mons(search_term, key, characters)
    monsters_amount = sum(len(list) for list in monster_lists)

    if characters:
        pass
        # determine title based of monsters amount and ability
        # and determine if to print the character specific table at all or whether to return text based of monsters amount

    table = monsters_to_table(monster_lists, search_term, key, col_names, title)

    return table


def key_search_mons(item_name, key, characters=False):
    monster_lists = filter_monsters(item_name, key, characters)
    monster_lists_sorted = []

    for list in monster_lists:
        new_list = replace_list_items(list, item_name, key)
        sorted_list = sort_monsters(new_list, item_name, key)
        monster_lists_sorted.append(sorted_list)

    return monster_lists_sorted



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



def monsters_to_table(monster_lists, search_term, key, col_names, title=None):
    if title is None:
        title = key_search_table_title(search_term, key)

    table = initialize_table(title, len(col_names), column_names=col_names)

    max_length = max(map(len, monster_lists))

    if max_length == 0:
        return

    if key == "bribe":
        monster_lists.pop()

    for i in range(max_length):
        row_data = juxtapose_monster_lists(monster_lists, search_term, key, i)
        table.add_row(*row_data)

    return table



def key_search_table_title(item_name, key):
    if key == "steal":
        title = "Stealing"

    if key == "drop":
        title = "Drops (Overkill Doubles Amount)"

    if key == "bribe":
        title = "Bribing"

    if key == "equipment":
        title = f"Monsters that drop {item_name.title()} (Drop Rate)"

    return title



def juxtapose_monster_lists(monster_lists, search_term, key, i):
    row_data = []

    for list in monster_lists:
        if i >= len(list):
            value = "-"
        elif key != "equipment":
            value = format_item_data(search_term, list[i], key)
        else:
            value = format_drop_rate(list[i])

        row_data.append(value)

    return row_data



