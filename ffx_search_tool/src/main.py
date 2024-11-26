from typer import Typer, Argument, Option
from ffx_search_tool.src.search.ability_search import aeon_ability_search, auto_ability_search
from ffx_search_tool.src.search.monster_search import monster_search
from ffx_search_tool.src.search.location_search import location_search
from ffx_search_tool.src.search.item_search import item_search
from ffx_search_tool.src.search.other_searches import get_primer_table, get_celestial_table, ronso_rage_search, arena_creation_search, get_reward_table, get_items_table
from ffx_search_tool.src.utilities.select import select


app = Typer()
list_app = Typer()
app.add_typer(list_app, name="list")


@app.command()
def monster(
    monster_name: str = Argument(None, help="The target monster."),
    include_allies: bool = Option(False, "--allies", "-a", help="Include the allies of a boss monster."),
    options: bool = Option(False, "--options", help="Manually select a monster.")
):
    monster_name = validate_input(monster_name, "monster", options)
    monster_search(monster_name, include_allies)


@app.command()
def location(
    location_name: str = Argument(None, help="The target location."),
    options: bool = Option(False, "--options", help="Manually select a location.")
):
    location_name = validate_input(location_name, "location", options)
    location_search(location_name)



def validate_input(search_term, category, options=False):
    if options:
        search_term = select(category)

    if search_term is None:
        search_term = select(category, "No input was given.")

    return format_input(search_term)

def format_input(search_term):
    return search_term.lower().replace("_", " ").replace("auto ", "auto-")




@app.command()
def item(item_name: str = Argument(None, help="The target item."),
         options: bool = Option(False, "--options", help="Manually select an item.")
):
    item_name = validate_input(item_name, "item", options)
    item_search(item_name)


@app.command()
def customize(
    ability_name: str = Argument(None, help="The target auto-ability."),
    options: bool = Option(False, "--options", help="Manually select an auto-ability.")
):
    ability_name = validate_input(ability_name, "auto_ability", options)
    auto_ability_search(ability_name)


@app.command()
def learn(
    ability_name: str = Argument(None, help="The target ability."),
    options: bool = Option(False, "--options", help="Manually select an ability.")
):
    ability_name = validate_input(ability_name, "aeon_ability", options)
    aeon_ability_search(ability_name)


@app.command()
def rage(
    ronso_rage: str = Argument(None, help="The target Ronso rage."),
    options: bool = Option(False, "--options", help="Manually select a Ronso rage.")
):
    ronso_rage = validate_input(ronso_rage, "rage", options)
    ronso_rage_search(ronso_rage)


@app.command()
def capture(
    creation_name: str = Argument(None, help="The target Monster Arena creation."),
    options: bool = Option(False, "--options", help="Manually select a Monster Arena creation.")
):
    creation_name = validate_input(creation_name, "creation", options)
    arena_creation_search(creation_name)


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
    lightning_dodging: bool = Option(False, "--lightning", "-l", help="Show all rewards for Lightning Dodging in the Thunder Plains."),
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