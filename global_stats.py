import pnw.game

if __name__ == '__main__':

    game = pnw.game.Game()
    game.update_nation_list(fetch_nations=True, fetch_cities=True, max_rank=1, force=False)
    print(game.nations)