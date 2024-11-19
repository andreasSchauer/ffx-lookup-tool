from rich.table import Table
from rich import box
from ffx_search_tool.src.data import monsters
from ffx_search_tool.src.utilities.constants import TABLE_WIDTH
from ffx_search_tool.src.utilities.format_monster_data import format_monster_data, format_num
from ffx_search_tool.src.utilities.tables import initialize_table, console
from ffx_search_tool.src.utilities.filter_monsters import filter_monsters


def item_search(item_name):
    item_table = Table(pad_edge=False, box=box.MINIMAL_HEAVY_HEAD, width=TABLE_WIDTH, padding=1)
    item_table.add_column(item_name.title())
    
    farmable_monsters, one_time_monsters, boss_monsters = filter_monsters(item_name, "steal")
    not_farmable_monsters = one_time_monsters + boss_monsters

    print("reoccurring: ", farmable_monsters)
    print("not reoccurring: ", not_farmable_monsters)



