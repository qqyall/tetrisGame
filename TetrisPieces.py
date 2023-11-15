class Pieces:
    def __init__(self):
        self.form = []

    pieces = [
        [
            list('  []  '),
            list('  []  '),
            list('  []  ')
        ],
        [
            list('  []  '),
            list('[][]  '),
            list('      ')
        ],
        [
            list('  [][]'),
            list('[][]  '),
            list('      ')
        ],
        [
            list('  []  ')
        ]
    ]

    def rotate_piece():
        pass

    def print_piece(self):
        print('-' * 6)
        for row in self.form:
            print(*row)
        print('-' * 6, end='\n')


class StickPiece(Pieces):
    def __init__(self) -> None:
        self.form = [
            list('  []  '),
            list('  []  '),
            list('  []  ')
        ]

    def rotate(self):
        new_form = [[[''] * 6] * 3]
        for i in range(len(self.form)):
            for j in range(len(self.form[i])):
                new_form[i][j] = self.form[j][i]
        self.form = new_form.copy()


class AnglePiece(Pieces):
    def __init__(self) -> None:
        self.form = [
            list('  []  '),
            list('[][]  '),
            list('      ')
        ]
        self.pos = 0

        self.rotates = [
            [
                list('  []  '),
                list('[][]  '),
                list('      ')
            ],
            [
                list('  []  '),
                list('  [][]'),
                list('      ')
            ],
            [
                list('      '),
                list('  [][]'),
                list('  []  ')
            ],
            [
                list('      '),
                list('[][]  '),
                list('  []  ')
            ]
        ]

    def rotate_piece(self, direction):
        if direction == 'r':
            self.pos = (self.pos + 1) % len(self.rotates)
        else:
            self.pos = self.pos - 1 % len(self.rotates)
        self.form = self.rotates[self.pos]


p1 = AnglePiece()
p1.print_piece()
p1.rotate_piece(direction='l')
p1.print_piece()
p1.rotate_piece(direction='l')
p1.print_piece()
p1.rotate_piece(direction='l')
p1.print_piece()
p1.rotate_piece(direction='l')
p1.print_piece()
