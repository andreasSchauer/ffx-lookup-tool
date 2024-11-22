from rich.table import Table
from rich import box
from functools import cmp_to_key
from ffx_search_tool.src.data import rewards, buyable_items, items, armour_abilities, weapon_abilities, aeon_abilities
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH
from ffx_search_tool.src.utilities.format_item_data import format_item_data, format_ability_data
from ffx_search_tool.src.utilities.key_search_table import get_key_search_table
from ffx_search_tool.src.utilities.misc import initialize_table, console, make_selection, format_num


def item_search(item_name):
    if item_name not in items:
        options = list(items.keys())
        item_name = make_selection(options, "Item not found.")
    
    get_item_desc_table(item_name)
    get_item_table(item_name)


#
def get_item_desc_table(item_name):
    item_desc_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    item_desc_table.add_column(item_name.title())
    tables = [items[item_name], get_ability_table(item_name)]
    
    for table in tables:
        if table is not None:
            item_desc_table.add_row(table)

    console.print(item_desc_table)



def get_ability_table(item_name):
    ability_lists = get_ability_lists(item_name)
    ability_table = abilities_to_table(ability_lists)
    
    return ability_table


def get_ability_lists(item_name):
    wpn_ability_list = list(filter(filter_ability_list(item_name, "weapon", weapon_abilities), weapon_abilities))
    armr_ability_list = list(filter(filter_ability_list(item_name, "armour", armour_abilities), armour_abilities))
    aeon_ability_list = list(filter(filter_ability_list(item_name, "aeon", aeon_abilities), aeon_abilities))

    return [wpn_ability_list, armr_ability_list, aeon_ability_list]


def filter_ability_list(item_name, ability_type, ability_data):
    def inner(abl):
        if ability_type == "weapon" or ability_type == "armour":
            item_data = ability_data[abl]["items"]
            return item_data is not None and item_name == item_data[0]
        
        if ability_type == "aeon":
            return item_name == ability_data[abl][0]
        
    return inner


def abilities_to_table(ability_lists):
    col_names = ["Weapon Abilities", "Armour Abilities", "Aeon Abilities"]
    table = initialize_table("Customizable / Learnable Abilities", 3, column_names=col_names)

    max_length = max(map(len, ability_lists))

    if max_length == 0:
        return

    for i in range(max_length):
        row_data = juxtapose_ability_lists(ability_lists, i)
        table.add_row(*row_data)
    
    return table


def juxtapose_ability_lists(ability_lists, i):
    types = ["weapon", "armour", "aeon"]
    row_data = []
    j = 0

    for list in ability_lists:
        if i >= len(list):
            value = "-"
        else:
            value = format_ability_data(list[i], types[j], item_search=True)
        
        row_data.append(value)
        j += 1

    return row_data



def get_item_table(item_name):    
    title = f"Where to get {item_name.title()}"

    if item_name in buyable_items:
        title += f" (Buyable for {format_num(buyable_items[item_name])} Gil)"
    
    item_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    item_table.add_column(title)

    if item_name == "clear sphere":
        item_table.add_row(f"Clear Spheres are buyable in the Monster Arena item shop after unlocking Ultima Buster.")

    tables = [
        get_key_search_table(item_name, "steal", ["Reoccurring", "Not Reoccurring", "Bosses"]),
        get_key_search_table(item_name, "drop", ["Reoccurring", "Not Reoccurring", "Bosses"]),
        get_key_search_table(item_name, "bribe", ["Reoccurring", "Not Reoccurring"]),
        get_item_rewards_table(item_name)
        ]

    for table in tables:
        if table is not None:
            item_table.add_row(table)
    
    console.print(item_table)



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

    return sort_rewards(quest_list)



def sort_rewards(filtered_list):
    return sorted(filtered_list, key=cmp_to_key(lambda mon1, mon2: compare_rewards(mon1, mon2)), reverse=True)



def compare_rewards(x, y):
    x_amount = x["reward"][1]
    y_amount = y["reward"][1]

    if x_amount > y_amount:
        return 1
    elif x_amount == y_amount:
        return 0
    else:
        return -1