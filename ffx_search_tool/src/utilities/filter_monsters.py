from ffx_search_tool.src.data import monsters



def filter_monsters(search_term, key):
    filtered_mons = list(filter(create_filter(search_term, key), monsters))
    key_is_location = key == "location"

    reoccuring_monsters = get_reoccurring_monsters(filtered_mons)
    one_time_monsters = get_one_time_monsters(filtered_mons)
    boss_monsters = get_boss_monsters(filtered_mons, include_allies=key_is_location)

    return reoccuring_monsters, one_time_monsters, boss_monsters


def create_filter(search_term, key):
    def inner(mon):
        monster = monsters[mon]
        match (key):
            case "steal":
                item_1 = get_item(monster, "steal_normal")
                item_2 = get_item(monster, "steal_rare")
                return search_term == item_1 or search_term == item_2
            case "drop":
                item_1 = get_item(monster, "drop_normal")
                item_2 = get_item(monster, "drop_rare")
                return search_term == item_1 or search_term == item_2
            case "bribe":
                return search_term == get_item(monster, "bribe")
            case "equipment":
                has_wpn_ability = has_ability(monster, "wpn_abilities", search_term)
                has_armour_ability = has_ability(monster, "armour_abilities", search_term)
                return has_wpn_ability or has_armour_ability
            case "location":
                return search_term in monster["location"]
    return inner


def get_item(monster, key):
    item = None
    
    if monster["items"][key] is not None:
        item = monster["items"][key][0]

    return item


def has_ability(monster, key, search_term):
    abilities = monster["equipment"][key]
    
    if abilities is None:
        return False
    
    return any(item["ability"] == search_term for item in abilities)
    



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