from ffx_search_tool.src.utilities.select import select


def validate_input(search_term, category, options=False):
    if options:
        search_term = select(category)

    if search_term is None:
        search_term = select(category, "No input was given.")

    return format_input(search_term)


def format_input(search_term):
    return search_term.lower().replace("_", " ").replace("auto ", "auto-").strip(" ")


HELPTEXT = {
    "monster": {
        "description": "Search for a monster by name and get its stats, resistances, items (stealing, dropped, bribing) and equipment drops. Also includes AP and Gil rewards, abilities for Kimahri to learn and whether the monster can be captured.",
        "monster_name": "The name of the target monster.",
        "allies": "If the monster appears in a boss fight with multiple opponents, all of them will be displayed.",
        "options": "Manually select a monster from a list of options. Select the monster's location first to filter the list of options."
    },
    "location": {
        "description": "Search for a location and get an overview of every monster that appears in that location, including their HP, AP and Gil rewards, items, Ronso Rage and whether they can be captured. Monsters are sorted by availability (farmable, one-time, bosses).",
        "location_name": "The name of the target location.",
        "options": "Manually select a location from a list of options."
    },
    "item": {
        "description": "Search for an item and get information on its effect, what abilities you can craft/learn from it, and how to obtain it from monsters (stealing, drops, bribing) or via rewards.",
        "item_name": "The name of the target item.",
        "options": "Manually select an item from a list of options. Select the item's category first to filter the list of options."
    },
    "customize": {
        "description": "Search for an auto-ability and get information on its effect, monsters that can drop it, the item and amount you need to customize it, and how to obtain the required item from monsters (stealing, drops, bribing) or via rewards.",
        "ability_name": "The name of the target auto-ability.",
        "options": "Manually select an auto-ability from a list of options. Select the ability's category first to filter the list of options."
    },
    "learn": {
        "description": "Search for an ability an aeon can learn and get the item and amount you need to learn it, and how to obtain the required item from monsters (stealing, drops, bribing) or via rewards.",
        "ability_name": "The name of the target ability.",
        "options": "Manually select an ability from a list of options."
    },
    "rage": {
        "description": "Search for a Ronso Rage ability and get an overview of every monster Kimahri can learn this ability from, including their HP, AP and Gil rewards, items, and whether they can be captured.",
        "ronso_rage": "The name of the target Ronso rage.",
        "options": "Manually select a Ronso rage from a list of options."
    },
    "capture": {
        "description": "Search for a Monster Arena creation and get its unlock requirements and reward, and an overview of it and the monsters needed to create it (if applicable), including their HP, AP and Gil rewards, items, and Ronso Rage.",
        "creation_name": "The name of the target creation.",
        "options": "Manually select a creation from a list of options."
    },
    "list": {
        "description": "Displays lists about rewards and key items for quick reference.",
        "primers": "Displays the locations of all Al Bhed Primers.",
        "celestials": "Displays the locations of and conditions to obtain every celestial weapon and their related items (crests and sigils).",
        "rewards": {
            "description": "Displays lists of rewards for various minigames and sidequests. If no flag is used, all eight lists are printed in the order seen below.",
            "arena": "Monster Arena creations.",
            "remiem": "Fights against Belgemine at Remiem Temple.",
            "chocobo": "Chocobo races at Remiem Temple.",
            "training": "Chocobo Training in the Calm Lands.",
            "lightning": "Lightning Dodging in the Thunder Plains.",
            "cactuar": "'Valley of the Cactuars' sidequest in Bikanel.",
            "butterfly": "Butterfly hunts in the Macalania Woods.",
            "other": "Other rewards (basically only for collecting all primers for now)."
        },
        "items": {
            "description": "Displays lists of items of various categories. If no flag is used, all five lists are printed in the order seen below.",
            "healing": "Healing items.",
            "support": "Protective items.",
            "attacking": "Damage-dealing items.",
            "spheres": "Sphere Grid related items.",
            "other": "Other items that don't fit the other categories."
        }
    }
}