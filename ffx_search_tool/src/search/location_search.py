from ffx_search_tool.src.utilities.constants import LOCATIONS
from ffx_search_tool.src.utilities.misc import initialize_wrapper_table, console, format_string
from ffx_search_tool.src.utilities.key_search_table.filter_monsters import filter_monsters
from ffx_search_tool.src.utilities.select import select
from ffx_search_tool.src.utilities.short_mon_table import get_short_mon_table


def location_search(location_name):
    if location_name not in LOCATIONS:
        location_name = select("location", "Location not found.")

    reoccurring_monsters, one_time_monsters, boss_monsters = filter_monsters(location_name, "location")

    if reoccurring_monsters:
        get_location_table(location_name, reoccurring_monsters, "Reoccurring")

    if one_time_monsters:
        get_location_table(location_name, one_time_monsters, "Not Reoccurring")

    if boss_monsters:
        get_location_table(location_name, boss_monsters, "Bosses")



def get_location_table(location_name, monster_list, type):
    title = format_string(f"{location_name} - {type}")
    table = initialize_wrapper_table(title)

    for monster_name in monster_list:
        if monster_name == "cindy" or monster_name == "sandy":
            continue
        
        table.add_row(get_short_mon_table(monster_name))

    console.print(table)