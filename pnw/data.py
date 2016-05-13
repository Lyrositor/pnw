from .continent import Continent
from .improvement import *
from .military import MilitaryUnit
from .project import Project

#############
# Resources #
#############

MONEY = 0

# Raw
FOOD = 1
COAL = 2
OIL = 3
URANIUM = 4
IRON = 5
BAUXITE = 6
LEAD = 7

# Manufactured
GASOLINE = 8
STEEL = 9
ALUMINUM = 10
MUNITIONS = 11

##########
# Colors #
##########

AQUA = 0
BLACK = 1
BLUE = 2
BROWN = 3
GREEN = 4
LIME = 5
MAROON = 6
OLIVE = 7
ORANGE = 8
PINK = 9
PURPLE = 10
RED = 11
WHITE = 12
YELLOW = 13
BEIGE = 14
GRAY = 15

COLORS = {
    "aqua": AQUA,
    "black": BLACK,
    "blue": BLUE,
    "brown": BROWN,
    "green": GREEN,
    "lime": LIME,
    "maroon": MAROON,
    "olive": OLIVE,
    "orange": ORANGE,
    "pink": PINK,
    "purple": PURPLE,
    "red": RED,
    "white": WHITE,
    "yellow": YELLOW,
    "beige": BEIGE,
    "gray": GRAY
}

##############
# Continents #
##############

NORTH_AMERICA = Continent("North America", (COAL, IRON, URANIUM))
SOUTH_AMERICA = Continent("South America", (OIL, BAUXITE, LEAD))
EUROPE = Continent("Europe", (COAL, IRON, LEAD))
AFRICA = Continent("Africa", (OIL, BAUXITE, URANIUM))
ASIA = Continent("Asia", (OIL, IRON, URANIUM))
AUSTRALIA = Continent("Australia", (COAL, BAUXITE, LEAD))

CONTINENTS = {
    "North America": NORTH_AMERICA,
    "South America": SOUTH_AMERICA,
    "Europe": EUROPE,
    "Africa": AFRICA,
    "Asia": ASIA,
    "Australia": AUSTRALIA
}

#####################
# Domestic Policies #
#####################

MANIFEST_DESTINY = 0
OPEN_MARKETS = 1
TECHNOLOGICAL_ADVANCEMENT = 2
IMPERIALISM = 3
URBANIZATION = 4

DOMESTIC_POLICIES = {
    "Manifest Destiny": MANIFEST_DESTINY,
    "Open Markets": OPEN_MARKETS,
    "Technologial Advancement": TECHNOLOGICAL_ADVANCEMENT,
    "Imperialism": IMPERIALISM,
    "Urbanization": URBANIZATION
}

############
# Military #
############

SOLDIERS = MilitaryUnit(
    "Soldiers",
    {MONEY: 2},
    {MONEY: 1.25, FOOD: 1 / 750},
    {MONEY: 1.88, FOOD: 1 / 500},
    {MUNITIONS: 1 / 5000}
)
TANKS = MilitaryUnit(
    "Tanks",
    {MONEY: 60, STEEL: 1},
    {MONEY: 50},
    {MONEY: 75},
    {MUNITIONS: 1 / 100, GASOLINE: 1 / 100}
)
AIR_FORCE = MilitaryUnit(
    "Air Force",
    {MONEY: 4000, ALUMINUM: 3},
    {MONEY: 500},
    {MONEY: 750},
    {MUNITIONS: 1/4, GASOLINE: 1/4}
)
NAVAL_SHIPS = MilitaryUnit(
    "Naval Ships",
    {MONEY: 50000, STEEL: 25},
    {MONEY: 3750},
    {MONEY: 5625},
    {MUNITIONS: 3, GASOLINE: 2}
)
SPIES = MilitaryUnit(
    "Spies",
    {MONEY: 50000},
    {MONEY: 2400},
    {MONEY: 2400},
    {}
)
MISSILES = MilitaryUnit(
    "Missiles",
    {MONEY: 150000, ALUMINUM: 100, GASOLINE: 75, MUNITIONS: 75},
    {MONEY: 21000},
    {MONEY: 31500},
    {}
)
NUCLEAR_WEAPONS = MilitaryUnit(
    "Nuclear Weapons",
    {MONEY: 1750000, ALUMINUM: 750, GASOLINE: 500, URANIUM: 250},
    {MONEY: 35000},
    {MONEY: 52500},
    {}
)

