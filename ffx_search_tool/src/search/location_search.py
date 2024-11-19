from rich.table import Table
from rich import box
from ffx_search_tool.src.data import monsters
from ffx_search_tool.src.utilities.constants import LOCATIONS, TABLE_WIDTH
from ffx_search_tool.src.utilities.tables import get_short_mon_table, console
from ffx_search_tool.src.utilities.filter_monsters import filter_monsters


def location_search(location_name):
    if location_name not in LOCATIONS:
        location_name = select_location("Invalid location. Choose by number: ")

    reoccurring_monsters, one_time_monsters, boss_monsters = filter_monsters(location_name, "location")

    if reoccurring_monsters:
        get_location_table(location_name, reoccurring_monsters, "Reoccurring")

    if one_time_monsters:
        get_location_table(location_name, one_time_monsters, "Not Reoccurring")

    if boss_monsters:
        get_location_table(location_name, boss_monsters, "Bosses")



def select_location(error_msg):
    for i, location in enumerate(LOCATIONS):
        print(f"{i + 1}: {location.title()}")
        
    choice = int(input(f"{error_msg}")) - 1
    return LOCATIONS[choice]



def get_location_table(location_name, monster_list, type):
    title = f"{location_name.title()} - {type}"
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    table.add_column(title)

    for monster_name in monster_list:
        if monster_name == "cindy" or monster_name == "sandy":
            continue
        
        table.add_row(get_short_mon_table(monster_name))

    console.print(table)