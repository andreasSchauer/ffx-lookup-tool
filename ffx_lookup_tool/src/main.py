from typer import Typer, Argument, Option
from ffx_lookup_tool.src.search.ability_search import aeon_ability_search, auto_ability_search
from ffx_lookup_tool.src.search.monster_search import monster_search
from ffx_lookup_tool.src.search.location_search import location_search
from ffx_lookup_tool.src.search.item_search import item_search
from ffx_lookup_tool.src.search.other_searches import get_primer_table, get_celestial_table, ronso_rage_search, arena_creation_search, get_reward_table, get_items_table
from ffx_lookup_tool.src.utilities.select import select
from ffx_lookup_tool.src.data import helptext



app = Typer()
list_app = Typer(help=helptext["list"]["description"])
app.add_typer(list_app, name="list")



def validate_input(search_term, category, options=False):
    if options:
        search_term = select(category)

    if search_term is None:
        search_term = select(category, "No input was given.")

    return format_input(search_term)


def format_input(search_term):
    return search_term.lower().replace("_", " ").replace("auto ", "auto-").strip(" ")



@app.command(help=helptext["monster"]["description"])
def monster(
    monster_name: str = Argument(None, help=helptext["monster"]["monster_name"]),
    include_allies: bool = Option(False, "--allies", "-a", help=helptext["monster"]["allies"]),
    options: bool = Option(False, "--options", help=helptext["monster"]["options"])
):
    monster_name = validate_input(monster_name, "monster", options)
    monster_search(monster_name, include_allies)



@app.command(help=helptext["location"]["description"])
def location(
    location_name: str = Argument(None, help=helptext["location"]["location_name"]),
    options: bool = Option(False, "--options", help=helptext["location"]["options"])
):
    location_name = validate_input(location_name, "location", options)
    location_search(location_name)



@app.command(help=helptext["item"]["description"])
def item(item_name: str = Argument(None, help=helptext["item"]["item_name"]),
         options: bool = Option(False, "--options", help=helptext["item"]["options"])
):
    item_name = validate_input(item_name, "item", options)
    item_search(item_name)



@app.command(help=helptext["customize"]["description"])
def customize(
    ability_name: str = Argument(None, help=helptext["customize"]["ability_name"]),
    options: bool = Option(False, "--options", help=helptext["customize"]["options"])
):
    ability_name = validate_input(ability_name, "auto_ability", options)
    auto_ability_search(ability_name)



@app.command(help=helptext["learn"]["description"])
def learn(
    ability_name: str = Argument(None, help=helptext["learn"]["ability_name"]),
    options: bool = Option(False, "--options", help=helptext["learn"]["options"])
):
    ability_name = validate_input(ability_name, "aeon_ability", options)
    aeon_ability_search(ability_name)



@app.command(help=helptext["rage"]["description"])
def rage(
    ronso_rage: str = Argument(None, help=helptext["rage"]["ronso_rage"]),
    options: bool = Option(False, "--options", help=helptext["rage"]["options"])
):
    ronso_rage = validate_input(ronso_rage, "rage", options)
    ronso_rage_search(ronso_rage)



@app.command(help=helptext["capture"]["description"])
def capture(
    creation_name: str = Argument(None, help=helptext["capture"]["creation_name"]),
    options: bool = Option(False, "--options", help=helptext["capture"]["options"])
):
    creation_name = validate_input(creation_name, "creation", options)
    arena_creation_search(creation_name)



@list_app.command(help=helptext["list"]["primers"])
def primers():
    get_primer_table()



@list_app.command(help=helptext["list"]["celestials"])
def celestials():
    get_celestial_table()



@list_app.command(help=helptext["list"]["rewards"]["description"])
def rewards(
    monster_arena: bool = Option(False, "--arena", "-a", help=helptext["list"]["rewards"]["arena"]),
    remiem_temple: bool = Option(False, "--remiem", "-r", help=helptext["list"]["rewards"]["remiem"]),
    chocobo_races: bool = Option(False, "--chocobo", "-c", help=helptext["list"]["rewards"]["chocobo"]),
    chocobo_training: bool = Option(False, "--training", "-t", help=helptext["list"]["rewards"]["training"]),
    lightning_dodging: bool = Option(False, "--lightning", "-l", help=helptext["list"]["rewards"]["lightning"]),
    cactuar_valley: bool = Option(False, "--cactuar", "-q", help=helptext["list"]["rewards"]["cactuar"]),
    butterfly_hunt: bool = Option(False, "--butterfly", "-b", help=helptext["list"]["rewards"]["butterfly"]),
    other: bool = Option(False, "--other", "-o", help=helptext["list"]["rewards"]["other"])
):
    get_reward_table(**locals())



@list_app.command(help=helptext["list"]["items"]["description"])
def items(
    healing: bool = Option(False, "--healing", "-h", help=helptext["list"]["items"]["healing"]),
    support: bool = Option(False, "--support", "-p", help=helptext["list"]["items"]["support"]),
    attacking: bool = Option(False, "--attacking", "-a", help=helptext["list"]["items"]["attacking"]),
    spheres: bool = Option(False, "--spheres", "-s", help=helptext["list"]["items"]["spheres"]),
    other: bool = Option(False, "--other", "-o", help=helptext["list"]["items"]["other"])
):
    get_items_table(**locals())



if __name__ == "__main__":
    app()