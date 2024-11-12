from ffx_search_tool.src.constants import DUPLICATES, LOCATIONS
from ffx_search_tool.data.monster_data import monster_data
from ffx_search_tool.src.search.monster_search import select_duplicate, get_monster_table
from ffx_search_tool.src.search.location_search import select_location, get_local_monsters, get_location_table


def monster_search(monster_name):
    if monster_name in DUPLICATES:
        monster_name = select_duplicate(monster_name)

    if monster_name not in monster_data:
        raise Exception("Monster not found.")
    
    monster = monster_data[monster_name]

    if monster["has_allies"]:
        for ally in monster["allies"]:
            get_monster_table(ally)
    else:
        get_monster_table(monster_name)



def location_search(location_name):
    if location_name not in LOCATIONS:
        location_name = select_location()

    reoccuring_monsters, one_time_monsters, boss_monsters = get_local_monsters(location_name)

    if reoccuring_monsters:
        get_location_table(location_name, reoccuring_monsters,"Reoccuring")

    if one_time_monsters:
        get_location_table(location_name, one_time_monsters, "Not Reoccuring")

    if boss_monsters:
        get_location_table(location_name, boss_monsters, "Bosses")




monster_search("bandersnatch")