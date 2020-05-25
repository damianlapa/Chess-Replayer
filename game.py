import re

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
                    pass
                    # print(line)


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
    def __init__(self, game_description):
        self.pieces = []
        self.game_description = game_description
        self.set_all_pieces()
        self.board = ChessBoard(self.pieces)
        self.game_moves = []

    def set_all_pieces(self):
        for i in range(0, 8):
            piece = ChessPiece('white_pawn', f'wP{alphabet[i]}', 9 + i)
            self.pieces.append(piece)
        for i in range(0, 8):
            piece = ChessPiece('black_pawn', f'bP{alphabet[i]}', 49 + i, 'black')
            self.pieces.append(piece)
        for i in range(0, 2):
            piece = ChessPiece('white_rook', 'wR', 1 + i * 7)
            black_piece = ChessPiece('black_rook', 'bR', 57 + i * 7, 'black')
            self.pieces.append(piece)
            self.pieces.append(black_piece)
        for i in range(0, 2):
            piece = ChessPiece('white_knight', 'wN', 2 + i * 5)
            black_piece = ChessPiece('black_knight', 'bN', 58 + i * 5, 'black')
            self.pieces.append(piece)
            self.pieces.append(black_piece)
        for i in range(0, 2):
            piece = ChessPiece('white_bishop', 'wB', 3 + i * 3)
            black_piece = ChessPiece('black_bishop', 'bB', 59 + i * 3, 'black')
            self.pieces.append(piece)
            self.pieces.append(black_piece)
        white_queen = ChessPiece('white_king', 'wK', 5)
        white_king = ChessPiece('white_queen', 'wQ', 4)
        black_queen = ChessPiece('black_king', 'bK', 61, 'black')
        black_king = ChessPiece('black_queen', 'bQ', 60, 'black')
        self.pieces.append(white_queen)
        self.pieces.append(white_king)
        self.pieces.append(black_king)
        self.pieces.append(black_queen)

    # TO DO

    # reading moves history
    def reading_game_history(self):
        self.game_moves = []
        steps = re.split(r'\d+\.', self.game_description)
        for step in steps:
            for move in step.split():
                self.game_moves.append(move)
    # separating steps
    # code moves for every text in moves history

    def game_moves_all(self):
        # black or white moves
        for i in range(0, len(self.game_moves)):
            if i % 2 == 0:
                color = 'white'
            else:
                color = 'black'
            # pawn move
            if re.fullmatch(r'[a-z]\d', self.game_moves[i]):
                print('{} pawn move [{}]({})'.format(color, self.game_moves[i], i))
            # rook move
            if re.fullmatch(r'R[a-z]\d', self.game_moves[i]):
                print('{} rook move [{}]({})'.format(color, self.game_moves[i], i))
            # knight move
            if re.fullmatch(r'N[a-z]\d', self.game_moves[i]):
                print('{} knight move [{}]({})'.format(color, self.game_moves[i], i))
            # bishop move
            if re.fullmatch(r'B[a-z]\d', self.game_moves[i]):
                print('{} bishop move [{}]({})'.format(color, self.game_moves[i], i))
            # queen move
            if re.fullmatch(r'Q[a-z]\d', self.game_moves[i]):
                print('{} queen move [{}]({})'.format(color, self.game_moves[i], i))
            # king move
            if re.fullmatch(r'K[a-z]\d', self.game_moves[i]):
                print('{} king move [{}]({})'.format(color, self.game_moves[i], i))
            if self.game_moves[i] == 'O-O':
                print('{} short castle [{}]({})'.format(color, self.game_moves[i], i))
            if self.game_moves[i] == 'O-O-O':
                print('{} long castle [{}]({})'.format(color, self.game_moves[i], i))
            if re.fullmatch(r'[a-z|A-Z]x[a-z]\d', self.game_moves[i]):
                print('{} XXX [{}]({})'.format(color, self.game_moves[i], i))
            if re.fullmatch(r'[a-z|A-Z][abcdefgh][a-z]\d', self.game_moves[i]):
                print('{} two possible figures [{}]({})'.format(color, self.game_moves[i], i))
            if re.fullmatch(r'[a-z|A-Z][abcdefgh]x[a-z]\d', self.game_moves[i]):
                print('{} two possible figures XXX [{}]({})'.format(color, self.game_moves[i], i))

game_text = '''
1. c4 e6 2. Nf3 d5 3. d4 Nf6 4. Nc3 Be7 5. Bg5 O-O 6. e3 h6
7. Bh4 b6 8. cxd5 Nxd5 9. Bxe7 Qxe7 10. Nxd5 exd5 11. Rc1 Be6
12. Qa4 c5 13. Qa3 Rc8 14. Bb5 a6 15. dxc5 bxc5 16. O-O Ra7
17. Be2 Nd7 18. Nd4 Qf8 19. Nxe6 fxe6 20. e4 d4 21. f4 Qe7
22. e5 Rb8 23. Bc4 Kh8 24. Qh3 Nf8 25. b3 a5 26. f5 exf5
27. Rxf5 Nh7 28. Rcf1 Qd8 29. Qg3 Re7 30. h4 Rbb7 31. e6 Rbc7
32. Qe5 Qe8 33. a4 Qd8 34. R1f2 Qe8 35. R2f3 Qd8 36. Bd3 Qe8
37. Qe4 Nf6 38. Rxf6 gxf6 39. Rxf6 Kg8 40. Bc4 Kh8 41. Qf4 1-0
'''

ng = NewGame(game_text)
ng.reading_game_history()
ng.game_moves_all()



