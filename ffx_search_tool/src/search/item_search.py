from rich.table import Table
from rich import box
from ffx_search_tool.src.data import rewards, buyable_items, items, armour_abilities, weapon_abilities, aeon_abilities
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH, COMMON_SPHERES, REPLACEMENTS
from ffx_search_tool.src.utilities.format_monster_data import format_num
from ffx_search_tool.src.utilities.format_item_data import format_item_data
from ffx_search_tool.src.utilities.tables import initialize_table, console
from ffx_search_tool.src.utilities.filter_monsters import filter_monsters
from ffx_search_tool.src.utilities.sort_monsters import sort_monsters_and_rewards


def item_search(item_name):
    # item-description
    # craftable weapon_abilities
    # craftable armour_abilities
    # learnable aeon_abilities
    
    get_item_table(item_name)


def get_item_table(item_name):
    item_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    
    title = f"Where to get {item_name.title()}"

    if item_name in buyable_items:
        title += f" (Buyable for {format_num(buyable_items[item_name])} Gil)"
    
    item_table.add_column(title)

    if item_name == "clear sphere":
        item_table.add_row(f"Clear Spheres are buyable in the Monster Arena item shop after unlocking Ultima Buster.")

    tables = [
        convert_mons_to_item_table(item_name, "steal", ["Reoccurring", "Not Reoccurring", "Bosses"]),
        convert_mons_to_item_table(item_name, "drop", ["Reoccurring", "Not Reoccurring", "Bosses"]),
        convert_mons_to_item_table(item_name, "bribe", ["Reoccurring", "Not Reoccurring"]),
        get_item_rewards_table(item_name)
        ]

    for table in tables:
        if table is not None:
            item_table.add_row(table)
    
    console.print(item_table)



def convert_mons_to_item_table(item_name, key, col_names):
    if key == "drop" and item_name in COMMON_SPHERES:
        return f"Most monsters drop {item_name.title()}s. If you run out while stat maxing, use a distiller on Kottos to get 20 or 40 (Overkill) per battle."
    
    if key == "steal":
        title = "Stealing"
    
    if key == "drop":
        title = "Drops (Overkill Doubles Amount)"

    if key == "bribe":
        title = "Bribing"
    
    table = initialize_table(title, len(col_names), column_names=col_names)
    reoccurring, not_reoccurring, bosses = filter_and_sort_mons(item_name, key)

    max_length = max(len(reoccurring), len(not_reoccurring), len(bosses))

    if max_length == 0:
        return

    monster_lists = [reoccurring, not_reoccurring, bosses]

    if key == "bribe":
        monster_lists.pop()

    for i in range(max_length):
        columns = []

        for list in monster_lists:
            if i >= len(list):
                value = "-"
            else:
                value = format_item_data(item_name, list[i], key)
            
            columns.append(value)
        
        table.add_row(*columns)
    
    return table



def filter_and_sort_mons(item_name, key):
    monster_lists = filter_monsters(item_name, key)
    monster_lists_sorted = []

    for list in monster_lists:
        new_list = replace_list_items(list, item_name, key)
        sorted_list = sort_monsters_and_rewards(new_list, item_name, key)
        monster_lists_sorted.append(sorted_list)

    return monster_lists_sorted[0], monster_lists_sorted[1], monster_lists_sorted[2]


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
        if mon_in_replacements and item_in_replacements(repl_name, item_name, key):
            return repl_name
        
    return monster_name


def item_in_replacements(monster_name, item_name, key):
    if key == "steal":
        key_1 = "steal_common"
        key_2 = "steal_rare"
    if key == "drop":
        key_1 = "drop_common"
        key_2 = "drop_rare"

    items = REPLACEMENTS[monster_name]["items"]

    return item_name == items[key_1][0] or item_name == items[key_2][0]




def get_item_rewards_table(item_name):
    table = initialize_table("Rewards", 2, column_names=["Condition", "Amount"])
    rewards = get_rewards(item_name)

    if len(rewards) == 0:
        return

    for quest in rewards:
        table.add_row(quest["description"], format_item_data(item_name, quest, "reward"))
    
    return table



def get_rewards(item_name):
    quest_list = []

    for quest in rewards.keys():
        for subquest in rewards[quest]["data"]:
            reward_item = subquest["reward"][0]

            if reward_item == item_name:
                quest_list.append(subquest)

    return sort_monsters_and_rewards(quest_list, item_name, "reward")