class BankObjects:
    """Banks seen across Gielinor and the interfaces you can click on."""

    r = "./Images/bank/"

    # Bank
    bank = (50, 30, 210)
    bank_floor = (50, 50, 200)

    # Bank tabs (Roman Numerals)
    tab_i = r + "tab_i.png"
    tab_ii = r + "tab_ii.png"
    tab_iii = r + "tab_iii.png"
    tab_iv = r + "tab_iv.png"
    tab_v = r + "tab_v.png"
    tab_vi = r + "tab_vi.png"
    tab_vii = r + "tab_vii.png"
    tab_viii = r + "tab_viii.png"
    tab_ix = r + "tab_ix.png"
    tab_all = r + "tab_all.png"

    # Quantities
    quantity_1 = r + "quantity_1.png"
    quantity_5 = r + "quantity_5.png"
    quantity_10 = r + "quantity_10.png"
    quantity_x = r + "quantity_x.png"
    quantity_all = r + "quantity_all.png"

    # Misc Bank
    bank_pin_screen = r + "bank_pin_screen.png"
    withdraw_5 = r + "withdraw_5.png"
    withdraw_6 = r + "withdraw_6.png"
    withdraw_10 = r + "withdraw_10.png"
    withdraw_14 = r + "withdraw_14.png"
    withdraw_40 = r + "withdraw_40.png"
    withdraw_x = r + "withdraw_x.png"
    withdraw_all = r + "withdraw_all.png"
    deposit_inventory = r + "deposit_inventory.png"
    deposit_equipment = r + "deposit_equipment.png"
    notes = r + "notes.png"

    # Specific locations
    fossil_island = r + "fossil_island.png"
    hosidius = r + "hosidius.png"
    farming_guild = r + "farming_guild.png"


class ChatMenuObjects:
    """Selections that will be made in the chat"""

    r = "./Images/chat_menus/"

    al_kharid = r + "al_kharid.png"
    draynor_village = r + "draynor_village.png"
    edgeville = r + "edgeville.png"
    karamja = r + "karamja.png"
    fossil_island = r + "fossil_island.png"


class Food:
    """Anything edible!"""

    r = "./Images/food/"

    lobster = r + "lobster.png"


class GlobalColorObjects:
    """All the common colors that will be reused."""

    # Closed door
    closed_door = (150, 50, 200)

    # Inventory
    food = (0, 255, 0)
    last_inv = (41, 53, 62)

    # Out of Bounds
    oob_tile = (255, 90, 0)

    fairy_ring = (80, 10, 120)

    altar = (244, 138, 87)

    # Farming Patches
    tree_patch = (115, 190, 0)

    # MushTrees
    mush_tree = (200, 30, 220)


class ItemObjects:
    """All items in Gielinor"""

    r = "./Images/items/"

    hammerstone_seeds = r + "hammerstone_seeds.png"
    dragon_axe = r + "dragon_axe.png"
    ectophial = r + "ectophial.png"
    seed_box = r + "seed_box.png"
    bottomless_bucket = r + "bottomless_bucket.png"
    ring_of_dueling = r + "ring_of_dueling.png"
    empty_birdnest = r + "empty_birdnest.png"
    fire_battlestaff = r + "fire_battlestaff.png"

    # An image of 5 seeds together
    herb_seed = r + "herb_seeds.png"
    limpwurt_seed = r + "limpwurt_seeds.png"

    sapling = r + "sapling.png"

    # Equipment
    dramen_staff = r + "dramen_staff.png"
    sickle = r + "sickle.png"

    # Logs
    logs = r + "logs.png"
    oak_logs = r + "oak_logs.png"
    willow_logs = r + "willow_logs.png"
    yew_logs = r + "yew_logs.png"
    maple_logs = r + "maple_logs.png"
    teak_logs = r + "teak_logs.png"
    mahogany_logs = r + "mahogany_logs.png"
    redwood_logs = r + "redwood_logs.png"
    magic_logs = r + "magic_logs.png"

    # Herbs
    clean_ranarr = r + "clean_ranarr.png"
    clean_avantoe = r + "clean_avantoe.png"
    clean_kwuarm = r + "clean_kwuarm.png"
    clean_snapdragon = r + "clean_snapdragon.png"
    clean_toadflax = r + "clean_toadflax.png"

    # Unfinished Potions
    vial_of_water = r + "vial_of_water.png"
    avantoe_potion_unf = r + "avantoe_potion_unf.png"
    toadflax_potion_unf = r + "toadflax_potion_unf.png"

    # Potion Secondaries
    mort_myre_fungus = r + "mort_myre_fungus.png"
    amylase_crystal = r + "amylase_crystal.png"
    super_energy = r + "super_energy.png"
    crushed_nest = r + "crushed_nest.png"

    # Crafting
    molten_glass = r + "molten_glass.png"
    battlestaff = r + "battlestaff.png"
    water_orb = r + "water_orb.png"
    earth_orb = r + "earth_orb.png"
    fire_orb = r + "fire_orb.png"
    air_orb = r + "air_orb.png"

    # Payments
    coins = r + "coins.png"
    basket_of_apples = r + "basket_of_apples.png"
    basket_of_oranges = r + "basket_of_oranges.png"
    coconut = r + "coconut.png"
    cactus_spine = r + "cactus_spine.png"

    # Teleport tablets
    taverly_tablet = r + "taverly_tablet.png"

    # Seeds
    onion_seed = r + "onion_seed.png"

    clockwork = r + "clockwork.png"


