from rich.table import Table
from rich import box
from ffx_search_tool.src.data import primers, celestials, monsters, monster_arena
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH, RONSO_RAGES
from ffx_search_tool.src.utilities.tables import initialize_table, get_short_mon_table, console
from ffx_search_tool.src.utilities.table_data import get_table_data


def get_primer_table():
    wrapper_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    wrapper_table.add_column("Al Bhed Primers")
    primer_table = initialize_table("", 3, column_names=["Primer", "Translation", "Location"])
    wrapper_table.add_row(primer_table)

    for primer in primers:
        num = primer["num"]
        translation = primer["translation"]
        location = primer["location"]

        if isinstance(location, list):
            location = " / ".join(location)

        primer_table.add_row(num, translation, location)

    console.print(wrapper_table)


def get_celestial_table():
    wrapper_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    wrapper_table.add_column("Celestial Items and Weapons")
    celestial_table = initialize_table("", 2, column_names=["Item / Weapon", "Location"])
    wrapper_table.add_row(celestial_table)

    for celestial in celestials:
        item = celestial["item"].title()
        location = celestial["location"]
        celestial_table.add_row(item, location)

    console.print(wrapper_table)



def get_ronso_rage_table(ronso_rage):
    if ronso_rage not in RONSO_RAGES:
        ronso_rage = select_rage()
    
    ronso_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    ronso_table.add_column(ronso_rage.title())

    monster_list = []

    for monster_key in monsters.keys():
        monster = monsters[monster_key]
        rage = monster["ronso_rage"]

        if rage is not None and (rage == ronso_rage or ronso_rage in rage):
            monster_list.append(monster_key)

    for monster in monster_list:
        ronso_table.add_row(get_short_mon_table(monster))

    console.print(ronso_table)


def select_rage():
    for i, rage in enumerate(RONSO_RAGES):
        print(f"{i + 1}: {rage.title()}")
        
    choice = int(input("Rage not found. Choose by number: ")) - 1
    return RONSO_RAGES[choice]



def get_monster_arena_table(creation_name):
    if creation_name not in monster_arena:
        creation_name = select_creation()

    creation = monster_arena[creation_name]
    
    monster_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    monster_table.add_column(creation_name.title())
    monster_table.add_row(get_short_mon_table(creation_name))


    if "monsters" in creation:
        for monster_name in creation["monsters"]:
            monster_table.add_row(get_short_mon_table(monster_name))

    

    console.print(monster_table)


def select_creation():
    keys = monster_arena.keys()
    for i, creation in enumerate(keys):
        print(f"{i + 1}: {creation.title()}")
        
    choice = int(input("Creation not found. Choose by number: ")) - 1
    chosen_key = list(keys)[choice]
    return chosen_key


