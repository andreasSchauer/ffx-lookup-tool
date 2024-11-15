import json
import importlib.resources

with importlib.resources.open_text("ffx_search_tool.data", "monsters.json") as file:
    monster_data = json.load(file)