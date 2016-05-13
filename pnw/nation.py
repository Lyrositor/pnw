from datetime import datetime
import grequests

from .city import City
from .data import *

NATION_REPR = """{0.prename} {0.name} (#{0.id}) {{
    Leader: {0.leader_title} {0.leader}
    Continent: {0.continent}
    Color: {0.color}
    Government: {0.government}
    Alliance: {0.alliance}
    Founded: {0.founded}
    Minutes Since Active: {0.inactive:,}m
    Approval: {0.approval:.2f}
    Vacation Mode: {0.vacation_mode}
    City/Project Timer: {0.city_project_timer_turns} turns

    Score: {0.score:,.2f}
    GDP: ${0.gdp:,.2f}
    Population: {0.population:,}
    Infrastructure: {0.infrastructure:,.2f}
    Land: {0.land:,.2f}

    Domestic Policy: {0.domestic_policy}
    War Policy: {0.war_policy}
    Social Policy: {0.social_policy}
    Economic Policy: {0.economic_policy}

    Soldiers: {0.soldiers:,}
    Tanks: {0.tanks:,}
    Aircraft: {0.aircraft:,}
    Ships: {0.ships:,}
    Missiles: {0.missiles:,}
    Nuclear Weapons: {0.nukes:,}

    Infrastructure Destroyed: {0.infrastructure_destroyed:,}

    Location: ({0.latitude:.2f}, {0.longitude:.2f})
    Flag URL: {0.flag}
    Unique ID: {0.uniqueid}

    Revenue:
        Money: ${1[0]:,.2f}
        Food: {1[1]:,.2f} tons
        Coal: {1[2]:,.2f} tons
        Oil: {1[3]:,.2f} tons
        Uranium: {1[4]:,.2f} tons
        Iron: {1[5]:,.2f} tons
        Bauxite: {1[6]:,.2f} tons
        Lead: {1[7]:,.2f} tons
        Gasoline: {1[8]:,.2f} tons
        Steel: {1[9]:,.2f} tons
        Aluminum: {1[10]:,.2f} tons
        Munitions: {1[11]:,.2f} tons
}}"""


