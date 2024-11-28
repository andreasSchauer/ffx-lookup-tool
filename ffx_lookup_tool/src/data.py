import json
import importlib.resources

with importlib.resources.open_text("ffx_lookup_tool.data", "aeon_abilities.json") as file:
    aeon_abilities = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "armour_abilities.json") as file:
    armour_abilities = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "buyable_items.json") as file:
    buyable_items = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "celestials.json") as file:
    celestials = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "items.json") as file:
    items = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "monster_arena.json") as file:
    monster_arena = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "monsters.json") as file:
    monsters = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "primers.json") as file:
    primers = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "remiem_temple.json") as file:
    remiem_temple = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "rewards.json") as file:
    rewards = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.data", "weapon_abilities.json") as file:
    weapon_abilities = json.load(file)

with importlib.resources.open_text("ffx_lookup_tool.src", "helptext.json") as file:
    helptext = json.load(file)