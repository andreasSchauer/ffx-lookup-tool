from ffx_search_tool.src.utilities.select import select


def validate_input(search_term, category, options=False):
    if options:
        search_term = select(category)

    if search_term is None:
        search_term = select(category, "No input was given.")

    return format_input(search_term)


def format_input(search_term):
    return search_term.lower().replace("_", " ").replace("auto ", "auto-").strip(" ")


HELP = {
    "monster": {
        "help": "Search for a monster by name and get its stats, resistances, items and drops.",
        "verbose": "jiaodüaoidajsüoiajüoaijsüaoisjdaüoij",
        "monster_name": "The name of the target monster.",
        "allies": "Includes the allies of a boss monster, if it has any.",
        "options": "Manually select a monster from a list of options."
    },
    "location": {
        "help": "Search for a location and get an overview of every monster that appears in that location.",
        "location_name": "The name of the target location.",
        "options": "Manually select a location from a list of options."
    },
    "item": {
        "help": "Search for an item and get information on its effect, what abilities you can craft/learn from it, and where to find it.",
        "item_name": "The name of the target item.",
        "options": "Manually select an item from a list of options."
    },
    "customize": {
        "help": "Search for an auto-ability and get information on its effect, monsters that drop it, how to customize it, and where to find the required item.",
        "ability_name": "The name of the target auto-ability.",
        "options": "Manually select an auto-ability from a list of options."
    },
    "learn": {
        "help": "Search for an ability an aeon can learn and get information on how to learn it, and where to find the required item.",
        "ability_name": "The name of the target ability.",
        "options": "Manually select an ability from a list of options."
    },
    "rage": {
        "help": "Search for a Ronso Rage ability and get an overview of every monster Kimahri can learn this ability from.",
        "ronso_rage": "The name of the target Ronso rage.",
        "options": "Manually select a Ronso rage from a list of options."
    },
    "capture": {
        "help": "Search for a Monster Arena creation and get its requirements, unlock reward, an overview of it and the monsters needed to create it (if applicable).",
        "creation_name": "The name of the target creation.",
        "options": "Manually select a creation from a list of options."
    },
    "list": {
        "help": "Displays informative lists for quick reference.",
        "primers": "Displays the locations of all Al Bhed Primers.",
        "celestials": "Displays the locations and conditions of every celestial weapon and their respective items.",
        "rewards": {
            "help": "Displays lists of rewards. If no flag is used, all eight lists are printed in the order seen below.",
            "arena": "Displays all Monster Arena rewards.",
            "remiem": "Displays all rewards for fights against Belgemine at Remiem Temple.",
            "chocobo": "Displays all rewards for winning the chocobo races at Remiem Temple.",
            "training": "Displays all rewards for Chocobo Training in the Calm Lands.",
            "lightning": "Displays all rewards for Lightning Dodging in the Thunder Plains.",
            "cactuar": "Displays all possible rewards for doing the 'Valley of the Cactuars' sidequest in Bikanel.",
            "butterfly": "Displays all rewards for doing the butterfly hunts in Macalania Woods.",
            "other": "Displays other rewards (basically only for collecting all primers for now)."
        },
        "items": {
            "help": "Displays lists of items of various categories. If no flag is used, all five lists are printed in the order seen below.",
            "healing": "Displays all healing items.",
            "support": "Displays all protective items.",
            "attacking": "Displays all damage-dealing items.",
            "spheres": "Displays all Spheres.",
            "other": "Displays other items that don't fit the other categories."
        }
    }
}


HELPTEXT_VERBOSE = {
    "monster": {
        "help": "Search jaiosdaisdjaosidajsodiajfor a monster by name and get its stats, resistances, items and drops.",
        "monster_name": "The name of the target monster.",
        "allies": "Includes the allies of a boss monster, if it has any.",
        "options": "Manually select a monster from a list of options."
    },
    "location": {
        "help": "Search for a location and get an overview of every monster that appears in that location.",
        "location_name": "The name of the target location.",
        "options": "Manually select a location from a list of options."
    },
    "item": {
        "help": "Search for an item and get information on its effect, what abilities you can craft/learn from it, and where to find it.",
        "item_name": "The name of the target item.",
        "options": "Manually select an item from a list of options."
    },
    "customize": {
        "help": "Search for an auto-ability and get information on its effect, monsters that drop it, how to customize it, and where to find the required item.",
        "ability_name": "The name of the target auto-ability.",
        "options": "Manually select an auto-ability from a list of options."
    },
    "learn": {
        "help": "Search for an ability an aeon can learn and get information on how to learn it, and where to find the required item.",
        "ability_name": "The name of the target ability.",
        "options": "Manually select an ability from a list of options."
    },
    "rage": {
        "help": "Search for a Ronso Rage ability and get an overview of every monster Kimahri can learn this ability from.",
        "ronso_rage": "The name of the target Ronso rage.",
        "options": "Manually select a Ronso rage from a list of options."
    },
    "capture": {
        "help": "Search for a Monster Arena creation and get its requirements, unlock reward, an overview of it and the monsters needed to create it (if applicable).",
        "creation_name": "The name of the target creation.",
        "options": "Manually select a creation from a list of options."
    },
    "list": {
        "help": "Displays informative lists for quick reference.",
        "primers": "Displays the locations of all Al Bhed Primers.",
        "celestials": "Displays the locations and conditions of every celestial weapon and their respective items.",
        "rewards": {
            "help": "Displays lists of rewards. If no flag is used, all eight lists are printed in the order seen below.",
            "arena": "Displays all Monster Arena rewards.",
            "remiem": "Displays all rewards for fights against Belgemine at Remiem Temple.",
            "chocobo": "Displays all rewards for winning the chocobo races at Remiem Temple.",
            "training": "Displays all rewards for Chocobo Training in the Calm Lands.",
            "lightning": "Displays all rewards for Lightning Dodging in the Thunder Plains.",
            "cactuar": "Displays all possible rewards for doing the 'Valley of the Cactuars' sidequest in Bikanel.",
            "butterfly": "Displays all rewards for doing the butterfly hunts in Macalania Woods.",
            "other": "Displays other rewards (basically only for collecting all primers for now)."
        },
        "items": {
            "help": "Displays lists of items of various categories. If no flag is used, all five lists are printed in the order seen below.",
            "healing": "Displays all healing items.",
            "support": "Displays all protective items.",
            "attacking": "Displays all damage-dealing items.",
            "spheres": "Displays all Spheres.",
            "other": "Displays other items that don't fit the other categories."
        }
    }
}