from .continent import Continent
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

################
# Improvements #
################

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
AIR_FORCE = None
NAVAL_SHIPS = None
SPIES = None
MISSILES = None
NUCLEAR_WEAPONS = None

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
IRONWORKS = Project(
        "Ironworks",
        {MONEY: 5000000, ALUMINUM: 750, GASOLINE: 1500}
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
MASS_IRRIGATION = Project(
        "Mass Irrigation",
        {MONEY: 3000000, ALUMINUM: 500, STEEL: 500}
)
INT_TRADE_CENTER = Project(
        "International Trade Center",
        {MONEY: 45000000, ALUMINUM: 2500, STEEL: 2500, GASOLINE: 5000}
)
MISSILE_L_PAD = Project(
        "Missile Launch Pad",
        {MONEY: 8000000, STEEL: 1000, GASOLINE: 350}
)
NUCLEAR_RES_FAC = Project(
        "Nuclear Research Facility",
        {MONEY: 50000000, STEEL: 5000, GASOLINE: 7500}
)
IRON_DOME = Project(
        "Iron Dome",
        {MONEY: 6000000, ALUMINUM: 500, STEEL: 1250, GASOLINE: 500}
)
VITAL_DEF_SYS = Project(
        "Vital Defense System",
        {MONEY: 40000000, ALUMINUM: 3000, STEEL: 6500, GASOLINE: 5000}
)
URANIUM_ENRICH = Project(
        "Uranium Enrichment Program",
        {MONEY: 21000000, ALUMINUM: 1000, GASOLINE: 1000, URANIUM: 500}
)
PROP_BUREAU = Project(
        "Propaganda Bureau",
        {MONEY: 15000000, ALUMINUM: 1500}
)

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