from datetime import datetime
import grequests

from .data import *


class Alliance:

    def __init__(
            self, game, id, name="", acronym="", color=BEIGE, accepting=True,
            flag="", founded=datetime.now(), forum="", irc="", treasures=0,
            continent=NORTH_AMERICA, officer_ids=None, leader_ids=None,
            heir_ids=None
    ):

        self.game = game

        self.id = id
        self.name = name
        self.acronym = acronym
        self.color = color
        self.accepting = accepting
        self.flag = flag
        self.founded = founded
        self.forum = forum
        self.irc = irc
        self.treasures = treasures
        self.continent = continent
        self.officer_ids = officer_ids if officer_ids else []
        self.leader_ids = leader_ids if leader_ids else []
        self.heir_ids = heir_ids if heir_ids else []

    @property
    def members(self):

        members = []
        for nation_id, nation in self.game.nations.items():
            if self.id == nation.alliance_id:
                members.append(self.game.nations)
        return members

    @property
    def score(self):

        score = 0.0
        for member in self.members:
            score += member.score if not member.vacation_mode else 0
        return score

    @property
    def gdp(self):

        gdp = 0.0
        for member in self.members:
            gdp += member.gdp if not member.vacation_mode else 0
        return gdp

    @property
    def soldiers(self):

        soldiers = 0
        for member in self.members:
            soldiers += member.soldiers if not member.vacation_mode else 0
        return soldiers

    @property
    def tanks(self):

        tanks = 0
        for member in self.members:
            tanks += member.tanks if not member.vacation_mode else 0
        return tanks

    @property
    def aircraft(self):

        aircraft = 0
        for member in self.members:
            aircraft += member.aircraft if not member.vacation_mode else 0
        return aircraft

    @property
    def ships(self):

        ships = 0
        for member in self.members:
            ships += member.ships if not member.vacation_mode else 0
        return ships

    @property
    def missiles(self):

        missiles = 0
        for member in self.members:
            missiles += member.missiles if not member.vacation_mode else 0
        return missiles

    @property
    def nukes(self):

        nukes = 0
        for member in self.members:
            nukes += member.nukes if not member.vacation_mode else 0
        return nukes

    @property
    def leaders(self):

        leaders = []
        for leader_id in self.leader_ids:
            leaders.append(self.game.nations[leader_id])
        return leaders

    def update(self, response, *args, **kwargs):

        if response.status_code != 200:
            return
        d = response.json()

        self.id = d['allianceid']
        self.name = d['name']
        self.acronym = d['acronym']
        self.color = COLORS[d['color']]
        self.accepting = bool(int(d['accepting']))
        self.flag = d['flagurl']
        self.forum = d['forumurl']
        self.irc = d['irc']
        self.leader_ids = [int(i) for i in d['leaderids']]

    def fetch(self):

        return grequests.get(
            self.game.URL + 'alliance/id={}'.format(self.id),
            headers={'User-Agent': self.game.USER_AGENT},
            callback=self.update
        )

    def __repr__(self):

        return "Alliance(" + \
               ")"