class LoginObjects:
    """All the different login icons to get into the game."""

    r = "./Images/login/"

    play_now_button = r + "play_now.png"
    click_to_play_button = r + "click_here_to_play.png"
    temp_play_now = r + "temp_play_now.png"
    try_again = r + "try_again.png"
    ok = r + "ok.png"
    world_switch_logout = r + "world_switch_logout.png"


class MenuObjects:
    """Subcontext menus to click on when using an item."""

    r = "./Images/menu/"

    # Jewelry
    rub = r + "rub.png"

    # Digsite Pendant
    fossil_island = r + "fossil_island.png"

    # Mushtree (Fossil Island)
    mushroom_meadow = r + "mushroom_meadow.png"
    verdant_valley = r + "verdant_valley.png"
    outside = r + "outside.png"
    activity = r + "select.png"
    fishing_trawler = r + "fishing_trawler.png"
    minigame_teleport = r + "minigame_teleport.png"

    # Ardougne Cloak
    monastery = r + "monastery.png"
    farm = r + "farm.png"

    # Explorers Ring
    teleport = r + "teleport.png"

    # Ring of Dueling
    castle_wars = r + "castle_wars.png"

    # Farming
    ## In the Seed Vault interface
    saplings = r + "saplings.png"
    willow_sapling = r + "willow_sapling.png"
    maple_sapling = r + "maple_sapling.png"
    yew_sapling = r + "yew_sapling.png"
    magic_sapling = r + "magic_sapling.png"
    ## Mouse tooltip
    diseased_herbs = r + "diseased_herbs.png"

    # Amulet of Glory
    al_kharid = r + "al_kharid.png"
    draynor_village = r + "draynor_village.png"
    edgeville = r + "edgeville.png"
    karamja = r + "karamja.png"


class MiscObjects:
    """If it doesn't fall into any of the other categories, it'll go here."""

    r = "./Images/misc/"

    # Currently woodcutting
    woodcutting = r + "woodcutting.png"

    # Stunned from Pickpocketing
    stunned = r + "stunned.png"

    # Switch World Bounty Hunter
    switch_world = r + "switch_world.png"

    good = r + "good.png"

    # Birdhouses
    bh1 = r + "birdhouse_1.png"
    bh2 = r + "birdhouse_2.png"
    bh3 = r + "birdhouse_3.png"
    bh4 = r + "birdhouse_4.png"


class NormalSpellObjects:
    """Any spell found in all the spell boooks."""

    r = "./Images/normal_spellbook/"

    trollheim = r + "trollheim.png"
    varrock = r + "varrock.png"
    home = r + "home.png"
    ardy = r + "ardougne.png"
    camelot = r + "camelot.png"
    house = r + "house.png"
    lumby = r + "lumbridge.png"
    falador = r + "falador.png"
    high_alchemy = r + "high_alch.png"


class PathingObjects:
    """Oh the places you'll go"""

    step_1 = (0, 200, 200)
    step_2 = (20, 250, 200)
    step_3 = (80, 150, 200)
    step_4 = (100, 20, 150)
    step_5 = (210, 100, 170)
    step_6 = (40, 240, 120)
    step_7 = (150, 40, 40)
    step_8 = (140, 200, 200)
    step_9 = (150, 140, 40)
    step_10 = (85, 180, 170)


class PlayerObjects:
    """Any information about the player's state."""

    r = "Images\\player\\"

    player_tile = (240, 170, 0)
    most_health = (7, 25, 136)


class RuneObjects:
    """All the magical runes."""

    r = "./Images/runes/"

    air = r + "air.png"
    earth = r + "earth.png"
    water = r + "water.png"
    fire = r + "fire.png"
    death = r + "death.png"
    cosmic = r + "cosmic.png"
    nature = r + "nature.png"
    mind = r + "mind.png"
    chaos = r + "chaos.png"
    blood = r + "blood.png"
    law = r + "law.png"


class ToolObjects:
    """Any tools to be used in Gielinor"""

    r = "./Images/tools/"

    chisel = r + "chisel.png"
    glassblowing_pipe = r + "glassblowing_pipe.png"
    hammer = r + "hammer.png"
    magic_secateurs = r + "magic_secateurs.png"
    pestle_and_mortar = r + "pestle_and_mortar.png"
    rake = r + "rake.png"
    seed_dibber = r + "seed_dibber.png"
    spade = r + "spade.png"


class ToolTips:
    r = "./Images/tooltips/"

    bank_booth = r + "bank_booth.png"
    grand_exchange = r + "grand_exchange.png"
    bank_chest = r + "bank_chest.png"


class WearableObjects:
    """Teleport jewelry!"""

    r = "./Images/wearables/"

    # Teleport Jewelry
    digsite_pendant = r + "digsite_pendant.png"
    ring_of_dueling = r + "ring_of_dueling.png"
    skills_necklace = r + "skills_necklace.png"
    amulet_of_glory = r + "amulet_of_glory.png"

    # Diary equipment
    ardougne_cloak = r + "ardougne_cloak.png"
    explorers_ring = r + "explorers_ring.png"

    # Rogue Outfit
    rogue_boots = r + "rogue_boots.png"
    rogue_gloves = r + "rogue_gloves.png"
    rogue_top = r + "rogue_top.png"
    rogue_trousers = r + "rogue_trousers.png"
    rogue_mask = r + "rogue_mask.png"

    rabbits_foot = r + "rabbits_foot.png"
