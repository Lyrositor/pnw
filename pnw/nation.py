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
    Approval: {0.approval}
    Vacation Mode: {0.vacation_mode}
    City/Project Timer: {0.city_project_timer_turns} turns

    Score: {0.score}
    GDP: {0.gdp}
    Population: {0.population}
    Infrastructure: {0.infrastructure}
    Land: {0.land}

    Domestic Policy: {0.domestic_policy}
    War Policy: {0.war_policy}
    Social Policy: {0.social_policy}
    Economic Policy: {0.economic_policy}

    Soldiers: {0.soldiers}
        Casualties: {0.soldier_casualties}
        Killed: {0.soldiers_killed}

    Tanks: {0.tanks}
        Lost: {0.tank_casualties}
        Destroyed: {0.tanks_killed}

    Aircraft: {0.aircraft}
        Lost: {0.aircraft_casualties}
        Destroyed: {0.aircraft_killed}

    Ships: {0.ships}
        Lost: {0.ship_casualties}
        Destroyed: {0.ships_killed}

    Missiles: {0.missiles}
        Launched: {0.missiles_launched}
        Eaten: {0.missiles_eaten}

    Nuclear Weapons: {0.nukes}
        Launched: {0.nukes_launched}
        Eaten: {0.nukes_eaten}

    Infrastructure Destroyed: {0.infrastructure_destroyed}

    Location: ({0.latitude}, {0.longitude})
    Flag URL: {0.flag}
    Unique ID: {0.uniqueid}

    Revenue:
        Money: ${1[0]}
        Food: {1[1]} tons
        Coal: {1[2]} tons
        Oil: {1[3]} tons
        Uranium: {1[4]} tons
        Iron: {1[5]} tons
        Bauxite: {1[6]} tons
        Lead: {1[7]} tons
        Gasoline: {1[8]} tons
        Steel: {1[9]} tons
        Aluminum: {1[10]} tons
        Munitions: {1[11]} tons
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
            missiles=0, missiles_launched=0, missiles_eaten=0,
            nukes=0, nukes_launched=0, nukes_eaten=0,
            infrastructure_destroyed=0.0,
            domestic_policy=MANIFEST_DESTINY,
            war_policy=FORTRESS,
            social_policy="", economic_policy="",
            city_project_timer_turns=0, latitude=0.0, longitude=0.0,
            vacation_mode=False, cities=None, projects=None
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

        self.cities = cities if cities else []
        self.projects = projects if projects else []

    @property
    def alliance(self):

        #if self.alliance_id:
        #    return self.game.alliances[self.alliance_id]
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

        score = 0
        return score

    @property
    def gdp(self):

        gdp = 0.0
        return gdp

    @property
    def revenue(self):

        return {
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

        self.missiles = d['missiles']
        self.missiles_launched = d['missilelaunched']
        self.missiles_eaten = d['missileseaten']

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