################
# Improvements #
################

COAL_POWER = Improvement("Coal Power", {MONEY: 5000}, {MONEY: -1200}, 8)
OIL_POWER = Improvement("Oil Power", {MONEY: 7000}, {MONEY: -1800}, 6)
NUCLEAR_POWER = Improvement("Nuclear Power", {MONEY: 500000, STEEL: 100}, {MONEY: -10500})
WIND_POWER = Improvement("Wind Power", {MONEY: 30000, ALUMINUM: 25}, {MONEY: -500})
COAL_MINE = Improvement("Coal Mine", {MONEY: 1000}, {MONEY: -400, COAL: 6}, 6)
OIL_WELL = Improvement("Oil Well", {MONEY: 1500}, {MONEY: -600, OIL: 9}, 6)
BAUXITE_MINE = Improvement("Bauxite Mine", {MONEY: 9500}, {MONEY: -1600, BAUXITE: 6}, 6)
IRON_MINE = Improvement("Iron Mine", {MONEY: 9500}, {MONEY: -1600, IRON: 6}, 6)
LEAD_MINE = Improvement("Lead Mine", {MONEY: 7500}, {MONEY: -1500, LEAD: 9}, 6)
URANIUM_MINE = Improvement("Uranium Mine", {MONEY: 25000}, {MONEY: -5000, URANIUM: 3}, 10)
FARM = Improvement("Farm", {MONEY: 1000}, {MONEY: -300}, 1)
OIL_REFINERY = Improvement("Oil Refinery", {MONEY: 45000}, {MONEY: -4000, OIL: -3, GASOLINE: 6}, 16, True)
STEEL_MILL = Improvement("Steel Mill", {MONEY: 45000}, {MONEY: -4000, IRON: -3, COAL: -3, STEEL: 9}, 20, True)
ALUMINUM_REFINERY = Improvement("Aluminum Refinery", {MONEY: 30000}, {MONEY: -2500, BAUXITE: -3, ALUMINUM: 9}, 20, True)
MUNITIONS_FACTORY = Improvement("Munitions Factory", {MONEY: 35000}, {MONEY: -3500, LEAD: -6, MUNITIONS: 18}, 16, True)
POLICE_STATION = Improvement("Police Station", {MONEY: 75000, STEEL: 20}, {MONEY: -750}, 1, True)
HOSPITAL = Improvement("Hospital", {MONEY: 100000, ALUMINUM: 25}, {MONEY: -1000}, 4, True)
RECYCLING_CENTER = Improvement("Recycling Center", {MONEY: 125000}, {MONEY: -2500}, -70, True)
SUBWAY = CommerceImprovement("Subway", {MONEY: 250000, STEEL: 50, ALUMINUM: 25}, {MONEY: -3250}, 7, -45)
SUPERMARKET = CommerceImprovement("Supermarket", {MONEY: 5000}, {MONEY: -600}, 4)
BANK = CommerceImprovement("Bank", {MONEY: 1500, STEEL: 5, ALUMINUM: 10}, {MONEY: -1800}, 7)
SHOPPING_MALL = CommerceImprovement("Shopping Mall", {MONEY: 45000, STEEL: 20, ALUMINUM: 25}, {MONEY: -5400}, 12, 2)
STADIUM = CommerceImprovement("Stadium", {MONEY: 100000, STEEL: 40, ALUMINUM: 50}, {MONEY: -12150}, 18, 5)
BARRACKS = MilitaryImprovement("Barracks", {MONEY: 3000}, {SOLDIERS: 3000})
FACTORY = MilitaryImprovement("Factory", {MONEY: 15000}, {TANKS: 250})
AIR_FORCE_BASE = MilitaryImprovement("Air Force Base", {MONEY: 100000, STEEL: 10}, {AIR_FORCE: 18})
DRYDOCK = MilitaryImprovement("Drydock", {MONEY: 250000, ALUMINUM: 20}, {NAVAL_SHIPS: 5})

############
# Projects #
############

