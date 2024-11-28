# FFX Lookup Tool

A command-line tool for Final Fantasy X that can lookup monsters, items, abilities and more. If you need guidance on how to farm an item, how many of an item are needed for customizing an ability, or if you need the stats of a specific monster to aid you on your playthrough/challenge run: This tool will be of great assistance.


## Installation Instructions

need help


## Features and Usage

This tool uses various search commands which are explained below. Generally every search command only takes one string as input. The input will get converted to lowercase, underscores will be replaced with spaces.

Dashes are not yet accounted for, except for when typing an ability starting with "auto-", then you can also type "auto haste" for example.

For now, the search term needs to be an exact match (apart from the above exceptions), but if you type it in wrong, you will always be presented with options to guide you through the searching process within one or two steps. Most commands also have an --options option that does the same.

### Monster Search

Search for any monster by running:

```shell
ffx monster monster_name
```

This will give you the following information about the monster:
* Location
* Whether it can be captured
* Stats
* Elemental resistances 
* Status resistances
* AP and Gil rewards
* Available items (stealing, defeating, bribing)
* Equipment drops (including drop rate, amount of ability slots, and amount of abilities on the weapon/armour)
* If it has an ability for Kimahri to learn

The aeons you fight in Remiem Temple don't drop any items or equipment and have this section replaced with the reward you get for the initial and recurring victories.

Monster Arena creations have an extra table containing their unlock condition and reward and the monsters you need to capture to create it (if applicable).

**** Edge Cases

***** Duplicates

If there are several versions of a monster (for example Garuda appears in Besaid, Luca and Mushroom Rock Road with different stats), you will get asked to pick the desired version.

***** Biran and Yenke

If you search for Biran or Yenke Ronso, you will be asked to enter Kimahri's HP, Strength, Magic and Agility, since their own stats are determined by them. The tool will then calculate the stats for them.

***** Groups

Some monsters are part of a group, which means they get an extra identifier. Searching for the group name will give you the data of all monsters in the group. This is done, if they either have multiple phases with significant stat changes, or if the search_term itself is not a monster. Here are the currently used groups:

* "braskas final aeon" => braskas final aeon (first phase), braskas final aeon (second phase)
* "dark magus sisters" => dark cindy, dark sandy, dark mindy
* "issaru" => grothia, pterya, spathi
* "magus sisters" => cindy, sandy, mindy
* seymour => seymour (first phase), seymour (second phase)
* sinspawn geneaux => sinspawn geneaux (first phase), sinspawn geneaux (second phase)

**** --allies

With the --allies option activated, if the monster appears in a boss fight with multiple opponents (for example Seymour + Guado Guardians and Anima, or Sinspawn Gui and its body parts), this information is printed for every opponent that takes part in this fight.

If the exact monster appears in multiple boss fights, you will get asked to pick the desired fight, but that actually only applies to Yu Pagoda (Braskas Final Aeon and Yu Yevon).

*** Location Search

Search for any location by running:

```shell
ffx location location_name
```

This will give you a list of every monster that can be found in that location. The monsters are sorted based on availability:

* Reoccurring: These monsters can always be found for farming
* Not Reoccurring: These monsters only appear during certain parts of the story
* Boss Monsters

For every monster you will receive an overview that is not as detailed as when searching for the monster individually, but still gives you the following information:

* If the monster can be captured
* Location (in case they appear in multiple locations)
* The monster's HP
* AP and Gil rewards
* The monster's items (stealing, defeating, bribing)
* If the monster has an ability for Kimahri to learn

**** Edge Cases

If you search for Remiem Temple, you will only see the Aeon's HP, and the rewards that come with initial and recurring victories, since they have no items.

If you search for Monster Arena, you will get an overview of every Monster Arena Creation, and some redundant fields will be replaced with their unlock condition and unlock reward.

*** Item Search






