from ffx_lookup_tool.src.constants import COMMON_SPHERES, CHARACTER_SPECIFIC_ABILITIES
from ffx_lookup_tool.src.utilities.format_monster_data import format_drop_rate
from ffx_lookup_tool.src.utilities.misc import initialize_table, format_string
from ffx_lookup_tool.src.utilities.key_search_table.filter_monsters import filter_monsters
from ffx_lookup_tool.src.utilities.key_search_table.replace_list_items import replace_list_items
from ffx_lookup_tool.src.utilities.key_search_table.sort_monsters import sort_monsters
from ffx_lookup_tool.src.utilities.format_item_data import format_item_data



# possible keys: steal, drop, bribe, equipment

def get_key_search_table(search_term, key, col_names, title=None, characters=False):
    if key == "drop" and search_term in COMMON_SPHERES:
        return f"Most monsters drop {search_term.title()}s. If you run out while stat maxing, use a distiller on Kottos to get 20 or 40 (Overkill) per battle."

    monster_lists = key_search_mons(search_term, key, characters)

    if characters:
        monsters_amount = sum(len(list) for list in monster_lists)
        characters_str = CHARACTER_SPECIFIC_ABILITIES[search_term]

        if monsters_amount > 80:
            return f"Most monsters drop this ability for {characters_str}. Below are the monsters that drop the ability for everybody."

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
        row_data = monster_lists_into_rows(monster_lists, search_term, key, i)
        table.add_row(*row_data)

    return table



def monster_lists_into_rows(monster_lists, search_term, key, i):
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



def key_search_table_title(search_term, key, format_characters=False, include_names=False):
    if key == "steal":
        title = "Stealing"

    if key == "drop":
        title = "Drops (Overkill Doubles Amount)"

    if key == "bribe":
        title = "Bribing"

    if key == "equipment":
        if format_characters:
            names = get_character_names(search_term, include_names)
            title = f"Monsters that drop {format_string(search_term)} for {names} (Drop Rate)"
        else:
            title = f"Monsters that drop {format_string(search_term)} (Drop Rate)"

    return title


def get_character_names(search_term, include_names=False):
    if include_names:
        return CHARACTER_SPECIFIC_ABILITIES[search_term]
    else:
        return "everybody"