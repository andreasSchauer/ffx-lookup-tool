TABLE_WIDTH = 100

MONSTER_TABLE_CELL_NAMES = {
    "stats":        [
                        "HP (Overkill)", "MP", "Strength",
                        "Defence", "Magic", "Magic Defence",
                        "Agility", "Luck", "Evasion", "Accuracy"
                    ],
    "elements":     [
                        "Fire", "Lightning", "Water", "Ice", "Holy", "Gravity"
                    ],
    "statusses":    [
                        "Silence", "Sleep", "Dark", "Poison (HP Loss)",
                        "Petrify", "Slow", "Zombie (Life)", "Power Break", "Magic Break",
                        "Armour Break", "Mental Break", "Threaten", "Death",
                        "Provoke", "Doom (Countdown)", "Delay", "Eject", "Zanmato"
                    ],
    "items":        [
                        "Steal (Normal)", "Steal (Rare)", "Drop (Normal)",
                        "Drop (Rare)", "Bribe"
                    ],
    "equipment":    [
                        "Drop Rate", "Slots Amount", "Number of Abilities",
                        "Weapon Abilities", "Armour Abilities"
                    ]
}


LOCATIONS = ["dream zanarkand", "baaj temple", "besaid", "s.s. liki", "kilika", "luca", "mi'ihen highroad", "mushroom rock road", "djose highroad", "moonflow", "thunder plains", "macalania", "bikanel", "home", "airship", "bevelle", "via purifico", "calm lands", "cavern of the stolen fayth", "mount gagazet", "zanarkand", "zanarkand dome", "sin", "omega ruins", "remiem temple", "monster arena"]


RONSO_RAGES = ["seed cannon", "self-destruct", "fire breath", "stone breath", "aqua breath", "thrust kick", "bad breath", "doom", "white wind", "mighty guard", "nova"]


COMMON_SPHERES = ["power sphere", "mana sphere", "speed sphere"]


DUPLICATES = {
    "anima": ["anima (remiem temple)", "anima (seymour)"],
    "bahamut": ["bahamut (remiem temple)", "spathi"],
    "bomb": ["bomb (mi'ihen highroad)", "bomb (home)"],
    "chimera": ["chimera (macalania)", "chimera (home)"],
    "dark ixion": ["dark ixion (first fight)", "dark ixion (second fight)"],
    "dual horn": ["dual horn (mi'ihen highroad)", "dual horn (home)"],
    "evil eye": ["evil eye (macalania)", "evil eye (home)"],
    "garuda": ["garuda (besaid)", "garuda (luca)", "garuda (mushroom rock road)"],
    "gemini": ["gemini 1", "gemini 2"],
    "guado guardian": ["guado guardian (seymour)", "guado guardian (macalania)", "guado guardian (home)"],
    "ifrit": ["ifrit (mi'ihen highroad)", "ifrit (remiem temple)", "grothia"],
    "ixion": ["ixion (moonflow)", "ixion (remiem temple)"],
    "mech scouter": ["mech scouter (normal)", "mech scouter (burning)"],
    "mimic": ["mimic (red)", "mimic (blue)", "mimic (yellow)", "mimic (green)"],
    "piranha": ["piranha x1", "piranha x2", "piranha x3"],
    "sahagin": ["sahagin (baaj temple)", "sahagin (via purifico, underwater)", "sahagin (via purifico, land)"],
    "shiva": ["shiva (calm lands)", "shiva (remiem temple)"],
    "sinscale": ["sinscale (zanarkand)", "sinscale (s.s. liki, boat)", "sinscale (s.s. liki, underwater)"],
    "sinspawn gui": ["sinspawn gui (first fight)", "sinspawn gui (second fight)"],
    "splasher": ["splasher x1", "splasher x2", "splasher x3"],
    "valefor": ["valefor (remiem temple)", "pterya"],
    "vouivre": ["vouivre (luca)", "vouivre (mi'ihen highroad)"],
    "yojimbo": ["yojimbo (cavern of the stolen fayth)", "yojimbo (remiem temple)"],
    "zu": ["zu (first encounter)", "zu (regular encounter)"]
}


SYNONYMS = {
    "braskas final aeon": ["braskas final aeon (first phase)", "braskas final aeon (second phase)"],
    "dark magus sisters": ["dark cindy", "dark sandy", "dark mindy"],
    "isaaru": ["grothia", "pterya", "spathi"],
    "magus sisters": ["cindy", "sandy", "mindy"],
    "seymour": ["seymour (first phase)", "seymour (second phase)"],
    "sinspawn geneaux": ["sinspawn geneaux (first phase)", "sinspawn geneaux (second phase)"]
}


REPLACEMENTS = {
    "dark aeons": {
        "mons": ["dark valefor", "dark ifrit", "dark ixion (first fight)", "dark ixion (second fight)", "dark shiva", "dark bahamut", "dark anima", "dark cindy", "dark sandy", "dark mindy"],
        "items": {
            "steal_common": [None, 0],
            "steal_rare": ["elixir", 1],
            "drop_common": ["dark matter", 1],
            "drop_rare": ["master sphere", 1]
        },
        "equipment": {
            "drop_rate": 0.99,
            "wpn_abilities": [
                {"ability": "break damage limit"}
            ],
            "armour_abilities": [
                {"ability": "break hp limit"},
                {"ability": "ribbon"}
            ]
        }
    },
    "monster arena creations": {
        "mons": ["stratoavis", "malboro menace", "kottos", "coeurlregina", "jormungand", "cactuar king", "espada", "abyss worm", "chimerageist", "don tonberry", "catoblepas", "abaddon", "vorban", "fenrir", "ornitholestes", "pteryx", "hornet", "vidatu", "one-eye", "jumbo flan", "nega elemental", "tanket", "fafnir", "sleep sprout", "bomb king", "juggernaut", "ironclad", "earth eater", "greater sphere", "catastrophe", "th'uban", "neslug", "ultima buster", "shinryu", "nemesis"],
        "items": {
            "steal_common": [None, 0],
            "steal_rare": [None, 0],
            "drop_common": [None, 0],
            "drop_rare": ["dark matter", 1]
        },
        "equipment": {
            "drop_rate": 0.99,
            "wpn_abilities": [],
            "armour_abilities": []
        }
    },
    "monster arena original creations": {
        "mons": ["earth eater", "greater sphere", "catastrophe", "th'uban", "neslug", "ultima buster", "shinryu"],
        "items": {
            "steal_common": ["gamblers spirit", 1],
            "steal_rare": [None, 0],
            "drop_common": [None, 0],
            "drop_rare": [None, 0]
        },
        "equipment": {
            "drop_rate": 0.99,
            "wpn_abilities": [],
            "armour_abilities": []
        }
    },
}


ITEM_CATEGORIES = {
    "healing": [0, 20],
    "support": [20, 32],
    "attacking": [32, 65],
    "spheres": [65, 95],
    "other": [95, 111]
}


CHARACTER_SPECIFIC_ABILITIES = {
    "piercing": "Kimahri and Auron only",
    "strength +3%": "everybody except Yuna and Lulu",
    "strength +5%": "everybody except Yuna and Lulu",
    "strength +10%": "everybody except Yuna and Lulu",
    "magic +3%": "Yuna and Lulu only",
    "magic +5%": "Yuna and Lulu only",
    "magic +10%": "Yuna and Lulu only"
}