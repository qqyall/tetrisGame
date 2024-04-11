from tetris import Game


def main():
    while True:
        game = Game()
        game.runTetris()
        game.pauseScreen()
        game.showText('Игра закончена')
        del game


if __name__ == '__main__':
    main()
