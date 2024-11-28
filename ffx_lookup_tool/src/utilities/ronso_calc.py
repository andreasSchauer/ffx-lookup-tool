import sys

def get_kimahri_stats():
        kimahri_stats = {}
        kimahri_stats["hp"] = kimahri_stats_input("HP")
        kimahri_stats["str"] = kimahri_stats_input("Strength")
        kimahri_stats["mag"] = kimahri_stats_input("Magic")
        kimahri_stats["agl"] = kimahri_stats_input("Agility")

        return kimahri_stats


def kimahri_stats_input(key):
    try:
        if key == "HP":
            kimahri_stat = validate_stat_input("Enter Kimahri's max HP: ")

            if kimahri_stat < 644:
                raise ValueError("Kimahri's max HP can't be lower than 644.")
            
        else:
            kimahri_stat = validate_stat_input(f"Enter Kimahri's {key} stat: ")

            if not (0 <= kimahri_stat <= 255):
                raise ValueError("Stats must have a value from 0 to 255.")
        
        return kimahri_stat
    
    except ValueError as e:
            print(str(e))
            print("")
            print("Try again.")
            return kimahri_stats_input(key)


def validate_stat_input(input_msg):
    try:
        return int(input(input_msg))
    
    except ValueError:
        raise ValueError("Invalid Input.")
    except KeyboardInterrupt:
        print("\nInput cancelled.")
        sys.exit()



def get_ronso_hp(monster_name, kimahri_str, kimahri_mag):
    val_1 = kimahri_str ** 3
    val_2 = kimahri_mag ** 3
    val_3 = (val_1 + val_2) / 2 * 16 / 15

    HP_mod = round(((val_3 // 32) + 30) * 586 // 730) + 1

    if monster_name == "biran ronso":
        return [HP_mod * 8, 2500]

    if monster_name == "yenke ronso":
        return [HP_mod * 6, 2500]


def get_ronso_strength(monster_name, kimahri_hp):
    strength_vals = [11, 12, 13, 15, 17, 19, 21, 22, 23, 24, 25, 27]
    power_mod = (kimahri_hp - 644) // 200

    if power_mod > 11:
        power_mod = 11

    strength = strength_vals[power_mod]

    if monster_name == "yenke ronso":
        strength = strength // 2

    return strength


def get_ronso_magic(monster_name, kimahri_hp):
    magic_vals = [8, 8, 9, 10, 12, 14, 16, 17, 19, 20, 21, 22] 
    power_mod = (kimahri_hp - 644) // 200

    if power_mod > 11:
        power_mod = 11
    
    if power_mod < 0:
        raise Exception("Kimahri's max HP can't be lower than 644.")

    magic = magic_vals[power_mod]

    if monster_name == "biran ronso":
        magic = magic // 2

    return magic


def get_ronso_agility(monster_name, kimahri_agl):
    if monster_name == "biran ronso":
        agility = kimahri_agl - 4
    
    if monster_name == "yenke ronso":
        agility = kimahri_agl - 6

    if agility < 1:
        agility = 1

    return agility