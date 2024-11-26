from typer import Typer, Option
from ffx_search_tool.src.search.ability_search import aeon_ability_search, auto_ability_search
from ffx_search_tool.src.search.monster_search import monster_search
from ffx_search_tool.src.search.location_search import location_search
from ffx_search_tool.src.search.item_search import item_search
from ffx_search_tool.src.search.other_searches import get_primer_table, get_celestial_table, ronso_rage_search, get_monster_arena_table, get_reward_table, get_items_table


app = Typer()
list_app = Typer()
app.add_typer(list_app, name="list")


@app.command()
def monster(
    monster_name: str,
    include_allies: bool = Option(False, "--allies", "-a", help="Include the allies of a boss monster.")
):
    monster_search(monster_name, include_allies)


@app.command()
def location(location_name: str):
    location_search(location_name)


@app.command()
def item(item_name: str):
    item_search(item_name)


@app.command()
def customize(ability_name: str):
    auto_ability_search(ability_name)


@app.command()
def learn(ability_name: str):
    aeon_ability_search(ability_name)


@app.command()
def rage(ronso_rage: str):
    ronso_rage_search(ronso_rage)


@app.command()
def capture(creation_name: str):
    get_monster_arena_table(creation_name)


@list_app.command()
def primers():
    get_primer_table()


@list_app.command()
def celestials():
    get_celestial_table()


@list_app.command()
def rewards(
    monster_arena: bool = Option(False, "--arena", "-a", help="Show all Monster Arena rewards."),
    remiem_temple: bool = Option(False, "--remiem", "-r", help="Show all rewards for fights against Belgemine at Remiem Temple."),
    chocobo_races: bool = Option(False, "--chocobo", "-c", help="Show all rewards for winning the chocobo races at Remiem Temple."),
    chocobo_training: bool = Option(False, "--training", "-t", help="Show all rewards for Chocobo Training in the Calm Lands."),
    lightning_dodging: bool = Option(False, "--dodges", "-d", help="Show all rewards for Lightning Dodging in the Thunder Plains."),
    cactuar_valley: bool = Option(False, "--cactuar", "-q", help="Show all possible rewards for doing the 'Valley of the Cactuars' sidequest in Bikanel."),
    butterfly_hunt: bool = Option(False, "--butterfly", "-b", help="Show all rewards for doing the butterfly hunts in Macalania Woods."),
    other: bool = Option(False, "--other", "-o", help="Show other rewards (basically only collecting all primers).")
):
    get_reward_table(**locals())


@list_app.command()
def items(
    healing: bool = Option(False, "--healing", "-h", help="Display healing items."),
    support: bool = Option(False, "--support", "-p", help="Display protective items."),
    attacking: bool = Option(False, "--attacking", "-a", help="Display damage-dealing items."),
    spheres: bool = Option(False, "--spheres", "-s", help="Display Spheres."),
    other: bool = Option(False, "--other", "-o", help="Display other items that don't fit the other categories.")
):
    get_items_table(**locals())