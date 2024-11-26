from typer import Typer, Argument, Option
from ffx_search_tool.src.search.ability_search import aeon_ability_search, auto_ability_search
from ffx_search_tool.src.search.monster_search import monster_search
from ffx_search_tool.src.search.location_search import location_search
from ffx_search_tool.src.search.item_search import item_search
from ffx_search_tool.src.search.other_searches import get_primer_table, get_celestial_table, ronso_rage_search, arena_creation_search, get_reward_table, get_items_table
from ffx_search_tool.src.CLI_utility import validate_input, HELP


app = Typer()
list_app = Typer(help=HELP["list"]["help"])
app.add_typer(list_app, name="list")

    

@app.command(help=HELP["monster"]["help"])
def monster(
    monster_name: str = Argument(None, help=HELP["monster"]["monster_name"]),
    include_allies: bool = Option(False, "--allies", "-a", help=HELP["monster"]["allies"]),
    options: bool = Option(False, "--options", help=HELP["monster"]["options"])
):
    f"""{HELP["monster"]["help"]}

    {HELP["monster"]["verbose"]}
    """
    monster_name = validate_input(monster_name, "monster", options)
    monster_search(monster_name, include_allies)



@app.command(help=HELP["location"]["help"])
def location(
    location_name: str = Argument(None, help=HELP["location"]["location_name"]),
    options: bool = Option(False, "--options", help=HELP["location"]["options"])
):
    location_name = validate_input(location_name, "location", options)
    location_search(location_name)



@app.command(help=HELP["item"]["help"])
def item(item_name: str = Argument(None, help=HELP["item"]["item_name"]),
         options: bool = Option(False, "--options", help=HELP["item"]["options"])
):
    item_name = validate_input(item_name, "item", options)
    item_search(item_name)



@app.command(help=HELP["customize"]["help"])
def customize(
    ability_name: str = Argument(None, help=HELP["customize"]["ability_name"]),
    options: bool = Option(False, "--options", help=HELP["customize"]["options"])
):
    ability_name = validate_input(ability_name, "auto_ability", options)
    auto_ability_search(ability_name)



@app.command(help=HELP["learn"]["help"])
def learn(
    ability_name: str = Argument(None, help=HELP["learn"]["ability_name"]),
    options: bool = Option(False, "--options", help=HELP["learn"]["options"])
):
    ability_name = validate_input(ability_name, "aeon_ability", options)
    aeon_ability_search(ability_name)



@app.command(help=HELP["rage"]["help"])
def rage(
    ronso_rage: str = Argument(None, help=HELP["rage"]["ronso_rage"]),
    options: bool = Option(False, "--options", help=HELP["rage"]["options"])
):
    ronso_rage = validate_input(ronso_rage, "rage", options)
    ronso_rage_search(ronso_rage)



@app.command(help=HELP["capture"]["help"])
def capture(
    creation_name: str = Argument(None, help=HELP["capture"]["creation_name"]),
    options: bool = Option(False, "--options", help=HELP["capture"]["options"])
):
    creation_name = validate_input(creation_name, "creation", options)
    arena_creation_search(creation_name)



@list_app.command(help=HELP["list"]["primers"])
def primers():
    get_primer_table()



@list_app.command(help=HELP["list"]["celestials"])
def celestials():
    get_celestial_table()



@list_app.command(help=HELP["list"]["rewards"]["help"])
def rewards(
    monster_arena: bool = Option(False, "--arena", "-a", help=HELP["list"]["rewards"]["arena"]),
    remiem_temple: bool = Option(False, "--remiem", "-r", help=HELP["list"]["rewards"]["remiem"]),
    chocobo_races: bool = Option(False, "--chocobo", "-c", help=HELP["list"]["rewards"]["chocobo"]),
    chocobo_training: bool = Option(False, "--training", "-t", help=HELP["list"]["rewards"]["training"]),
    lightning_dodging: bool = Option(False, "--lightning", "-l", help=HELP["list"]["rewards"]["lightning"]),
    cactuar_valley: bool = Option(False, "--cactuar", "-q", help=HELP["list"]["rewards"]["cactuar"]),
    butterfly_hunt: bool = Option(False, "--butterfly", "-b", help=HELP["list"]["rewards"]["butterfly"]),
    other: bool = Option(False, "--other", "-o", help=HELP["list"]["rewards"]["other"])
):
    get_reward_table(**locals())



@list_app.command(help=HELP["list"]["items"]["help"])
def items(
    healing: bool = Option(False, "--healing", "-h", help=HELP["list"]["items"]["healing"]),
    support: bool = Option(False, "--support", "-p", help=HELP["list"]["items"]["support"]),
    attacking: bool = Option(False, "--attacking", "-a", help=HELP["list"]["items"]["attacking"]),
    spheres: bool = Option(False, "--spheres", "-s", help=HELP["list"]["items"]["spheres"]),
    other: bool = Option(False, "--other", "-o", help=HELP["list"]["items"]["other"])
):
    get_items_table(**locals())


if __name__ == "__main__":
    app()