from ffx_search_tool.src.search.monster_search import monster_search
from ffx_search_tool.src.search.location_search import location_search
from ffx_search_tool.src.search.item_search import item_search, get_steal_table
from ffx_search_tool.src.search.other_searches import get_primer_table, get_celestial_table, ronso_rage_search, get_monster_arena_table, get_reward_table


#monster_search("mimifc", single=True)
#location_search("remiem templek")
#get_reward_table(monster_arena=False, remiem_temple=True, chocobo_races=False, chocobo_training=False, lightning_dodging=False, cactuar_valley=False, butterfly_hunt=False, other=False)

get_steal_table("water gem")

