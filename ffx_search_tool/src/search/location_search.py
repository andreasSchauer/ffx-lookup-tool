from rich.table import Table
from rich import box
from ffx_search_tool.src.data import monster_data
from ffx_search_tool.src.constants import LOCATIONS, TABLE_WIDTH
from ffx_search_tool.src.utilities import get_table_data, initialize_table, console



def location_search(location_name):
    if location_name not in LOCATIONS:
        location_name = select_location()

    reoccuring_monsters, one_time_monsters, boss_monsters = get_local_monsters(location_name)

    if reoccuring_monsters:
        get_location_table(location_name, reoccuring_monsters, "Reoccuring")

    if one_time_monsters:
        get_location_table(location_name, one_time_monsters, "Not Reoccuring")

    if boss_monsters:
        get_location_table(location_name, boss_monsters, "Bosses")



def select_location():
    for i, location in enumerate(LOCATIONS):
        print(f"{i + 1}: {location.title()}")
        
    choice = int(input("Invalid location. Choose by number: ")) - 1
    return LOCATIONS[choice]



def get_local_monsters(location_name):
    local_monsters = list(filter(lambda mon: location_name in monster_data[mon]["location"], monster_data))
    reoccuring_monsters = get_reoccuring_monsters(local_monsters)
    one_time_monsters = get_one_time_monsters(local_monsters)
    boss_monsters = get_boss_monsters(local_monsters)

    return reoccuring_monsters, one_time_monsters, boss_monsters
    

def get_reoccuring_monsters(local_monsters):
    return list(filter(lambda mon: monster_data[mon]["is_reoccuring"], local_monsters))


def get_one_time_monsters(local_monsters):
    return list(filter(lambda mon: not monster_data[mon]["is_reoccuring"] and not monster_data[mon]["is_boss"], local_monsters))


def get_boss_monsters(local_monsters):
    boss_monsters = list(filter(lambda mon: monster_data[mon]["is_boss"], local_monsters))
    boss_monsters_sorted = []

    for boss in boss_monsters:
        if monster_data[boss]["has_allies"]:
            for ally in monster_data[boss]["allies"]:
                if ally not in boss_monsters_sorted and not isinstance(ally, list):
                    boss_monsters_sorted.append(ally)
        else:
            boss_monsters_sorted.append(boss)

    return boss_monsters_sorted



def get_location_table(location_name, monster_list, type):
    title = f"{location_name.title()} - {type}"
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    table.add_column(title)

    for monster_name in monster_list:
        monster = monster_data[monster_name]
        table.add_row(get_short_mon_table(monster, monster_name))

    console.print(table)



def get_short_mon_table(monster, monster_name): 
    is_not_catchable = (
        not monster["is_boss"]
        and "monster arena" not in monster["location"]
        and "remiem temple" not in monster["location"]
    )
    
    if monster["is_catchable"]:
        monster_name += " - Catchable"
    elif is_not_catchable:
        monster_name += " - Not Catchable"

    monster_table = initialize_table(monster_name.title(), 2, tab_header=False)
    
    # initialize this with an if else statement: monster arena, remiem, else = regular
    # if monster arena in monster["location"]: hp, ap, steals, drops, condition, reward
    # if remiem temple in monster["location"]: hp, first reward, recurring reward
    # else:
    table_keys = [("HP (Overkill)", "hp"), ("AP (Overkill)", "ap"), ("Gil", "gil"), ("Steal (Rare Steal)", "steals"), ("Drop (Rare Drop)", "drops"), ("Bribe (Max Amount)", "bribe_max"), ("Ronso Rage", "ronso_rage")]

    for key in table_keys:
        monster_table.add_row(key[0], get_table_data(key[1], monster))

    """
    monster_table.add_row("HP (Overkill)", get_table_data("hp", monster))
    monster_table.add_row("AP (Overkill)", get_table_data("ap", monster))
    monster_table.add_row("Gil", get_table_data("gil", monster))
    monster_table.add_row("Steal (Rare Steal)", get_table_data("steals", monster))
    monster_table.add_row("Drop (Rare Drop)", get_table_data("drops", monster))
    monster_table.add_row("Bribe (Max Amount)", get_table_data("bribe_max", monster))
    monster_table.add_row("Ronso Rage", get_table_data("ronso_rage", monster))
    """
    

    return monster_table