from rich.table import Table
from rich import box
from ffx_search_tool.src.data import rewards, buyable_items, items, armour_abilities, weapon_abilities, aeon_abilities
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH, COMMON_SPHERES, REPLACEMENTS
from ffx_search_tool.src.utilities.format_item_data import format_item_data, format_ability_data
from ffx_search_tool.src.utilities.misc import initialize_table, console, make_selection, format_num
from ffx_search_tool.src.utilities.filter_monsters import filter_monsters
from ffx_search_tool.src.utilities.sort_monsters import sort_monsters_and_rewards


def item_search(item_name):
    if item_name not in items:
        options = list(items.keys())
        item_name = make_selection(options, "Item not found.")
    
    get_item_desc_table(item_name)
    get_item_table(item_name)


def aeon_ability_search(ability_name):
    if ability_name not in aeon_abilities:
        options = list(aeon_abilities.keys())
        ability_name = make_selection(options, "Ability not found.")

    item_name = aeon_abilities[ability_name][0]

    get_aeon_ability_desc_table(ability_name)
    get_item_table(item_name)



def auto_ability_search(ability_name):
    if ability_name not in weapon_abilities and ability_name not in armour_abilities:
        options = list(weapon_abilities.keys()) + list(armour_abilities.keys())
        ability_name = make_selection(options, "Ability not found.")

        if ability_name in weapon_abilities:
            ability_data = weapon_abilities
            ability_type = "weapon"
        else:
            ability_data = armour_abilities
            ability_type = "armour"

    item_name = ability_data[ability_name]["items"][0]

    get_auto_ability_desc_table(ability_name, ability_type)
    get_item_table(item_name)



def get_item_desc_table(item_name):
    item_desc_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    item_desc_table.add_column(item_name.title())
    tables = [items[item_name], get_ability_table(item_name)]
    
    for table in tables:
        if table is not None:
            item_desc_table.add_row(table)

    console.print(item_desc_table)


def get_aeon_ability_desc_table(ability_name):
    ability_desc_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    ability_desc_table.add_column(ability_name.title())
    data = format_ability_data(ability_name, "aeon")
    ability_desc_table.add_row(f"Needed to learn: {data}")

    console.print(ability_desc_table)


def get_auto_ability_desc_table(ability_name, ability_type):
    ability_desc_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    ability_desc_table.add_column(ability_name.title())
    item_data = format_ability_data(ability_name, ability_type)
    ability_description = get_auto_ability_description(ability_name, ability_type)

    ability_desc_table.add_row(ability_description)
    ability_desc_table.add_row(f"Needed to customize: {item_data}")
    
    # I can't use this exact function. I need to track everything down step by step
    ability_desc_table.add_row(convert_mons_to_item_table(ability_name, "equipment", ["Reoccurring", "Not Reoccurring", "Bosses"]))

    console.print(ability_desc_table)


def get_auto_ability_description(ability_name, ability_type):
    if ability_type == "weapon":
        return weapon_abilities[ability_name]["description"]
    
    if ability_type == "armour":
        return armour_abilities[ability_name]["description"]
    

def get_ability_drop_table(ability_name, ability_type):
    pass
    
    


def get_ability_table(item_name):
    type = ["weapon", "armour", "aeon"]
    col_names = ["Weapon Abilities", "Armour Abilities", "Aeon Abilities"]
    ability_lists = get_ability_lists(item_name)
    ability_table = initialize_table("Customizable / Learnable Abilities", 3, column_names=col_names)

    max_length = max(len(ability_lists[0]), len(ability_lists[1]), len(ability_lists[2]))

    if max_length == 0:
        return

    for i in range(max_length):
        columns = []
        j = 0
        for list in ability_lists:
            if i >= len(list):
                value = "-"
            else:
                value = format_ability_data(list[i], type[j], item_search=True)
            
            columns.append(value)
            j += 1
        
        ability_table.add_row(*columns)
    
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
    title = get_item_table_title(item_name, key)
    table = initialize_table(title, len(col_names), column_names=col_names)
    monster_lists = filter_and_sort_mons(item_name, key)

    max_length = max(len(monster_lists[0]), len(monster_lists[1]), len(monster_lists[2]))

    if max_length == 0:
        return

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


def get_item_table_title(item_name, key):
    if key == "drop" and item_name in COMMON_SPHERES:
        return f"Most monsters drop {item_name.title()}s. If you run out while stat maxing, use a distiller on Kottos to get 20 or 40 (Overkill) per battle."
    
    if key == "steal":
        title = "Stealing"
    
    if key == "drop":
        title = "Drops (Overkill Doubles Amount)"

    if key == "bribe":
        title = "Bribing"

    # need own function
    if key == "equipment":
        title = f"Monsters that drop {item_name.title()}"

    return title



def filter_and_sort_mons(item_name, key):
    monster_lists = filter_monsters(item_name, key)
    monster_lists_sorted = []

    for list in monster_lists:
        new_list = replace_list_items(list, item_name, key)
        sorted_list = sort_monsters_and_rewards(new_list, item_name, key)
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