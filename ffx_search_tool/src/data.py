import json
import importlib.resources

with importlib.resources.open_text("ffx_search_tool.data", "monsters.json") as file:
    monster_data = json.load(file)

with importlib.resources.open_text("ffx_search_tool.data", "monster_arena.json") as file:
    monster_arena_data = json.load(file)

with importlib.resources.open_text("ffx_search_tool.data", "remiem_temple.json") as file:
    remiem_temple_data = json.load(file)