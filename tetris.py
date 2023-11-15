import os
import time

# define the Tetris board size
WIGTH = 16
HEIGHT = 12
WALL_LEN = 3


def create_board():
    '''
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|]               [|]
    [|][|][|][|][|][|][|]
    '''
    row = list(f'[|]{" " * (WIGTH - 1)}[|]')
    bottom = list('[|][|][|][|][|][|][|]')

    board = []
    for i in range(HEIGHT):
        board.append(row)
    board.append(bottom)

    return board


def print_board(board):
    for r in board:
        print(*r, sep='')


def drop_piece(board, piece):
    for i in range(HEIGHT - 1):
        for j in range(5, WIGTH - WALL_LEN - 1):
            if board[i][j] == ' ':
                pass


def main():
    while True:
        os.system('cls')
        print_board(create_board())
        time.sleep(0.5)


if __name__ == '__main__':
    main()
