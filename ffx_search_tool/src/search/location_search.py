from rich.table import Table
from rich import box
from ffx_search_tool.src.data import monsters
from ffx_search_tool.src.utilities.constants import LOCATIONS, TABLE_WIDTH
from ffx_search_tool.src.utilities.tables import get_short_mon_table, console


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
    local_monsters = list(filter(lambda mon: location_name in monsters[mon]["location"], monsters))
    reoccuring_monsters = get_reoccurring_monsters(local_monsters)
    one_time_monsters = get_one_time_monsters(local_monsters)
    boss_monsters = get_boss_monsters(local_monsters)

    return reoccuring_monsters, one_time_monsters, boss_monsters
    

def get_reoccurring_monsters(local_monsters):
    return list(filter(lambda mon: monsters[mon]["is_reoccurring"], local_monsters))


def get_one_time_monsters(local_monsters):
    return list(filter(lambda mon: not monsters[mon]["is_reoccurring"] and not monsters[mon]["is_boss"], local_monsters))


def get_boss_monsters(local_monsters):
    boss_monsters = list(filter(lambda mon: monsters[mon]["is_boss"], local_monsters))
    boss_monsters_sorted = []

    for boss in boss_monsters:
        if monsters[boss]["has_allies"]:
            for ally in monsters[boss]["allies"]:
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
        if monster_name == "cindy" or monster_name == "sandy":
            continue
        
        table.add_row(get_short_mon_table(monster_name))

    console.print(table)