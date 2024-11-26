from ffx_search_tool.src.search.ability_search import aeon_ability_search, auto_ability_search
from ffx_search_tool.src.search.monster_search import monster_search
from ffx_search_tool.src.search.location_search import location_search
from ffx_search_tool.src.search.item_search import item_search
from ffx_search_tool.src.search.other_searches import get_primer_table, get_celestial_table, ronso_rage_search, arena_creation_search, get_reward_table, get_items_table
from ffx_search_tool.src.data import monsters
from ffx_search_tool.src.utilities.misc import console


#monster_search("seymour", include_allies=False) # monster
#location_search("remiem templek") # location
#item_search("luknar curtain") # item
auto_ability_search("f") # customize
#aeon_ability_search("jfo") # learn
#ronso_rage_search("g") # rage
#get_monster_arena_table("jio") # capture

# list:
#get_primer_table() # list primers
#get_celestial_table() # list celestials
#get_reward_table(monster_arena=False, remiem_temple=False, chocobo_races=False, chocobo_training=False, lightning_dodging=False, cactuar_valley=False, butterfly_hjunt=False, other=False) # list rewards
#get_items_table(healing=False, support=False, attacking=False, spheres=False, okther=False) # list items