ARMS_STOCKPILE = Project(
        "Arms Stockpile",
        {MONEY: 4000000, ALUMINUM: 125, STEEL: 125}
)
BAUXITEWORKS = Project(
        "Bauxiteworks",
        {MONEY: 5000000, STEEL: 750, GASOLINE: 1500}
)
CEN_CIV_ENG = Project(
        "Center for Civil Engineering",
        {MONEY: 3000000, OIL: 1000, IRON: 1000, BAUXITE: 1000}
)
CEN_INT_AGNCY = Project(
        "Central Intelligence Agency",
        {MONEY: 5000000, STEEL: 500, GASOLINE: 500}
)
EM_GAS_RESERVE = Project(
        "Emergency Gasoline Reserve",
        {MONEY: 4000000, ALUMINUM: 125, STEEL: 125}
)
INT_TRADE_CENTER = Project(
        "International Trade Center",
        {MONEY: 45000000, ALUMINUM: 2500, STEEL: 2500, GASOLINE: 5000}
)
IRON_DOME = Project(
        "Iron Dome",
        {MONEY: 6000000, ALUMINUM: 500, STEEL: 1250, GASOLINE: 500}
)
IRONWORKS = Project(
        "Ironworks",
        {MONEY: 5000000, ALUMINUM: 750, GASOLINE: 1500}
)
MASS_IRRIGATION = Project(
        "Mass Irrigation",
        {MONEY: 3000000, ALUMINUM: 500, STEEL: 500}
)
MISSILE_L_PAD = Project(
        "Missile Launch Pad",
        {MONEY: 8000000, STEEL: 1000, GASOLINE: 350}
)
NUCLEAR_RES_FAC = Project(
        "Nuclear Research Facility",
        {MONEY: 50000000, STEEL: 5000, GASOLINE: 7500}
)
PROP_BUREAU = Project(
        "Propaganda Bureau",
        {MONEY: 15000000, ALUMINUM: 1500}
)
URANIUM_ENRICH = Project(
        "Uranium Enrichment Program",
        {MONEY: 21000000, ALUMINUM: 1000, GASOLINE: 1000, URANIUM: 500}
)
VITAL_DEF_SYS = Project(
        "Vital Defense System",
        {MONEY: 40000000, ALUMINUM: 3000, STEEL: 6500, GASOLINE: 5000}
)

FOOD_PROD = 1 / 25
FOOD_PROD_MI = 12 / 250

ARMS_STOCKPILE_MOD = 1.34
BAUXITEWORKS_MOD = 1.36
EM_GAS_RESERVE_MOD = 2.00
IRONWORKS_MOD = 1.36
URANIUM_ENRICH_MOD = 2.00

PROJECTS = {
    "ironworks": IRONWORKS,
    "bauxiteworks": BAUXITEWORKS,
    "armsstockpile": ARMS_STOCKPILE,
    "emgasreserve": EM_GAS_RESERVE,
    "massirrigation": MASS_IRRIGATION,
    "inttradecenter": INT_TRADE_CENTER,
    "missilelpad": MISSILE_L_PAD,
    "nuclearresfac": NUCLEAR_RES_FAC,
    "irondome": IRON_DOME,
    "vitaldefsys": VITAL_DEF_SYS,
    "cenintagncy": CEN_INT_AGNCY,
    "uraniumenrich": URANIUM_ENRICH,
    "propbureau": PROP_BUREAU,
    "cenciveng": CEN_CIV_ENG
}

###########
# Seasons #
###########

SUMMER = 1
FALL = 2
WINTER = -1
SPRING = -2

SUMMER_MOD = 1.2
WINTER_MOD = 0.8

################
# War Policies #
################

ATTRITION = 0
TURTLE = 1
BLITZKRIEG = 2
FORTRESS = 3
MONEYBAGS = 4
PIRATE = 5
TACTICIAN = 6
GUARDIAN = 7
COVERT = 8
ARCANE = 9

WAR_POLICIES = {
    "Attrition": ATTRITION,
    "Turtle": TURTLE,
    "Blitzkrieg": BLITZKRIEG,
    "Fortress": FORTRESS,
    "Moneybags": MONEYBAGS,
    "Pirate": PIRATE,
    "Tactician": TACTICIAN,
    "Guardian": GUARDIAN,
    "Covert": COVERT,
    "Arcane": ARCANE
}