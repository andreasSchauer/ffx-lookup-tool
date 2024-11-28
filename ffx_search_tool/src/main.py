from typer import Typer, Argument, Option
from ffx_lookup_tool.src.main import format_input
from ffx_lookup_tool.src.search.ability_search import aeon_ability_search, auto_ability_search
from ffx_lookup_tool.src.search.monster_search import monster_search
from ffx_lookup_tool.src.search.location_search import location_search
from ffx_lookup_tool.src.search.item_search import item_search
from ffx_lookup_tool.src.search.other_searches import get_primer_table, get_celestial_table, ronso_rage_search, arena_creation_search, get_reward_table, get_items_table
from ffx_lookup_tool.src.Helptext import HELPTEXT
from ffx_lookup_tool.src.utilities.misc import validate_input
from ffx_lookup_tool.src.utilities.select import select

#{extras = ["all"], version = "^0.12.5"}

app = Typer()
list_app = Typer(help=HELPTEXT["list"]["description"])
app.add_typer(list_app, name="list")



@app.command(help=HELPTEXT["monster"]["description"])
def monster(
    monster_name: str = Argument(None, help=HELPTEXT["monster"]["monster_name"]),
    include_allies: bool = Option(False, "--allies", "-a", help=HELPTEXT["monster"]["allies"]),
    options: bool = Option(False, "--options", help=HELPTEXT["monster"]["options"])
):
    monster_name = validate_input(monster_name, "monster", options)
    monster_search(monster_name, include_allies)



@app.command(help=HELPTEXT["location"]["description"])
def location(
    location_name: str = Argument(None, help=HELPTEXT["location"]["location_name"]),
    options: bool = Option(False, "--options", help=HELPTEXT["location"]["options"])
):
    location_name = validate_input(location_name, "location", options)
    location_search(location_name)



@app.command(help=HELPTEXT["item"]["description"])
def item(item_name: str = Argument(None, help=HELPTEXT["item"]["item_name"]),
         options: bool = Option(False, "--options", help=HELPTEXT["item"]["options"])
):
    item_name = validate_input(item_name, "item", options)
    item_search(item_name)



@app.command(help=HELPTEXT["customize"]["description"])
def customize(
    ability_name: str = Argument(None, help=HELPTEXT["customize"]["ability_name"]),
    options: bool = Option(False, "--options", help=HELPTEXT["customize"]["options"])
):
    ability_name = validate_input(ability_name, "auto_ability", options)
    auto_ability_search(ability_name)



@app.command(help=HELPTEXT["learn"]["description"])
def learn(
    ability_name: str = Argument(None, help=HELPTEXT["learn"]["ability_name"]),
    options: bool = Option(False, "--options", help=HELPTEXT["learn"]["options"])
):
    ability_name = validate_input(ability_name, "aeon_ability", options)
    aeon_ability_search(ability_name)



@app.command(help=HELPTEXT["rage"]["description"])
def rage(
    ronso_rage: str = Argument(None, help=HELPTEXT["rage"]["ronso_rage"]),
    options: bool = Option(False, "--options", help=HELPTEXT["rage"]["options"])
):
    ronso_rage = validate_input(ronso_rage, "rage", options)
    ronso_rage_search(ronso_rage)



@app.command(help=HELPTEXT["capture"]["description"])
def capture(
    creation_name: str = Argument(None, help=HELPTEXT["capture"]["creation_name"]),
    options: bool = Option(False, "--options", help=HELPTEXT["capture"]["options"])
):
    creation_name = validate_input(creation_name, "creation", options)
    arena_creation_search(creation_name)



@list_app.command(help=HELPTEXT["list"]["primers"])
def primers():
    get_primer_table()



@list_app.command(help=HELPTEXT["list"]["celestials"])
def celestials():
    get_celestial_table()



@list_app.command(help=HELPTEXT["list"]["rewards"]["description"])
def rewards(
    monster_arena: bool = Option(False, "--arena", "-a", help=HELPTEXT["list"]["rewards"]["arena"]),
    remiem_temple: bool = Option(False, "--remiem", "-r", help=HELPTEXT["list"]["rewards"]["remiem"]),
    chocobo_races: bool = Option(False, "--chocobo", "-c", help=HELPTEXT["list"]["rewards"]["chocobo"]),
    chocobo_training: bool = Option(False, "--training", "-t", help=HELPTEXT["list"]["rewards"]["training"]),
    lightning_dodging: bool = Option(False, "--lightning", "-l", help=HELPTEXT["list"]["rewards"]["lightning"]),
    cactuar_valley: bool = Option(False, "--cactuar", "-q", help=HELPTEXT["list"]["rewards"]["cactuar"]),
    butterfly_hunt: bool = Option(False, "--butterfly", "-b", help=HELPTEXT["list"]["rewards"]["butterfly"]),
    other: bool = Option(False, "--other", "-o", help=HELPTEXT["list"]["rewards"]["other"])
):
    get_reward_table(**locals())



@list_app.command(help=HELPTEXT["list"]["items"]["description"])
def items(
    healing: bool = Option(False, "--healing", "-h", help=HELPTEXT["list"]["items"]["healing"]),
    support: bool = Option(False, "--support", "-p", help=HELPTEXT["list"]["items"]["support"]),
    attacking: bool = Option(False, "--attacking", "-a", help=HELPTEXT["list"]["items"]["attacking"]),
    spheres: bool = Option(False, "--spheres", "-s", help=HELPTEXT["list"]["items"]["spheres"]),
    other: bool = Option(False, "--other", "-o", help=HELPTEXT["list"]["items"]["other"])
):
    get_items_table(**locals())



if __name__ == "__main__":
    app()