from ffx_search_tool.src.data import monsters


def filter_monsters(search_term, key, characters=False):
    filtered_mons = list(filter(create_filter(search_term, key, characters), monsters))
    is_location_search = key == "location"

    reoccuring_monsters = get_reoccurring_monsters(filtered_mons)
    one_time_monsters = get_one_time_monsters(filtered_mons)
    boss_monsters = get_boss_monsters(filtered_mons, include_allies=is_location_search)

    monster_lists = [reoccuring_monsters, one_time_monsters, boss_monsters]

    if not is_location_search:
        if accessible_via_dark_yojimbo(search_term, key):
            reoccuring_monsters.append("dark yojimbo")
            dark_yojimbo = boss_monsters.index("dark yojimbo")
            boss_monsters.pop(dark_yojimbo)

    return monster_lists


def accessible_via_dark_yojimbo(search_term, key):
    match (key):
        case "steal":
            return search_term in ["stamina tonic", "elixir"]
        case "drop":
            return search_term in ["dark matter", "master sphere"]
        case "equipment":
            is_dark_yojimbo_weapon = has_ability("dark yojimbo", "wpn_abilities", search_term)
            is_dark_yojimbo_armour = has_ability("dark yojimbo", "armour_abilities", search_term)
            return is_dark_yojimbo_weapon or is_dark_yojimbo_armour


def create_filter(search_term, key, characters=False):
    def inner(mon):
        match (key):
            case "steal":
                item_1 = get_item(mon, "steal_common")
                item_2 = get_item(mon, "steal_rare")
                return search_term == item_1 or search_term == item_2
            case "drop":
                item_1 = get_item(mon, "drop_common")
                item_2 = get_item(mon, "drop_rare")
                return search_term == item_1 or search_term == item_2
            case "bribe":
                return search_term == get_item(mon, "bribe")
            case "equipment":
                has_wpn_ability = has_ability(mon, "wpn_abilities", search_term, characters)
                has_armour_ability = has_ability(mon, "armour_abilities", search_term, characters)
                return has_wpn_ability or has_armour_ability
            case "location":
                return search_term in monsters[mon]["location"]
    return inner


def get_item(monster_name, key):
    item_data = monsters[monster_name]["items"][key]
    
    if item_data is not None:
        if isinstance(item_data[0], list):
            return item_data[1][0]

        return item_data[0]


def has_ability(monster_name, key, search_term, characters=False):
    abilities = monsters[monster_name]["equipment"][key]
    
    if abilities is None:
        return False
    
    if characters:
        return any(item["ability"] == search_term  and "characters" in item for item in abilities)

    return any(item["ability"] == search_term and "characters" not in item for item in abilities)
    



def get_reoccurring_monsters(mons):
    return list(filter(lambda mon: monsters[mon]["is_reoccurring"], mons))


def get_one_time_monsters(mons):
    return list(filter(lambda mon: not monsters[mon]["is_reoccurring"] and not monsters[mon]["is_boss"], mons))


def get_boss_monsters(mons, include_allies=False):
    boss_monsters = list(filter(lambda mon: monsters[mon]["is_boss"], mons))

    if not include_allies:
        return boss_monsters

    boss_monsters_sorted = []

    for boss in boss_monsters:
        if monsters[boss]["has_allies"]:
            for ally in monsters[boss]["allies"]:
                if ally not in boss_monsters_sorted and not isinstance(ally, list):
                    boss_monsters_sorted.append(ally)
        else:
            boss_monsters_sorted.append(boss)

    return boss_monsters_sorted