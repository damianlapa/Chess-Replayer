alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')


class ChessBoard:
    def __init__(self, pieces=None):
        # creating fields
        for y in range(1, 9)[::-1]:
            line = ''
            for x in range(0, 8):
                field_nr = 8 * (y - 1) + x + 1
                if not pieces:
                    line += '{}{} '.format(alphabet[x], str(y))

                else:
                    field_piece = None
                    for piece in pieces:
                        if piece.position == field_nr:
                            field_piece = piece
                    if not field_piece:
                        line += '{}{} '.format(alphabet[x], str(y))
                    else:
                        line += '{} '.format(field_piece.shortcut)

                if x == 7:
                    print(line)


class ChessPiece:
    def __init__(self, name, shortcut, position=None, color='white'):
        self.name = name
        self.shortcut = shortcut
        self.color = color
        self.position = position

    def __str__(self):
        return self.shortcut

    def new_position(self, new_position):
        self.position = new_position


class NewGame:
    def __init__(self):
        self.pieces = []
        self.set_all_pieces()
        self.board = ChessBoard(self.pieces)

    def set_all_pieces(self):
        for i in range(0, 8):
            piece = ChessPiece('white_pawn', f'wP{alphabet[i]}', 9 + i)
            self.pieces.append(piece)
        for i in range(0, 8):
            piece = ChessPiece('black_pawn', f'bP{alphabet[i]}', 49 + i, 'black')
            self.pieces.append(piece)
        for i in range(0, 2):
            piece = ChessPiece('white_rook', 'wR', 1 + i * 7)
            black_piece = ChessPiece('black_rook', 'bR', 57 + i * 7)
            self.pieces.append(piece)
            self.pieces.append(black_piece)


ng = NewGame()
