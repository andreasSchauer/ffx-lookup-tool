from rich.table import Table
from rich import box
from ffx_search_tool.src.utilities.constants import LOCATIONS, TABLE_WIDTH
from ffx_search_tool.src.utilities.misc import console, make_selection, format_string
from ffx_search_tool.src.utilities.key_search_table.filter_monsters import filter_monsters
from ffx_search_tool.src.utilities.short_mon_table import get_short_mon_table


def location_search(location_name):
    if location_name not in LOCATIONS:
        location_name = make_selection(LOCATIONS, "Invalid location")

    reoccurring_monsters, one_time_monsters, boss_monsters = filter_monsters(location_name, "location")

    if reoccurring_monsters:
        get_location_table(location_name, reoccurring_monsters, "Reoccurring")

    if one_time_monsters:
        get_location_table(location_name, one_time_monsters, "Not Reoccurring")

    if boss_monsters:
        get_location_table(location_name, boss_monsters, "Bosses")



def get_location_table(location_name, monster_list, type):
    title = format_string(f"{location_name} - {type}")
    table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    table.add_column(title)

    for monster_name in monster_list:
        if monster_name == "cindy" or monster_name == "sandy":
            continue
        
        table.add_row(get_short_mon_table(monster_name))

    console.print(table)