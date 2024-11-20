from rich.table import Table
from rich import box
from ffx_search_tool.src.data import monsters, rewards
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH
from ffx_search_tool.src.utilities.format_monster_data import format_monster_data, format_num
from ffx_search_tool.src.utilities.tables import initialize_table, console
from ffx_search_tool.src.utilities.filter_monsters import filter_monsters
from ffx_search_tool.src.utilities.sort_monsters import sort_monsters_and_rewards


def item_search(item_name):
    pass



def get_item_table(item_name):
    item_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    item_table.add_column(item_name.title())
    




def get_steal_table(item_name):
    steal_table = initialize_table("Stealing", 3, column_names=["Reoccurring", "Not Reoccurring", "Bosses"])
    farmable_mons, one_time_mons, boss_mons = filter_monsters(item_name, "steal")
    farmable_mons_sorted = sort_monsters_and_rewards(farmable_mons, item_name, "steal")
    one_time_mons_sorted = sort_monsters_and_rewards(one_time_mons, item_name, "steal")
    boss_mons_sorted = sort_monsters_and_rewards(boss_mons, item_name, "steal")

    for mon in boss_mons_sorted:
        print(format_item_data(item_name, mon, "steal"))



def format_item_data(item_name, monster_name, key):
    match (key):
        case "steal":
            return format_steal_drop_data(item_name, monster_name, "steal_common", "steal_rare")
        case "drop":
            return format_steal_drop_data(item_name, monster_name, "drop_common", "drop_rare")
        case "bribe":
            return format_bribe_data(monster_name)



def format_steal_drop_data(item_name, monster_name, common, rare):
    items = monsters[monster_name]["items"]
    item_is_common = items[common][0] == item_name
    item_is_rare = items[rare][0] == item_name
    common_amount = 0
    rare_amount = 0

    if item_is_common:
        common_amount = items[common][1]

    if item_is_rare:
        rare_amount = items[rare][1]

    if common_amount >= rare_amount:
        return f"{monster_name}: {common_amount}x"

    if not common_amount:
        return f"{monster_name}: {rare_amount}x (Rare)"
    
    return f"{monster_name}: {common_amount}x / {rare_amount}x (Rare)"



def format_bribe_data(monster_name):
    bribe_amount = monsters[monster_name]["items"]["bribe"][1]
    hp = monsters[monster_name]["stats"]["hp"][0]
    bribe_max = format_num(hp * 25)
    return f"{monster_name}: {bribe_amount}x ({bribe_max} Gil)"



def get_rewards(item_name):
    quest_list = []

    for quest in rewards.keys():
        for subquest in rewards[quest]["data"]:
            reward_item = subquest["reward"][0]

            if reward_item == item_name:
                quest_list.append(subquest)

    return sort_monsters_and_rewards(quest_list, item_name, "reward")