import grequests


class City:

    def __init__(
            self, game, id, nation_id, age=0, infrastructure=0.0, land=0.0,
            nuclear_pollution=0, coal_power=0, oil_power=0, nuclear_power=0,
            wind_power=0, coal_mine=0, oil_well=0, iron_mine=0, bauxite_mine=0,
            leadmine=0, uranium_mine=0, farm=0, oil_refinery=0, steel_mill=0,
            aluminum_refinery=0, munitions_factory=0, police_station=0,
            hospital=0, recycling_center=0, subway=0, supermarket=0, bank=0,
            shopping_mall=0, stadium=0, barracks=0, factory=0, air_force_base=0,
            dry_dock=0
    ):

        self.game = game

        self.id = id
        self.nation_id = nation_id
        self.age = age
        self.infrastructure = infrastructure
        self.land = land
        self.nuclear_pollution = nuclear_pollution

        self.coal_power = coal_power
        self.oil_power = oil_power
        self.nuclear_power = nuclear_power
        self.wind_power = wind_power
        self.coal_mine = coal_mine
        self.oil_well = oil_well
        self.iron_mine = iron_mine
        self.bauxite_mine = bauxite_mine
        self.leadmine = leadmine
        self.uranium_mine = uranium_mine
        self.farm = farm
        self.oil_refinery = oil_refinery
        self.steel_mill = steel_mill
        self.aluminum_refinery = aluminum_refinery
        self.munitions_factory = munitions_factory
        self.police_station = police_station
        self.hospital = hospital
        self.recycling_center = recycling_center
        self.subway = subway
        self.supermarket = supermarket
        self.bank = bank
        self.shopping_mall = shopping_mall
        self.stadium = stadium
        self.barracks = barracks
        self.factory = factory
        self.air_force_base = air_force_base
        self.dry_dock = dry_dock

    @property
    def powered(self):

        return True

    @property
    def population(self):

        return 0

    @property
    def crime(self):

        return 0.0

    @property
    def disease(self):

        return 0.0

    @property
    def commerce(self):

        return 0.0

    @property
    def average_income(self):

        return 0.0

    @property
    def pollution(self):

        return 0

    def update(self, response, *args, **kwargs):

        if response.status_code != 200:
            return
        d = response.json()

        self.id = d['cityid']
        self.nation_id = d['nationid']
        self.age = d['age']
        self.infrastructure = float(d['infrastructure'])
        self.land = float(d['land'])
        self.nuclear_pollution = d['nuclearpollution']

        self.coal_power = d['coalpower']
        self.oil_power = d['oilpower']
        self.nuclear_power = d['nuclearpower']
        self.wind_power = d['windpower']
        self.coal_mine = d['coalmine']
        self.oil_well = d['oilwell']
        self.iron_mine = d['ironmine']
        self.bauxite_mine = d['bauxitemine']
        self.leadmine = d['leadmine']
        self.uranium_mine = d['uraniummine']
        self.farm = d['farm']
        self.oil_refinery = d['oilrefinery']
        self.steel_mill = d['steelmill']
        self.aluminum_refinery = d['aluminumrefinery']
        self.munitions_factory = d['munitionsfactory']
        self.police_station = d['policestation']
        self.hospital = d['hospital']
        self.recycling_center = d['recyclingcenter']
        self.subway = d['subway']
        self.supermarket = d['supermarket']
        self.bank = d['bank']
        self.shopping_mall = d['shoppingmall']
        self.stadium = d['stadium']
        self.barracks = d['barracks']
        self.factory = d['factory']
        self.air_force_base = d['airforcebase']
        self.dry_dock = d['drydock']

    def fetch(self):

        return grequests.get(
            self.game.URL + 'city/id={}'.format(self.id),
            headers={'User-Agent': self.game.USER_AGENT},
            callback=self.update
        )

    def __repr__(self):
        return "City(" + \
               ")"