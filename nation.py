from pnw.data import *
import pnw.game

ID = 0
SPIES = 0
TAX = 0.00

game = pnw.game.Game(SPRING)
game.update_prices()
game.update_alliance_list(False)
game.update_nation(ID, True)
nation = game.nations[ID]
nation.spies = SPIES
game.update_alliance(nation.alliance_id)
game.alliances[nation.alliance_id].revenue_tax = TAX

print(nation)