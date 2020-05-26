import re

alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')


class ChessBoard:
    def __init__(self, pieces=None):
        # creating fields
        for y in range(1, 9)[::-1]:
            for x in range(0, 8):
                field_nr = 8 * (y - 1) + x + 1
        self.border_fields = ()


class ChessPiece:
    def __init__(self, piece_type, position=None, color='white'):
        self.piece_type = piece_type
        self.color = color
        self.position = position
        self.possible_moves = []
        self.border_fields = ()

    def __str__(self):
        return self.color + self.piece_type

    def chessboard_border_fields(self):
        fields_south = []
        fields_north = []
        fields_east = []
        fields_west = []
        i = 1
        while i < 9:
            fields_south.append(i)
            fields_north.append(56 + i)
            fields_west.append(1 + (i - 1) * 8)
            fields_east.append(8 + (i - 1) * 8)
            i += 1
        self.border_fields = tuple(set(fields_east + fields_south + fields_west + fields_north))
        return self.border_fields

    def new_position(self, new_position):
        self.position = new_position

    def finding_possible_moves(self):
        # pawn move
        if self.piece_type == 'pawn':
            if self.color == 'white':
                if self.position in range(9, 17):
                    for i in range(1, 3):
                        self.possible_moves.append(self.position + 8 * i)
                else:
                    self.possible_moves.append(self.position + 8)
            else:
                if self.position in range(49, 57):
                    for i in range(1, 3):
                        self.possible_moves.append(self.position - 8 * i)
                else:
                    self.possible_moves.append(self.position - 8)

            return self.possible_moves
        # knight move
        elif self.piece_type == 'knight':
            # decode field number to chess board field
            column = self.position % 8
            row = self.position // 8
            if column == 0:
                row = row - 1
            # possible knight moves
            # west moves
            if self.position % 8 not in (0, 7):
                move_1 = self.position + 2 + 8
                move_2 = self.position + 2 - 8
                if 0 < move_1 < 65:
                    self.possible_moves.append(move_1)
                if 0 < move_2 < 65:
                    self.possible_moves.append(move_2)

            # east moves
            if self.position % 8 not in (1, 2):
                move_1 = self.position - 2 + 8
                move_2 = self.position - 2 - 8
                if 0 < move_1 < 65:
                    self.possible_moves.append(move_1)
                if 0 < move_2 < 65:
                    self.possible_moves.append(move_2)

            # north moves + south_moves
            if self.position % 8 != 0:
                row_ = (self.position // 8) + 1
            else:
                row_ = self.position // 8

            # north moves
            if row_ not in (7, 8):
                move_1 = self.position + 16 + 1
                move_2 = self.position + 16 - 1
                if 0 < move_1 < 65:
                    if self.position % 8 != 0:
                        self.possible_moves.append(move_1)
                if 0 < move_2 < 65:
                    if self.position % 8 != 1:
                        self.possible_moves.append(move_2)

            # south moves
            if row_ not in (1, 2):
                move_1 = self.position - 16 + 1
                move_2 = self.position - 16 - 1
                if 0 < move_1 < 65:
                    if self.position % 8 != 0:
                        self.possible_moves.append(move_1)
                if 0 < move_2 < 65:
                    if self.position % 8 != 1:
                        self.possible_moves.append(move_2)

            return '{}{}//{}'.format(alphabet[column - 1], row + 1, self.possible_moves)
        # bishop move
        elif self.piece_type == 'bishop':
            # moves to left
            current_position = self.position
            i = 1
            if self.position % 8 != 1:
                while True:
                    move_1 = current_position + 7 * i
                    move_2 = current_position - 9 * i
                    i += 1
                    if 0 < move_1 < 65:
                        self.possible_moves.append(move_1)
                    if 0 < move_2 < 65:
                        self.possible_moves.append(move_2)
                    if alphabet[(move_1 % 8) - 1] == 'a':
                        break
            # moves to right
            i = 1
            if self.position % 8 != 0:
                while True:
                    move_1 = current_position + 9 * i
                    move_2 = current_position - 7 * i
                    i += 1
                    if 0 < move_1 < 65:
                        self.possible_moves.append(move_1)
                    if 0 < move_2 < 65:
                        self.possible_moves.append(move_2)
                    if alphabet[(move_1 % 8) - 1] == 'h':
                        break

            return self.possible_moves

        # rook move
        elif self.piece_type == 'rook':
            y = self.position % 8
            x = self.position // 8
            for i in range(0, 8):
                # vertical moves
                if y != 0:
                    move_1 = y + i * 8
                else:
                    move_1 = (i + 1) * 8
                # horizontal moves
                move_2 = x * 8 + i + 1
                if move_1 != self.position:
                    self.possible_moves.append(move_1)
                if move_2 != self.position:
                    self.possible_moves.append(move_2)

            return self.possible_moves
        # queen move
        # king move
        pass


class NewGame:
    def __init__(self, game_description):
        self.pieces = []
        self.game_description = game_description
        self.set_all_pieces()
        self.board = ChessBoard(self.pieces)
        self.game_moves = []

    def set_all_pieces(self):
        for i in range(0, 8):
            pawn = ChessPiece('pawn', 9 + i)
            self.pieces.append(pawn)
            black_pawn = ChessPiece('pawn', 49 + i, 'black')
            self.pieces.append(black_pawn)
        for i in range(0, 2):
            piece = ChessPiece('rook', 1 + i * 7)
            black_piece = ChessPiece('rook', 57 + i * 7, 'black')
            self.pieces.append(piece)
            self.pieces.append(black_piece)
        for i in range(0, 2):
            piece = ChessPiece('knight', 2 + i * 5)
            black_piece = ChessPiece('knight', 58 + i * 5, 'black')
            self.pieces.append(piece)
            self.pieces.append(black_piece)
        for i in range(0, 2):
            piece = ChessPiece('bishop', 3 + i * 3)
            black_piece = ChessPiece('bishop', 59 + i * 3, 'black')
            self.pieces.append(piece)
            self.pieces.append(black_piece)
        white_queen = ChessPiece('king', 5)
        white_king = ChessPiece('queen', 4)
        black_queen = ChessPiece('king', 61, 'black')
        black_king = ChessPiece('queen', 60, 'black')
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

    def pawn_move(self):
        pass
        move1 = 'c4'
        move2 = 'd7'
        i = 1
        # finding piece color
        if i % 2 == 0:
            color = 'white'
        else:
            color = 'black'
        # finding piece which was moved
        # finding actual place
        field_nr = int(alphabet.index(move1[0]) * 8) + int(move1[1])
        print(field_nr)
        # place beneath and above actual field
        border = field_nr
        for i in range(1, 65):
            # finding possible white pawns
            if i <= field_nr:
                color = 'white'
            else:
                color = 'black'
            if i % 8 == field_nr % 8:
                for piece in self.pieces:
                    if piece.name == 'white_pawn':
                        if piece.position == i:
                            print(piece)


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

new_piece = ChessPiece('rook', , 'black')
print(new_piece.finding_possible_moves())
