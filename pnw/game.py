from datetime import datetime
import grequests
import requests

from .alliance import Alliance
from .data import *
from .nation import Nation


class Game:
    """
    Represents the current state of the game, as determined using the API.

    Attributes
    ----------
    alliances : dict
    nations : dict
    prices : dict
    season : int
    """

    """The URL for the Politics & War API."""
    URL = 'https://politicsandwar.com/api/'

    """The User-Agent to use while browsing the API."""
    USER_AGENT = 'PnWLib'

    def __init__(self, season=SUMMER):
        """
        Initializes a game to a default, empty state.

        The current season must be manually specified, as it cannot be
        determined from the API. This is the season that will be used for
        northern hemisphere nations; southern hemisphere nations will use the
        opposite season.

        Parameters
        ----------
        season : int, optional
            The current in-game season, for the northern hemisphere.
        """

        self.alliances = {}
        self.nations = {}
        self.prices = {
            FOOD: [0, 0, 0],
            COAL: [0, 0, 0],
            OIL: [0, 0, 0],
            URANIUM: [0, 0, 0],
            IRON: [0, 0, 0],
            BAUXITE: [0, 0, 0],
            LEAD: [0, 0, 0],
            GASOLINE: [0, 0, 0],
            STEEL: [0, 0, 0],
            ALUMINUM: [0, 0, 0],
            MUNITIONS: [0, 0, 0]
        }
        self.season = season

    def get_season(self, continent):
        """
        Calculates the current season for a country on the specified continent.

        Returns
        -------
        """

        return self.season * (1 if continent in (NORTH_AMERICA, EUROPE, ASIA) else -1)

    def update_alliance(self, i):

        if i not in self.alliances:
            self.prices[i] = Alliance(game=self, id=i)
        grequests.map([self.alliances[i].fetch()])

    def update_alliance_list(
            self, fetch_alliances=True, max_rank=None, force=False
    ):

        api_requests = []

        response = requests.get(
            self.URL + 'alliances/',
            headers={'User-Agent': self.USER_AGENT}
        )
        if response.status_code != 200:
            return
        d = response.json()['alliances']

        for a in d[:max_rank]:
            i = int(a['id'])
            founded = datetime.strptime(a['founddate'], "%Y-%m-%d %H:%M:%S")
            fetch = force
            if i not in self.alliances:
                self.alliances[i] = Alliance(
                    game=self, id=i, name=a['name'], acronym=a['acronym'],
                    color=COLORS[a['color']], founded=founded,
                    flag=a['flagurl'], forum=a['forumurl'], irc=a['ircchan'],
                    continent=CONTINENTS[a['continent']]
                )
                if 'leaderids' in a:
                    self.alliances[i].leader_ids = [
                        int(i) for i in a['leaderids']
                    ]
                if 'officerids' in a:
                    self.alliances[i].officer_ids = [
                        int(i) for i in a['officerids']
                    ]
                if 'heirids' in a:
                    self.alliances[i].heir_ids = [int(i) for i in a['heirids']]
                fetch = True
            if fetch_alliances and fetch:
                api_requests.append(self.alliances[i].fetch())

        grequests.map(api_requests)

    def update_nation(self, i, fetch_cities=False):

        if i not in self.nations:
            self.nations[i] = Nation(game=self, id=i)
        grequests.map([self.nations[i].fetch()])

        if fetch_cities:
            api_requests = []
            for city in self.nations[i].cities:
                api_requests.append(city.fetch())
            grequests.map(api_requests)

    def update_nations(self, i_list, fetch_cities=False):

        api_requests = []
        for i in i_list:
            if i not in self.nations:
                self.nations[i] = Nation(game=self, id=i)
            api_requests.append(self.nations[i].fetch())
        grequests.map(api_requests)

        if fetch_cities:
            api_requests = []
            for i in i_list:
                for city in self.nations[i].cities:
                    api_requests.append(city.fetch())
            grequests.map(api_requests)

    def update_nation_list(
            self, fetch_nations=False, fetch_cities=False, max_rank=None,
            from_alliance=None, force=False
    ):

        api_requests = []

        response = requests.get(
            self.URL + 'nations/',
            headers={'User-Agent': self.USER_AGENT}
        )
        if response.status_code != 200:
            return
        d = response.json()['nations']

        for n in d[:max_rank]:
            if from_alliance is not None and \
                    int(n['allianceid']) != from_alliance:
                continue

            i = int(n['nationid'])
            fetch = force
            if i not in self.nations:
                self.nations[i] = Nation(
                    game=self, id=i, name=n['nation'], leader=n['leader'],
                    continent=CONTINENTS[n['continent']],
                    alliance_id=int(n['allianceid']),
                    war_policy=WAR_POLICIES[n['war_policy']],
                    color=COLORS[n['color']],
                    vacation_mode=bool(int(n['vacmode']))
                )
                fetch = True
            nation = self.nations[i]
            if fetch_nations and fetch:
                api_requests.append(nation.fetch())

        grequests.map(api_requests)

        api_requests = []
        if fetch_cities:
            for nation_id, nation in self.nations.items():
                for city in nation.cities:
                    api_requests.append(city.fetch())
        grequests.map(api_requests)

    def update_prices(self):

        def r(n):
            return grequests.get(
                self.URL + 'tradeprice/resource={}'.format(n),
                headers={'User-Agent': self.USER_AGENT}
            )

        api_requests = (
            r('food'), r('coal'), r('oil'), r('uranium'),
            r('iron'), r('bauxite'), r('lead'), r('gasoline'), r('steel'),
            r('aluminum'), r('munitions')
        )
        responses = grequests.map(api_requests)

        def p(d):
            return (int(d['highestbuy']['price']), int(d['avgprice']),
                    int(d['lowestbuy']['price']))

        self.prices = {
            FOOD: p(responses[0].json()),
            COAL: p(responses[1].json()),
            OIL: p(responses[2].json()),
            URANIUM: p(responses[3].json()),
            IRON: p(responses[4].json()),
            BAUXITE: p(responses[5].json()),
            LEAD: p(responses[6].json()),
            GASOLINE: p(responses[7].json()),
            STEEL: p(responses[8].json()),
            ALUMINUM: p(responses[9].json()),
            MUNITIONS: p(responses[10].json())
        }