class Nation:

    def __init__(
            self, game, id, name="", prename="", leader="", leader_title="",
            continent=NORTH_AMERICA, color=BEIGE, inactive=0,
            uniqueid="", government="", alliance_id=0, flag=None,
            founded=datetime.now(), approval=0.0,
            soldiers=0, soldier_casualties=0, soldiers_killed=0,
            tanks=0, tank_casualties=0, tanks_killed=0,
            aircraft=0, aircraft_casualties=0, aircraft_killed=0,
            ships=0, ship_casualties=0, ships_killed=0,
            spies=0, spies_lost=0, spies_captured=0,
            missiles=0, missiles_launched=0, missiles_eaten=0,
            nukes=0, nukes_launched=0, nukes_eaten=0,
            infrastructure_destroyed=0.0,
            domestic_policy=MANIFEST_DESTINY,
            war_policy=FORTRESS,
            social_policy="", economic_policy="",
            city_project_timer_turns=0, latitude=0.0, longitude=0.0,
            vacation_mode=False, at_war=False, cities=None, projects=None
    ):

        self.game = game

        self.id = id
        self.name = name
        self.prename = prename
        self.leader = leader
        self.leader_title = leader_title
        self.continent = continent
        self.color = color
        self.inactive = inactive
        self.uniqueid = uniqueid
        self.government = government
        self.alliance_id = alliance_id
        self.flag = flag
        self.founded = founded
        self.approval = approval

        self.soldiers = soldiers
        self.soldier_casualties = soldier_casualties
        self.soldiers_killed = soldiers_killed

        self.tanks = tanks
        self.tank_casualties = tank_casualties
        self.tanks_killed = tanks_killed

        self.aircraft = aircraft
        self.aircraft_casualties = aircraft_casualties
        self.aircraft_killed = aircraft_killed

        self.ships = ships
        self.ship_casualties = ship_casualties
        self.ships_killed = ships_killed

        self.spies = spies
        self.spies_lost = spies_lost
        self.spies_captured = spies_captured

        self.missiles = missiles
        self.missiles_launched = missiles_launched
        self.missiles_eaten = missiles_eaten

        self.nukes = nukes
        self.nukes_launched = nukes_launched
        self.nukes_eaten = nukes_eaten

        self.infrastructure_destroyed = infrastructure_destroyed

        self.domestic_policy = domestic_policy
        self.war_policy = war_policy
        self.social_policy = social_policy
        self.economic_policy = economic_policy

        self.city_project_timer_turns = city_project_timer_turns
        self.latitude = latitude
        self.longitude = longitude
        self.vacation_mode = vacation_mode
        self.at_war = at_war

        self.cities = cities if cities else []
        self.projects = projects if projects else []

    @property
    def alliance(self):

        if self.alliance_id and self.alliance_id in self.game.alliances:
            return self.game.alliances[self.alliance_id]
        return None

    @property
    def infrastructure(self):

        infrastructure = 0.0
        for city in self.cities:
            infrastructure += city.infrastructure
        return infrastructure

    @property
    def land(self):

        land = 0.0
        for city in self.cities:
            land += city.land
        return land

    @property
    def population(self):

        population = 0
        for city in self.cities:
            population += city.population
        return population

    @property
    def score(self):

        return (self.infrastructure * 0.025 +
                len(self.projects) * 20 +
                50 * max(0, len(self.cities) - 1) +
                0.0005 * self.soldiers +
                0.05 * self.tanks +
                0.5 * self.aircraft +
                2 * self.ships +
                5 * self.missiles +
                15 * self.nukes)

    @property
    def gdp(self):
        """
            Note: GDP calculation is approximate for now, until a more
            accurate formula is found.
        """

        prod = self.production

        return (
                   self.gross_revenue +
                   sum([prod[p] * v[1] for p, v in self.game.prices.items()])
               ) * 365.25

    @property
    def gross_revenue(self):

        r = 0
        for city in self.cities:
            r += city.population * (1 + city.commerce/50) * 0.725

        bonus = 1
        if self.color == BEIGE:
            bonus += 0.05
        elif self.color != GRAY:
            bonus += 0.03
        if self.alliance:
            bonus *= 1 + min(self.alliance.treasures * 2, 20) / 100
        bonus = min(bonus, 1.20)
        if self.domestic_policy is OPEN_MARKETS:
            bonus *= 1.01
        r *= bonus

        return r

    @property
    def production(self):

        production = {
            MONEY: self.gross_revenue,
            FOOD: 0,
            COAL: 0,
            OIL: 0,
            URANIUM: 0,
            IRON: 0,
            BAUXITE: 0,
            LEAD: 0,
            GASOLINE: 0,
            STEEL: 0,
            ALUMINUM: 0,
            MUNITIONS: 0
        }

        for city in self.cities:
            for improvement, n in city.improvements.items():
                for resource, upkeep in improvement.upkeep.items():
                    if upkeep > 0 and (not improvement.power or (
                                improvement.power and city.powered)):
                        production[resource] += upkeep * n

            production[FOOD] += city.improvements[FARM] * city.land

        season = self.game.get_season(self.continent)
        if season is SUMMER:
            production[FOOD] *= SUMMER_MOD
        elif season is WINTER:
            production[FOOD] *= WINTER_MOD

        if MASS_IRRIGATION in self.projects:
            production[FOOD] *= FOOD_PROD_MI
        else:
            production[FOOD] *= FOOD_PROD

        if ARMS_STOCKPILE in self.projects:
            production[MUNITIONS] *= ARMS_STOCKPILE_MOD
        if BAUXITEWORKS in self.projects:
            production[ALUMINUM] *= BAUXITEWORKS_MOD
        if EM_GAS_RESERVE in self.projects:
            production[GASOLINE] *= EM_GAS_RESERVE_MOD
        if IRONWORKS in self.projects:
            production[STEEL] *= IRONWORKS_MOD
        if URANIUM_ENRICH in self.projects:
            production[URANIUM] *= URANIUM_ENRICH_MOD

        return production

    @property
    def usage(self):

        usage = {
            MONEY: 0,
            FOOD: 0,
            COAL: 0,
            OIL: 0,
            URANIUM: 0,
            IRON: 0,
            BAUXITE: 0,
            LEAD: 0,
            GASOLINE: 0,
            STEEL: 0,
            ALUMINUM: 0,
            MUNITIONS: 0
        }

        for city in self.cities:
            for improvement, n in city.improvements.items():
                for resource, upkeep in improvement.upkeep.items():
                    if upkeep < 0:
                        usage[resource] += upkeep * n

        if ARMS_STOCKPILE in self.projects:
            usage[LEAD] *= ARMS_STOCKPILE_MOD
        if BAUXITEWORKS in self.projects:
            usage[BAUXITE] *= BAUXITEWORKS_MOD
        if EM_GAS_RESERVE in self.projects:
            usage[OIL] *= EM_GAS_RESERVE_MOD
        if IRONWORKS in self.projects:
            usage[IRON] *= IRONWORKS_MOD
            usage[COAL] *= IRONWORKS_MOD

        military = 0
        if self.at_war:
            military -= self.soldiers * SOLDIERS.upkeep_war[MONEY]
            usage[FOOD] -= self.soldiers * SOLDIERS.upkeep_war[FOOD]
            military -= self.tanks * TANKS.upkeep_war[MONEY]
            military -= self.aircraft * AIR_FORCE.upkeep_war[MONEY]
            military -= self.ships * NAVAL_SHIPS.upkeep_war[MONEY]
            military -= self.spies * SPIES.upkeep_war[MONEY]
            military -= self.missiles * MISSILES.upkeep_war[MONEY]
            military -= self.nukes * NUCLEAR_WEAPONS.upkeep_war[MONEY]
        else:
            military -= self.soldiers * SOLDIERS.upkeep[MONEY]
            usage[FOOD] -= self.soldiers * SOLDIERS.upkeep[FOOD]
            military -= self.tanks * TANKS.upkeep[MONEY]
            military -= self.aircraft * AIR_FORCE.upkeep[MONEY]
            military -= self.ships * NAVAL_SHIPS.upkeep[MONEY]
            military -= self.spies * SPIES.upkeep[MONEY]
            military -= self.missiles * MISSILES.upkeep[MONEY]
            military -= self.nukes * NUCLEAR_WEAPONS.upkeep[MONEY]
        if self.domestic_policy is IMPERIALISM:
            military *= 0.95
        usage[MONEY] += military

        usage[FOOD] -= self.population / 1000

        for city in self.cities:
            infra = city.infrastructure

            infra -= 250 * city.improvements[WIND_POWER]
            if infra <= 0:
                continue

            for i in range(city.improvements[NUCLEAR_POWER]):
                for n in range(2):
                    usage[URANIUM] -= 1.2
                    infra -= 1000
                    if infra <= 0:
                        break
                if infra <= 0:
                    break
            if infra <= 0:
                continue

            for i in range(city.improvements[OIL_POWER]):
                for n in range(5):
                    usage[OIL] -= 1.2
                    infra -= 100
                    if infra <= 0:
                        break
                if infra <= 0:
                    break
            if infra <= 0:
                continue

            for i in range(city.improvements[COAL_POWER]):
                for n in range(5):
                    usage[COAL] -= 1.2
                    infra -= 100
                    if infra <= 0:
                        break
                if infra <= 0:
                    break

        return usage

    @property
    def revenue(self):

        prod = self.production
        usage = self.usage
        revenue = {key: prod[key] + usage[key] for key in prod}
        if self.alliance:
            if revenue[MONEY] > 0:
                revenue[MONEY] *= (1 - self.alliance.revenue_tax)
            for resource in prod:
                if resource is not MONEY and revenue[resource] > 0:
                    revenue[resource] *= 1 - self.alliance.resource_tax
        return revenue

    def update(self, response, *args, **kwargs):

        if response.status_code != 200:
            return
        d = response.json()

        self.id = int(d['nationid'])
        self.name = d['name']
        self.prename = d['prename']
        self.leader = d['leadername']
        self.leader_title = d['title']
        self.continent = CONTINENTS[d['continent']]
        self.color = COLORS[d['color']]
        self.inactive = d['minutessinceactive']
        self.uniqueid = d['uniqueid']
        self.government = d['government']
        self.alliance_id = int(d['allianceid'])
        self.flag = d['flagurl']
        self.founded = datetime.strptime(d['founded'], "%Y-%m-%d %H:%M:%S")
        self.approval = float(d['approvalrating'])

        self.soldiers = int(d['soldiers'])
        self.soldier_casualties = int(d['soldiercasualties'])
        self.soldiers_killed = int(d['soldierskilled'])

        self.tanks = int(d['tanks'])
        self.tank_casualties = int(d['tankcasualties'])
        self.tanks_killed = int(d['tankskilled'])

        self.aircraft = int(d['aircraft'])
        self.aircraft_casualties = int(d['aircraftcasualties'])
        self.aircraft_killed = int(d['aircraftkilled'])

        self.ships = int(d['ships'])
        self.ship_casualties = int(d['shipcasualties'])
        self.ships_killed = int(d['shipskilled'])

        self.missiles = int(d['missiles'])
        self.missiles_launched = int(d['missilelaunched'])
        self.missiles_eaten = int(d['missileseaten'])

        self.nukes = int(d['nukes'])
        self.nukes_launched = int(d['nukeslaunched'])
        self.nukes_eaten = int(d['nukeseaten'])

        self.infrastructure_destroyed = float(d['infdesttot'])

        self.domestic_policy = DOMESTIC_POLICIES[d['domestic_policy']]
        self.war_policy = WAR_POLICIES[d['war_policy']]
        self.social_policy = d['socialpolicy']
        self.economic_policy = d['ecopolicy']

        self.city_project_timer_turns = int(d['cityprojecttimerturns'])
        self.latitude = float(d['latitude'])
        self.longitude = float(d['longitude'])

        self.cities = [City(self.game, int(id), self.id) for id in d['cityids']]
        self.projects = {p for s, p in PROJECTS.items() if d[s] == '1'}

    def fetch(self):

        return grequests.get(
                self.game.URL + 'nation/id={}'.format(self.id),
                headers={'User-Agent': self.game.USER_AGENT},
                callback=self.update
        )

    def __repr__(self):

        revenue = self.revenue
        return NATION_REPR.format(self, revenue)
