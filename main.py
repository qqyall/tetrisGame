from tetris import Game


def main():
    while True:
        game = Game()
        game.runTetris()
        game.pauseScreen()
        game.endGameScreen()
        del game


if __name__ == '__main__':
    main()
