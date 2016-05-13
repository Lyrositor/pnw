class Improvement:

    def __init__(self, name, cost, upkeep, pollution=0, power=False):

        self.name = name
        self.cost = cost
        self.upkeep = upkeep
        self.pollution = pollution
        self.power = power

    def __repr__(self):

        return self.name


class CommerceImprovement(Improvement):

    def __init__(self, name, cost, upkeep, commerce, pollution=0):

        super().__init__(name, cost, upkeep, pollution, True)
        self.commerce = commerce


class MilitaryImprovement(Improvement):

    def __init__(self, name, cost, capacity):

        super().__init__(name, cost, {}, 0, True)
        self.capacity = capacity
