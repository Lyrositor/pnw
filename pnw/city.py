import grequests

from .data import *

CITY_REPR = """{0.name} (#{0.id}) {{
    Age: {0.age:,}
    Powered: {0.powered}

    Infrastructure: {0.infrastructure:,.2f}
    Land: {0.land:,.2f}
    Population: {0.population:,}
    Pollution: {0.pollution}
    Crime: {0.crime:.2f}%
    Disease: {0.disease:.2f}%
    Commerce: {0.commerce}
}}"""


class City:

    def __init__(
            self, game, id, nation_id, name="", age=0, infrastructure=10.0,
            land=20.0, nuclear_pollution=0, coal_power=0, oil_power=0,
            nuclear_power=0, wind_power=0, coal_mine=0, oil_well=0, iron_mine=0,
            bauxite_mine=0, lead_mine=0, uranium_mine=0, farm=0, oil_refinery=0,
            steel_mill=0, aluminum_refinery=0, munitions_factory=0,
            police_station=0, hospital=0, recycling_center=0, subway=0,
            supermarket=0, bank=0, shopping_mall=0, stadium=0, barracks=0,
            factory=0, air_force_base=0,
            drydock=0
    ):

        self.game = game

        self.id = id
        self.nation_id = nation_id
        self.name = name
        self.age = age
        self.infrastructure = infrastructure
        self.land = land
        self.nuclear_pollution = nuclear_pollution

        self.improvements = {
            COAL_POWER: coal_power,
            OIL_POWER: oil_power,
            NUCLEAR_POWER: nuclear_power,
            WIND_POWER: wind_power,
            COAL_MINE: coal_mine,
            OIL_WELL: oil_well,
            IRON_MINE: iron_mine,
            BAUXITE_MINE: bauxite_mine,
            LEAD_MINE: lead_mine,
            URANIUM_MINE: uranium_mine,
            FARM: farm,
            OIL_REFINERY: oil_refinery,
            STEEL_MILL: steel_mill,
            ALUMINUM_REFINERY: aluminum_refinery,
            MUNITIONS_FACTORY: munitions_factory,
            POLICE_STATION: police_station,
            HOSPITAL: hospital,
            RECYCLING_CENTER: recycling_center,
            SUBWAY: subway,
            SUPERMARKET: supermarket,
            BANK: bank,
            SHOPPING_MALL: shopping_mall,
            STADIUM: stadium,
            BARRACKS: barracks,
            FACTORY: factory,
            AIR_FORCE_BASE: air_force_base,
            DRYDOCK: drydock
        }

    @property
    def nation(self):

        if self.nation_id and self.nation_id in self.game.nations:
            return self.game.alliances[self.nation_id]
        return None

    @property
    def powered(self):

        infra = (
                self.improvements[COAL_POWER] * 500 +
                self.improvements[OIL_POWER] * 500 +
                self.improvements[NUCLEAR_POWER] * 2000 +
                self.improvements[WIND_POWER] * 250
        )
        return infra >= self.infrastructure

    @property
    def base_population(self):

        return self.infrastructure * 100

    @property
    def population(self):

        pop = self.base_population
        pop -= max(0, self.crime/10 * self.base_population - 25)
        pop -= max(0, self.disease * self.infrastructure)
        pop *= 1 + self.age/3000
        return round(pop)

    @property
    def crime(self):

        crime = ((103 - self.commerce) ** 2 + self.base_population) / 111111
        if self.powered:
            crime -= self.improvements[POLICE_STATION] * 2.5
        return min(100, max(0, crime))

    @property
    def disease(self):

        disease = ((self.base_population / self.land) ** 2 * 0.01 - 25) / 100
        disease += self.base_population / 100000
        disease += self.pollution * 0.05
        if self.powered:
            disease -= self.improvements[HOSPITAL] * 2.5
        return min(100, max(0, disease))

    @property
    def commerce(self):

        if not self.powered:
            return 0
        return min(
            self.improvements[SUPERMARKET] * SUPERMARKET.commerce +
            self.improvements[BANK] * BANK.commerce +
            self.improvements[SHOPPING_MALL] * SHOPPING_MALL.commerce +
            self.improvements[STADIUM] * STADIUM.commerce +
            self.improvements[SUBWAY] * SUBWAY.commerce,
            115 if self.nation and INT_TRADE_CENTER in self.nation.projects else 100
        )

    @property
    def pollution(self):

        p = sum([
                i.pollution * self.improvements[i]
                if not i.power or (i.power and self.powered) else 0
                for i in self.improvements
        ])
        p += self.nuclear_pollution
        return max(0, p)

    def update(self, response, *args, **kwargs):

        if response.status_code != 200:
            return
        d = response.json()
        self.id = d['cityid']
        self.nation_id = d['nationid']
        self.name = d['name']
        self.age = d['age']
        self.infrastructure = float(d['infrastructure'])
        self.land = float(d['land'])
        self.nuclear_pollution = d['nuclearpollution']

        self.improvements = {
            COAL_POWER: int(d['imp_coalpower']),
            OIL_POWER: int(d['imp_oilpower']),
            NUCLEAR_POWER: int(d['imp_nuclearpower']),
            WIND_POWER: int(d['imp_windpower']),
            COAL_MINE: int(d['imp_coalmine']),
            OIL_WELL: int(d['imp_oilwell']),
            IRON_MINE: int(d['imp_ironmine']),
            BAUXITE_MINE: int(d['imp_bauxitemine']),
            LEAD_MINE: int(d['imp_leadmine']),
            URANIUM_MINE: int(d['imp_uraniummine']),
            FARM: int(d['imp_farm']),
            OIL_REFINERY: int(d['imp_oilrefinery']),
            STEEL_MILL: int(d['imp_steelmill']),
            ALUMINUM_REFINERY: int(d['imp_aluminumrefinery']),
            MUNITIONS_FACTORY: int(d['imp_munitionsfactory']),
            POLICE_STATION: int(d['imp_policestation']),
            HOSPITAL: int(d['imp_hospital']),
            RECYCLING_CENTER: int(d['imp_recyclingcenter']),
            SUBWAY: int(d['imp_subway']),
            SUPERMARKET: int(d['imp_supermarket']),
            BANK: int(d['imp_bank']),
            SHOPPING_MALL: int(d['imp_shoppingmall']),
            STADIUM: int(d['imp_stadium']),
            BARRACKS: int(d['imp_barracks']),
            FACTORY: int(d['imp_factory']),
            AIR_FORCE_BASE: int(d['imp_airforcebase']),
            DRYDOCK: int(d['imp_drydock'])
        }

    def fetch(self):

        return grequests.get(
            self.game.URL + 'city/id={}'.format(self.id),
            headers={'User-Agent': self.game.USER_AGENT},
            callback=self.update
        )

    def __repr__(self):

        return CITY_REPR.format(self)