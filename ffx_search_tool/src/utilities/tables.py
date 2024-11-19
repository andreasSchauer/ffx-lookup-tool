from rich.table import Table
from rich import box
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH
from ffx_search_tool.src.data import monsters, monster_arena
from ffx_search_tool.src.utilities.format_monster_data import format_monster_data
from rich.console import Console

console = Console()


def initialize_table(tab_title, num_columns, tab_header=True, column_names=[]):
    table = Table(title=tab_title, show_lines=True, expand=True, box=box.SQUARE, title_style="bold", show_header=tab_header)
    col_width = int(TABLE_WIDTH / num_columns)

    if len(column_names) == 0:
        for i in range(num_columns):
            table.add_column("", width=col_width)
    else:
        for i in range(int(num_columns / len(column_names))):
            for name in column_names:
                table.add_column(name, width=col_width)

    return table



def get_short_mon_table(monster_name): 
    locations = monsters[monster_name]["location"]
    title = get_catch_info(monster_name)
    monster_table = initialize_table(title, 2, tab_header=False)
    
    if "monster arena" in locations:
        table_keys = [
            ("Location", "location"),
            ("HP (Overkill)", "hp"),
            ("AP (Overkill)", "ap"),
            ("Steal (Rare Steal)", "steals"),
            ("Drop (Rare Drop)", "drops")]

        if monster_name in monster_arena:
            table_keys += [("Unlock Condition", "condition"), ("Reward", "reward")]
        
    elif "remiem temple" in locations:
        if monster_name == "mindy":
            return get_magus_table()
        
        table_keys = [
            ("HP (Overkill)", "hp"),
            ("First Victory Reward", "first reward"),
            ("Recurring Victory Reward", "recurring reward")]

    else:
        table_keys = [
            ("Location", "location"),
            ("HP (Overkill)", "hp"),
            ("AP (Overkill)", "ap"),
            ("Gil", "gil"),
            ("Steal (Rare Steal)", "steals"),
            ("Drop (Rare Drop)", "drops"),
            ("Bribe (Max Amount)", "bribe_max"),
            ("Ronso Rage", "ronso_rage")]

    for key in table_keys:
        monster_table.add_row(key[0], format_monster_data(key[1], monster_name))

    return monster_table


def get_catch_info(monster_name):
    monster = monsters[monster_name]
    is_not_catchable = (
        not monster["is_boss"]
        and "monster arena" not in monster["location"]
        and "remiem temple" not in monster["location"]
    )
    
    if monster["is_catchable"]:
        monster_name += " - Can be captured"
    elif is_not_catchable:
        monster_name += " - Can not be captured"

    return monster_name.title()


def get_magus_table():
    magus_table = initialize_table("Magus Sisters", 2, tab_header=False)
    
    magus_table.add_row("Cindy HP (Overkill)", format_monster_data("hp", "cindy"))
    magus_table.add_row("Sandy HP (Overkill)", format_monster_data("hp", "sandy"))
    magus_table.add_row("Mindy HP (Overkill)", format_monster_data("hp", "mindy"))
    magus_table.add_row("First Victory Reward", format_monster_data("first reward", "mindy"))
    magus_table.add_row("Recurring Victory Reward", format_monster_data("recurring reward", "mindy"))

    return magus_table