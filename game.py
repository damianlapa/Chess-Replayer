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
        self.finding_possible_moves()

    def __str__(self):
        return self.color + self.piece_type + self.piece_notation_position()

    def piece_notation_position(self):
        text = ''
        if self.position % 8 != 0:
            text += alphabet[self.position % 8 - 1]
            text += str(self.position // 8 + 1)
        else:
            text += alphabet[7]
            text += str(self.position // 8)
        return text

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
        self.possible_moves = self.finding_possible_moves()

    def finding_possible_moves(self):
        self.possible_moves = []
        # pawn move
        if self.piece_type == 'pawn':
            if self.color == 'white':
                if self.position in range(9, 17):
                    self.possible_moves.append(self.position + 9)
                    self.possible_moves.append(self.position + 7)
                    for j in range(1, 3):
                        self.possible_moves.append(self.position + 8 * j)
                else:
                    self.possible_moves.append(self.position + 8)
                    self.possible_moves.append(self.position + 7)
                    self.possible_moves.append(self.position + 9)
            else:
                if self.position in range(49, 57):
                    self.possible_moves.append(self.position - 9)
                    self.possible_moves.append(self.position - 7)
                    for j in range(1, 3):
                        self.possible_moves.append(self.position - 8 * j)
                else:
                    self.possible_moves.append(self.position - 8)
                    self.possible_moves.append(self.position - 7)
                    self.possible_moves.append(self.position - 9)

            return self.possible_moves
        # pawn capture

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

            return self.possible_moves

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
                    move_2 = x * 8 + i + 1
                else:
                    move_1 = (i + 1) * 8
                    move_2 = (x - 1) * 8 + i + 1

                if move_1 != self.position:
                    self.possible_moves.append(move_1)
                if move_2 != self.position:
                    self.possible_moves.append(move_2)

            return sorted(self.possible_moves)
        # queen move
        elif self.piece_type == 'queen':
            bishop_moves = ChessPiece('bishop', self.position).finding_possible_moves()
            rook_moves = ChessPiece('rook', self.position).finding_possible_moves()
            self.possible_moves = bishop_moves + rook_moves
            return self.possible_moves
        # king move
        elif self.piece_type == 'king':
            # up moves
            if not 56 < self.position < 65:
                move_1 = self.position + 8
                self.possible_moves.append(move_1)
                if not self.position % 8 == 1:
                    move_2 = self.position + 7
                    self.possible_moves.append(move_2)
                if not self.position == 0:
                    move_3 = self.position + 9
                    self.possible_moves.append(move_3)
            # left moves
            if not self.position % 8 == 1:
                move_1 = self.position - 1
                self.possible_moves.append(move_1)
                if self.position < 57:
                    move_2 = self.position + 7
                    self.possible_moves.append(move_2)
                if self.position > 8:
                    move_3 = self.position - 9
                    self.possible_moves.append(move_3)
            # down moves
            if not 0 < self.position < 9:
                move_1 = self.position - 8
                self.possible_moves.append(move_1)
                if not self.position % 8 == 1:
                    move_2 = self.position - 9
                    self.possible_moves.append(move_2)
                if not self.position % 8 == 0:
                    move_3 = self.position - 7
                    self.possible_moves.append(move_3)
            # right moves
            if not self.position % 8 == 0:
                move_1 = self.position + 1
                self.possible_moves.append(move_1)
                if self.position < 57:
                    move_2 = self.position + 9
                    self.possible_moves.append(move_2)
                if self.position > 8:
                    move_3 = self.position - 7
                    self.possible_moves.append(move_3)

            return list(set(self.possible_moves))


class NewGame:
    def __init__(self, game_description):
        self.pieces = []
        self.game_description = game_description
        self.set_all_pieces()
        self.board = ChessBoard(self.pieces)
        self.game_moves = []
        self.reading_game_history()

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

    def rook_blocked_lines(self, rook):
        rook.possible_moves = []
        rook.finding_possible_moves()
        self.pieces.remove(rook)
        blocked_horizontal_line_east = False
        blocked_horizontal_line_west = False
        blocked_vertical_line_north = False
        blocked_vertical_line_south = False
        blocked_horizontal_line_east_by_opponent_piece = False
        blocked_horizontal_line_west_by_opponent_piece = False
        blocked_vertical_line_north_by_opponent_piece = False
        blocked_vertical_line_south_by_opponent_piece = False
        for x in range(1, 8):
            move_right = rook.position + x
            move_left = rook.position - x
            move_up = rook.position + (x * 8)
            move_down = rook.position - (x * 8)
            for piece_ in self.pieces:
                if piece_.position == move_right:
                    if piece_.color == rook.color:
                        blocked_horizontal_line_east = True
                    else:
                        blocked_horizontal_line_east_by_opponent_piece = True
                if piece_.position == move_left:
                    if piece_.color == rook.color:
                        blocked_horizontal_line_west = True
                    else:
                        blocked_horizontal_line_west_by_opponent_piece = True
                if piece_.position == move_down:
                    if piece_.color == rook.color:
                        blocked_vertical_line_south = True
                    else:
                        blocked_vertical_line_south_by_opponent_piece = True
                if piece_.position == move_up:
                    if piece_.color == rook.color:
                        blocked_vertical_line_north = True
                    else:
                        blocked_vertical_line_north_by_opponent_piece = True
            if blocked_horizontal_line_east:
                if move_right in rook.possible_moves:
                    rook.possible_moves.remove(move_right)
            if blocked_horizontal_line_west:
                if move_left in rook.possible_moves:
                    rook.possible_moves.remove(move_left)
            if blocked_vertical_line_north:
                if move_up in rook.possible_moves:
                    rook.possible_moves.remove(move_up)
            if blocked_vertical_line_south:
                if move_down in rook.possible_moves:
                    rook.possible_moves.remove(move_down)
            if blocked_horizontal_line_east_by_opponent_piece:
                blocked_horizontal_line_east = True
            if blocked_horizontal_line_west_by_opponent_piece:
                blocked_horizontal_line_west = True
            if blocked_vertical_line_south_by_opponent_piece:
                blocked_vertical_line_south = True
            if blocked_vertical_line_north_by_opponent_piece:
                blocked_vertical_line_north = True
        self.pieces.append(rook)
        return rook.possible_moves

    # capturing a piece
    def piece_capture(self, position, final_position):
        piece_type = None
        piece_color = None
        captured_piece = None
        capturing_piece = None
        for piece in self.pieces:
            if piece.position == position:
                piece_type = piece.piece_type
                piece_color = piece.color
                capturing_piece = piece
            elif piece.position == final_position:
                captured_piece = piece
            if None not in (capturing_piece, captured_piece):
                break
        if None in (capturing_piece, captured_piece):
            raise NameError('brak elemetu')
        self.pieces.remove(captured_piece)
        self.pieces.remove(capturing_piece)
        moved_capturing_piece = ChessPiece(piece_type, final_position, piece_color)
        self.pieces.append(moved_capturing_piece)

    # reading moves history
    def reading_game_history(self):
        steps = re.split(r'\d+\.', self.game_description)
        for step in steps:
            for move in step.split():
                self.game_moves.append(move)

    def move_types(self, move):
        move_type = None
        # game result
        if re.fullmatch(r'1-0|0-1|1/2-1/2', move):
            move_type = 'game finished'
        # pawn move
        if re.fullmatch(r'[abcdefgh]\d[+]?[#]?', move):
            move_type = 'pawn'
        # rook move
        if re.fullmatch(r'R[a-z]\d[+]?[#]?', move):
            move_type = 'rook'
        # knight move
        if re.fullmatch(r'N[a-z]\d[+]?[#]?', move):
            move_type = 'knight'
        # bishop move
        if re.fullmatch(r'B[a-z]\d[+]?[#]?', move):
            move_type = 'bishop'
        # queen move
        if re.fullmatch(r'Q[a-z]\d[+]?[#]?', move):
            move_type = 'queen'
        # king move
        if re.fullmatch(r'K[a-z]\d[+]?[#]?', move):
            move_type = 'king'
        if move == 'O-O':
            move_type = 'short castle'
        if move == 'O-O-O':
            move_type = 'long castle'
        if re.fullmatch(r'[abcdefgh|A-Z]x[abcdefgh]\d[+]?[#]?', move):
            if move[0] in alphabet:
                move_type = 'pawn capture'
            elif move[0] == 'R':
                move_type = 'rook capture'
            elif move[0] == 'B':
                move_type = 'bishop capture'
            elif move[0] == 'N':
                move_type = 'knight capture'
            elif move[0] == 'Q':
                move_type = 'queen capture'
            else:
                move_type = 'king capture'
        if re.fullmatch(r'R[abcdefgh|0-9][abcdefgh]\d[+]?[#]?', move):
            move_type = 'pos'
        if re.fullmatch(r'[R|N]\d[abcdefgh]\d[+]?[#]?', move) or re.fullmatch(r'[R|N][abcdefgh][a-z]\d[+]?[#]?', move):
            move_type = 'two pieces'
        if re.fullmatch(r'[R|N]\dx[abcdefgh]\d[+]?[#]?', move) or re.fullmatch(r'[R|N][abcdefgh]x[abcdefgh]\d[+]?[#]?',
                                                                               move):
            move_type = 'two pieces capture'

        return move_type

    def move(self, num):
        # finding side color
        if num % 2 == 0:
            color = 'white'
        else:
            color = 'black'

        # finding move type
        move_type = self.move_types(self.game_moves[num])
        if move_type == 'game finished':
            if self.game_moves[num] == '1-0':
                return 'White won!'
            elif self.game_moves[num] == '0-1':
                return 'Black won!'
            else:
                return 'Draw'
        if move_type not in ('pawn', 'pawn capture', 'short castle', 'long castle', 'two pieces', 'two pieces capture'):
            for piece in self.pieces:
                if piece.color == color:
                    if piece.piece_type == move_type:
                        if piece.piece_type == 'rook':
                            self.rook_blocked_lines(piece)
                        final_position = (int(self.game_moves[num][2]) - 1) * 8 + alphabet.index(
                            self.game_moves[num][1]) + 1
                        if final_position in piece.possible_moves:
                            self.pieces.remove(piece)
                            piece.new_position(final_position)
                            piece.finding_possible_moves()
                            self.pieces.append(piece)
                            if piece.piece_type == 'rook':
                                self.rook_blocked_lines(piece)
                            return move_type
                    elif piece.piece_type + ' capture' == move_type:
                        final_position = (int(self.game_moves[num][3]) - 1) * 8 + alphabet.index(
                            self.game_moves[num][2]) + 1
                        if piece.piece_type == 'rook':
                            self.rook_blocked_lines(piece)
                        if final_position in piece.possible_moves:
                            self.piece_capture(piece.position, final_position)
                            return move_type, len(self.pieces)
                    elif move_type == 'pos':
                        return 'pos'
                    elif move_type == 'pos2':
                        return 'pos2'
        else:
            if move_type == 'pawn':
                final_position = (int(self.game_moves[num][1]) - 1) * 8 + alphabet.index(self.game_moves[num][0]) + 1
                for piece in self.pieces:
                    if piece.piece_type == 'pawn':
                        if color == 'white':
                            if piece.color == color:
                                if piece.position == final_position - 8:
                                    self.pieces.remove(piece)
                                    new_piece = ChessPiece('pawn', final_position, color)
                                    self.pieces.append(new_piece)
                                    return 'white pawn'
                                elif piece.position == final_position - 16:
                                    self.pieces.remove(piece)
                                    new_piece = ChessPiece('pawn', final_position, color)
                                    self.pieces.append(new_piece)
                                    return 'white pawn 16'
                        else:
                            if piece.position == final_position + 8:
                                self.pieces.remove(piece)
                                new_piece = ChessPiece('pawn', final_position, color)
                                self.pieces.append(new_piece)
                                return 'black pawn'
                            elif piece.position == final_position + 16:
                                self.pieces.remove(piece)
                                new_piece = ChessPiece('pawn', final_position, color)
                                self.pieces.append(new_piece)
                                return 'black pawn 16'
            elif move_type == 'pawn capture':
                final_position = (int(self.game_moves[num][3]) - 1) * 8 + alphabet.index(self.game_moves[num][2]) + 1
                pawn_horizontal_position = alphabet.index(self.game_moves[num][0])
                final_horizontal_position = alphabet.index(self.game_moves[num][2])

                if color == 'white':
                    if pawn_horizontal_position > final_horizontal_position:
                        pawn_position = final_position - 7
                    else:
                        pawn_position = final_position - 9
                else:
                    if pawn_horizontal_position > final_horizontal_position:
                        pawn_position = final_position + 9
                    else:
                        pawn_position = final_position + 7
                self.piece_capture(pawn_position, final_position)

            elif move_type == 'short castle':
                for piece in self.pieces:
                    if color == 'white':
                        rook = piece if piece.position == 8 else None
                        king = piece if piece.position == 5 else None
                        if rook:
                            rook.new_position(6)
                        if king:
                            king.new_position(7)
                    else:
                        rook = piece if piece.position == 64 else None
                        king = piece if piece.position == 61 else None
                        if rook:
                            rook.new_position(62)
                        if king:
                            king.new_position(63)
            elif move_type == 'long castle':
                for piece in self.pieces:
                    if color == 'white':
                        rook = piece if piece.position == 1 else None
                        king = piece if piece.position == 5 else None
                        if rook:
                            rook.new_position(4)
                        if king:
                            king.new_position(3)
                    else:
                        rook = piece if piece.position == 57 else None
                        king = piece if piece.position == 61 else None
                        if rook:
                            rook.new_position(60)
                        if king:
                            king.new_position(59)
            elif move_type == 'two piece':
                try:
                    piece_position = (int(self.game_moves[num][1]) - 1) * 8 + alphabet.index(
                        self.game_moves[num][2]) + 1
                except ValueError:
                    piece_position = (int(self.game_moves[num][3]) - 1) * 8 + alphabet.index(
                        self.game_moves[num][1]) + 1
                final_position = (int(self.game_moves[num][3]) - 1) * 8 + alphabet.index(self.game_moves[num][2]) + 1
                for piece in self.pieces:
                    if piece.position == piece_position:
                        piece.new_position(final_position)
                        if piece.piece_type == 'rook':
                            self.rook_blocked_lines(piece)


            elif move_type == 'two rooks/knights capture':
                try:
                    piece_position = (int(self.game_moves[num][1]) - 1) * 8 + alphabet.index(
                        self.game_moves[num][3]) + 1
                except ValueError:
                    piece_position = (int(self.game_moves[num][4]) - 1) * 8 + alphabet.index(
                        self.game_moves[num][1]) + 1
                final_position = (int(self.game_moves[num][4]) - 1) * 8 + alphabet.index(self.game_moves[num][3]) + 1
                for piece in self.pieces:
                    if piece.position == piece_position:
                        self.piece_capture(piece_position, final_position)

            else:
                pass
        return move_type
        # finding piece(s)
        # final field


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

gt = '''
1. e4 d5 2. e5 f5 3. exf6 Kf7
'''
two_rooks_game = '1. h4 h5 2. Rh3 a6 3. a3 b6 4. a4 d5 5. Raa3 d4 6. g4 d3 7. Rhxd3'
ng = NewGame(game_text)
for i in range(0, len(ng.game_moves)):
    print(i, ng.game_moves[i])
for i in range(0, len(ng.game_moves)):
    print(ng.move(i))
