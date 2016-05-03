from datetime import datetime
import grequests
import requests

from .alliance import Alliance
from .data import *
from .nation import Nation


class Game:

    URL = 'https://politicsandwar.com/api/'
    USER_AGENT = 'PnWLib'

    def __init__(self):

        self.alliances = {}
        self.nations = {}
        self.prices = {}

    def update_alliance(self, i):

        if i not in self.alliances:
            self.prices[i] = Alliance(game=self, id=i)
        grequests.map(self.alliances[i].fetch())

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
            founded = datetime.strptime(d['founddate'], "%Y-%m-%d %H:%M:%S")
            fetch = force
            if i not in self.alliances:
                self.alliances[i] = Alliance(
                    game=self, id=i, name=a['name'], acronym=a['acronym'],
                    color=COLORS[a['color']], founded=founded,
                    flag=a['flagurl'], forum=a['forumurl'], irc=a['ircchan'],
                    continent=CONTINENTS[a['continent']],
                    officer_ids=[int(i) for i in d['officerids']],
                    leader_ids=[int(i) for i in d['leaderids']],
                    heir_ids=[int(i) for i in d['heirids']]
                )
                fetch = True
            if fetch_alliances and fetch:
                api_requests.append(self.alliances[i].fetch())

        grequests.map(api_requests)

    def update_nation(self, i, fetch_cities=False):

        if i not in self.nations:
            self.nations[i] = Nation(game=self, id=i)
        grequests.map(self.nations[i].fetch())

        api_requests = []
        if fetch_cities:
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

        pass