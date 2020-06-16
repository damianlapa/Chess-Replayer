import re
from PIL import Image, ImageTk

alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')


class ChessPiece:
    def __init__(self, piece_type, position=None, color='white'):
        self.piece_type = piece_type
        self.color = color
        self.position = position
        self.possible_moves = []
        self.protected_moves = []
        self.border_fields = ()
        self.finding_possible_moves()
        self.image = None

    def __str__(self):
        return self.color + self.piece_type

    def representation(self):
        if not self.image:
            self.image = ImageTk.PhotoImage(Image.open("pieces/{}.png".format(self)))
        return self.image

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
        z = 1
        while z < 9:
            fields_south.append(z)
            fields_north.append(56 + z)
            fields_west.append(1 + (z - 1) * 8)
            fields_east.append(8 + (z - 1) * 8)
            z += 1
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
                    if self.position % 8 != 1:
                        self.possible_moves.append(self.position + 7)
                    if self.position % 8 != 0:
                        self.possible_moves.append(self.position + 9)
                    for j in range(1, 3):
                        self.possible_moves.append(self.position + 8 * j)
                else:
                    self.possible_moves.append(self.position + 8)
                    if self.position % 8 != 1:
                        self.possible_moves.append(self.position + 7)
                    if self.position % 8 != 0:
                        self.possible_moves.append(self.position + 9)

            else:
                if self.position in range(49, 57):
                    if self.position % 8 != 1:
                        self.possible_moves.append(self.position - 9)
                    if self.position % 8 != 0:
                        self.possible_moves.append(self.position - 7)
                    for j in range(1, 3):
                        self.possible_moves.append(self.position - 8 * j)
                else:
                    self.possible_moves.append(self.position - 8)
                    if self.position % 8 != 1:
                        self.possible_moves.append(self.position - 9)
                    if self.position % 8 != 0:
                        self.possible_moves.append(self.position - 7)

            return self.possible_moves
        # pawn capture

        # knight move
        elif self.piece_type == 'knight':
            # decode field number to chess board field
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
            move_1 = self.position + 8 if self.position not in (57, 65) else 0
            move_2 = self.position - 8 if self.position not in (1, 9) else 0
            move_3 = self.position + 9 if self.position not in (57, 65) and self.position % 8 != 0 else 0
            move_4 = self.position - 9 if self.position not in (1, 9) and self.position % 8 != 1 else 0
            move_5 = self.position + 7 if self.position not in (57, 65) and self.position % 8 != 1 else 0
            move_6 = self.position - 7 if self.position not in (1, 9) and self.position % 8 != 0 else 0
            move_7 = self.position + 1 if self.position % 8 != 0 else 0
            move_8 = self.position - 1 if self.position % 8 != 1 else 0

            king_moves = (move_1, move_2, move_3, move_4, move_5, move_6, move_7, move_8)
            for move in king_moves:
                if move > 0 and move < 65:
                    self.possible_moves.append(move)

            return self.possible_moves


class NewGame:
    def __init__(self, game_description):
        self.pieces = []
        self.game_description = game_description
        self.set_all_pieces()
        self.game_moves = []
        self.reading_game_history()

    def reset(self):
        self.__init__(game_description=self.game_description)

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
        index = self.pieces.index(rook)
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
        self.pieces.insert(index, rook)
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
        return self.pieces.index(moved_capturing_piece)

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
            move_type = 'two rooks/knights capture'
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
        if move_type not in (
                'pawn', 'pawn capture', 'short castle', 'long castle', 'two pieces', 'two rooks/knights capture'):
            for piece in self.pieces:
                if piece.piece_type == 'rook':
                    self.rook_blocked_lines(piece)
            for piece in self.pieces:
                if piece.color == color:
                    if piece.piece_type == move_type:

                        final_position = (int(self.game_moves[num][2]) - 1) * 8 + alphabet.index(
                            self.game_moves[num][1]) + 1
                        if final_position in piece.possible_moves:
                            old_position = piece.position
                            self.pieces.remove(piece)
                            piece.new_position(final_position)
                            piece.finding_possible_moves()
                            self.pieces.append(piece)
                            return old_position, piece.position, self.pieces.index(piece)
                    elif piece.piece_type + ' capture' == move_type:
                        final_position = (int(self.game_moves[num][3]) - 1) * 8 + alphabet.index(
                            self.game_moves[num][2]) + 1
                        if piece.piece_type == 'rook':
                            self.rook_blocked_lines(piece)
                        if final_position in piece.possible_moves:
                            piece_old_position = piece.position
                            piece_index = self.piece_capture(piece.position, final_position)
                            return piece_old_position, final_position, piece_index
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
                                    old_position = piece.position
                                    self.pieces.remove(piece)
                                    piece.new_position(final_position)
                                    self.pieces.append(piece)
                                    return old_position, piece.position, self.pieces.index(piece)
                                elif piece.position == final_position - 16:
                                    old_position = piece.position
                                    self.pieces.remove(piece)
                                    piece.new_position(final_position)
                                    self.pieces.append(piece)
                                    return old_position, piece.position, self.pieces.index(piece)
                        else:
                            if piece.position == final_position + 8:
                                old_position = piece.position
                                self.pieces.remove(piece)
                                piece.new_position(final_position)
                                self.pieces.append(piece)
                                return old_position, piece.position, self.pieces.index(piece)
                            elif piece.position == final_position + 16:
                                old_position = piece.position
                                self.pieces.remove(piece)
                                piece.new_position(final_position)
                                self.pieces.append(piece)
                                return old_position, piece.position, self.pieces.index(piece)
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
                pawn = None
                for piece in self.pieces:
                    if piece.position == final_position:
                        pawn = piece
                return pawn_position, final_position, self.pieces.index(pawn)

            elif move_type == 'short castle':
                rook = None
                king = None
                king_old_position = None
                king_new_position = None
                king_index = None
                rook_old_position = None
                rook_new_position = None
                rook_index = None
                for piece in self.pieces:
                    if color == 'white':
                        if not rook:
                            rook = piece if piece.position == 8 else None
                            if rook:
                                rook_old_position = piece.position

                        if not king:
                            king = piece if piece.position == 5 else None
                            if king:
                                king_old_position = piece.position
                        if rook and king:
                            rook.new_position(6)
                            king.new_position(7)
                            king_new_position = king.position
                            rook_new_position = rook.position
                            king_index = self.pieces.index(king)
                            rook_index = self.pieces.index(rook)
                            return king_old_position, king_new_position, king_index, rook_old_position, \
                                   rook_new_position, rook_index
                    else:
                        if not rook:
                            rook = piece if piece.position == 64 else None
                            if rook:
                                rook_old_position = piece.position
                        if not king:
                            king = piece if piece.position == 61 else None
                            if king:
                                king_old_position = piece.position
                        if rook and king:
                            rook.new_position(62)
                            king.new_position(63)
                            king_new_position = king.position
                            rook_new_position = rook.position
                            king_index = self.pieces.index(king)
                            rook_index = self.pieces.index(rook)
                            return king_old_position, king_new_position, king_index, rook_old_position, \
                                   rook_new_position, rook_index

            elif move_type == 'long castle':
                rook = None
                king = None
                king_old_position = None
                king_new_position = None
                king_index = None
                rook_old_position = None
                rook_new_position = None
                rook_index = None
                for piece in self.pieces:
                    if color == 'white':
                        if not rook:
                            rook = piece if piece.position == 1 else None
                            if rook:
                                rook_old_position = piece.position
                        if not king:
                            king = piece if piece.position == 5 else None
                            if king:
                                king_old_position = piece.position
                        if rook and king:
                            rook.new_position(4)
                            king.new_position(3)
                            king_new_position = king.position
                            rook_new_position = rook.position
                            king_index = self.pieces.index(king)
                            rook_index = self.pieces.index(rook)
                            return king_old_position, king_new_position, king_index, rook_old_position, \
                                   rook_new_position, rook_index
                    else:
                        if not rook:
                            rook = piece if piece.position == 57 else None
                            if rook:
                                rook_old_position = piece.position
                        if not king:
                            king = piece if piece.position == 61 else None
                            if king:
                                king_old_position = piece.position
                        if rook and king:
                            rook.new_position(60)
                            king.new_position(59)
                            king_new_position = king.position
                            rook_new_position = rook.position
                            king_index = self.pieces.index(king)
                            rook_index = self.pieces.index(rook)
                            return king_old_position, king_new_position, king_index, rook_old_position, \
                                   rook_new_position, rook_index

            elif move_type == 'two pieces':
                index = None
                piece_position = None
                try:
                    piece_position = (int(self.game_moves[num][1]) - 1) * 8 + alphabet.index(
                        self.game_moves[num][2]) + 1
                except ValueError:
                    if self.game_moves[num][0] == 'R':
                        piece_type = 'rook'
                    else:
                        piece_type = 'knight'
                    for piece in self.pieces:
                        if piece.color == color:
                            if piece.piece_type == piece_type:
                                possible_positions = []
                                for x in range(0, 8):
                                    possible_field = (alphabet.index(self.game_moves[num][1]) + 1) + x * 8
                                    possible_positions.append(possible_field)
                                if piece.position in possible_positions:
                                    piece_position = piece.position
                final_position = (int(self.game_moves[num][3]) - 1) * 8 + alphabet.index(self.game_moves[num][2]) + 1
                for piece in self.pieces:
                    if piece.position == piece_position:
                        piece.new_position(final_position)
                        if piece.piece_type == 'rook':
                            self.rook_blocked_lines(piece)

                for piece in self.pieces:
                    if piece.position == final_position:
                        index = self.pieces.index(piece)

                return piece_position, final_position, index

            elif move_type == 'two rooks/knights capture':
                index = None
                piece_position = None
                try:
                    piece_position = (int(self.game_moves[num][1]) - 1) * 8 + alphabet.index(
                        self.game_moves[num][3]) + 1
                except ValueError:
                    if self.game_moves[num][0] == 'R':
                        piece_type = 'rook'
                    else:
                        piece_type = 'knight'
                    for piece in self.pieces:
                        if piece.color == color:
                            if piece.piece_type == piece_type:
                                possible_positions = []
                                for x in range(0, 8):
                                    possible_field = (alphabet.index(self.game_moves[num][1]) + 1) + x * 8
                                    possible_positions.append(possible_field)
                                if piece.position in possible_positions:
                                    piece_position = piece.position
                final_position = (int(self.game_moves[num][4]) - 1) * 8 + alphabet.index(self.game_moves[num][3]) + 1
                for piece in self.pieces:
                    if piece.position == piece_position:
                        self.piece_capture(piece_position, final_position)

                for piece in self.pieces:
                    if piece.position == final_position:
                        index = self.pieces.index(piece)

                return piece_position, final_position, index


            else:
                pass


class ChessBoard:
    def __init__(self):
        self.chess_pieces = []
        self.black_long_castle_possibility = True
        self.black_short_castle_possibility = True
        self.white_short_castle_possibility = True
        self.white_long_castle_possibility = True
        self.en_passant = None
        self.en_passant_capture = None

    def __str__(self):
        for piece in self.chess_pieces:
            print(piece)

    def add_piece(self, piece):
        self.chess_pieces.append(piece)

    def find_piece_by_position(self, field_num):
        for piece in self.chess_pieces:
            if piece.position == field_num:
                return piece
        return False

    def chess_piece_move(self, piece, new_position):
        if self.en_passant:
            if piece.piece_type == 'pawn' and new_position == self.en_passant[3]:
                self.en_passant_capture = True
        self.en_passant = False
        if piece.piece_type == 'king':
            if piece.color == 'white':
                self.white_long_castle_possibility = False
                self.white_short_castle_possibility = False
            else:
                self.black_short_castle_possibility = False
                self.white_long_castle_possibility = False
        elif piece.piece_type == 'rook':
            if piece.position == 1:
                self.white_long_castle_possibility = False
            elif piece.position == 8:
                self.white_short_castle_possibility = False
            elif piece.position == 57:
                self.black_long_castle_possibility = False
            elif piece.position == 64:
                self.black_short_castle_possibility = False

        elif piece.piece_type == 'pawn':
            if abs(piece.position - new_position) == 16:
                self.en_passant = (True, new_position, piece.color, new_position + (8 if piece.color == 'black' else -8))

            if self.en_passant_capture:
                deleted_piece = self.find_piece_by_position(new_position + (8 if piece.color == 'black' else - 8))
                print(deleted_piece, deleted_piece.position)
                self.chess_pieces.remove(deleted_piece)
                self.en_passant_capture = False

        piece_index = self.chess_pieces.index(piece)
        self.chess_pieces.remove(piece)
        piece.new_position(new_position)
        self.piece_current_moves(piece)
        self.chess_pieces.insert(piece_index, piece)
        for piece in self.chess_pieces:
            if piece.piece_type == 'rook' or piece.piece_type == 'king':
                piece.finding_possible_moves()
                self.piece_current_moves(piece)

    def chess_piece_capture(self, piece, new_position):
        captured_piece = self.find_piece_by_position(new_position)
        if captured_piece:
            self.chess_pieces.remove(captured_piece)
            self.chess_piece_move(piece, new_position)

    def piece_current_moves(self, piece):

        piece.finding_possible_moves()

        if piece.piece_type == 'rook':
            piece.protected_moves = []
            field = piece.position
            north_block = False
            south_block = False
            east_block = False
            west_block = False

            for i in range(1, 8):
                field_1 = field + i if field % 8 != 0 else 0
                if (field + i) % 8 == 1:
                    field_1 = 0
                field_2 = field - i if field % 8 != 1 else 0
                if (field - i) % 8 == 0:
                    field_2 = 0
                field_3 = field + (8 * i)
                field_4 = field - (8 * i)

                field_1_occupancy = self.find_piece_by_position(field_1)
                field_2_occupancy = self.find_piece_by_position(field_2)
                field_3_occupancy = self.find_piece_by_position(field_3)
                field_4_occupancy = self.find_piece_by_position(field_4)

                if east_block:
                    if field_1 in piece.possible_moves:
                        piece.possible_moves.remove(field_1)
                if west_block:
                    if field_2 in piece.possible_moves:
                        piece.possible_moves.remove(field_2)
                if north_block:
                    if field_3 in piece.possible_moves:
                        piece.possible_moves.remove(field_3)
                if south_block:
                    if field_4 in piece.possible_moves:
                        piece.possible_moves.remove(field_4)

                if field_1_occupancy:
                    if field_1_occupancy.color == piece.color:

                        if field_1 in piece.possible_moves:
                            piece.possible_moves.remove(field_1)
                        if not east_block:
                            piece.protected_moves.append(field_1)
                        east_block = True
                    else:
                        east_block = True
                if field_2_occupancy:
                    if field_2_occupancy.color == piece.color:

                        if field_2 in piece.possible_moves:
                            piece.possible_moves.remove(field_2)
                        if not west_block:
                            piece.protected_moves.append(field_2)
                        west_block = True
                    else:
                        west_block = True
                if field_3_occupancy:
                    if field_3_occupancy.color == piece.color:

                        if field_3 in piece.possible_moves:
                            piece.possible_moves.remove(field_3)
                        if not north_block:
                            piece.protected_moves.append(field_3)
                        north_block = True
                    else:
                        north_block = True
                if field_4_occupancy:
                    if field_4_occupancy.color == piece.color:

                        if field_4 in piece.possible_moves:
                            piece.possible_moves.remove(field_4)
                        if not south_block:
                            piece.protected_moves.append(field_4)
                        south_block = True
                    else:
                        south_block = True
            return piece.possible_moves

        if piece.piece_type == 'knight':
            fields_to_remove = []
            piece.protected_moves = []
            for move in piece.possible_moves:
                if self.find_piece_by_position(move):
                    if self.find_piece_by_position(move).color == piece.color:
                        piece.protected_moves.append(move)
                        fields_to_remove.append(move)
            for field in fields_to_remove:
                piece.possible_moves.remove(field)
            return piece.possible_moves

        if piece.piece_type == 'bishop':
            field = piece.position
            piece.protected_moves = []
            north_east_block = False
            south_east_block = False
            south_west_block = False
            north_west_block = False
            for j in range(1, 8):
                field_1 = field + (9 * j) if (field + (9 * j)) % 8 != 1 else 0
                field_2 = field - (7 * j) if (field - (7 * j)) % 8 != 1 else 0
                field_3 = field - (9 * j) if (field - (9 * j)) % 8 != 0 else 0
                field_4 = field + (7 * j) if (field + (7 * j)) % 8 != 0 else 0

                field_1_occupancy = self.find_piece_by_position(field_1)
                field_2_occupancy = self.find_piece_by_position(field_2)
                field_3_occupancy = self.find_piece_by_position(field_3)
                field_4_occupancy = self.find_piece_by_position(field_4)

                if north_east_block:
                    if field_1 in piece.possible_moves:
                        piece.possible_moves.remove(field_1)
                if south_east_block:
                    if field_2 in piece.possible_moves:
                        piece.possible_moves.remove(field_2)
                if south_west_block:
                    if field_3 in piece.possible_moves:
                        piece.possible_moves.remove(field_3)
                if north_west_block:
                    if field_4 in piece.possible_moves:
                        piece.possible_moves.remove(field_4)

                if field_1_occupancy:
                    if field_1_occupancy.color == piece.color:
                        if field_1 in piece.possible_moves:
                            piece.protected_moves.append(field_1)
                            piece.possible_moves.remove(field_1)
                        north_east_block = True
                    else:
                        north_east_block = True
                if field_2_occupancy:
                    if field_2_occupancy.color == piece.color:
                        if field_2 in piece.possible_moves:
                            piece.protected_moves.append(field_2)
                            piece.possible_moves.remove(field_2)
                        south_east_block = True
                    else:
                        south_east_block = True
                if field_3_occupancy:
                    if field_3_occupancy.color == piece.color:
                        if field_3 in piece.possible_moves:
                            piece.protected_moves.append(field_3)
                            piece.possible_moves.remove(field_3)
                        south_west_block = True
                    else:
                        south_west_block = True
                if field_4_occupancy:
                    if field_4_occupancy.color == piece.color:
                        if field_4 in piece.possible_moves:
                            piece.protected_moves.append(field_4)
                            piece.possible_moves.remove(field_4)
                        north_west_block = True
                    else:
                        north_west_block = True
            return piece.possible_moves

        if piece.piece_type == 'queen':
            piece.protected_moves = []
            bishop = ChessPiece('bishop', piece.position, piece.color)
            rook = ChessPiece('rook', piece.position, piece.color)
            self.piece_current_moves(bishop)
            self.piece_current_moves(rook)
            piece.possible_moves = bishop.possible_moves + rook.possible_moves
            piece.protected_moves = bishop.protected_moves + rook.protected_moves
            return piece.possible_moves

        if piece.piece_type == 'king':
            piece.protected_moves = []
            moves_to_remove = []
            for move in piece.possible_moves:
                if self.find_piece_by_position(move):
                    if self.find_piece_by_position(move).color == piece.color:
                        piece.protected_moves.append(move)
                        moves_to_remove.append(move)
                for piece_ in self.chess_pieces:
                    if piece.color != piece_.color and piece_.piece_type != 'king':
                        self.piece_current_moves(piece_)
                        if move in piece_.possible_moves or move in piece_.protected_moves:
                            moves_to_remove.append(move)
            for move in moves_to_remove:
                if move in piece.possible_moves:
                    piece.possible_moves.remove(move)

            return piece.possible_moves

        if piece.piece_type == 'pawn':
            piece.protected_moves = []
            if piece.color == 'white':
                if self.find_piece_by_position(piece.position + 9) and piece.position % 8 != 0:
                    if self.find_piece_by_position(piece.position + 9).color == piece.color:
                        piece.protected_moves.append(piece.position + 9)
                        piece.possible_moves.remove(piece.position + 9)
                else:
                    try:
                        piece.possible_moves.remove(piece.position + 9)
                    except ValueError:
                        pass
                if self.find_piece_by_position(piece.position + 7) and piece.position % 8 != 1:
                    if self.find_piece_by_position(piece.position + 7).color == piece.color:
                        piece.protected_moves.append(piece.position + 7)
                        piece.possible_moves.remove(piece.position + 7)
                else:
                    try:
                        piece.possible_moves.remove(piece.position + 7)
                    except ValueError:
                        pass
                if self.find_piece_by_position(piece.position + 8):
                    try:
                        piece.possible_moves.remove(piece.position + 8)
                        piece.possible_moves.remove(piece.position + 16)
                    except ValueError:
                        pass
                if self.find_piece_by_position(piece.position + 16):
                    try:
                        piece.possible_moves.remove(piece.position + 16)
                    except ValueError:
                        pass
            else:
                if self.find_piece_by_position(piece.position - 9) and piece.position % 8 != 1:
                    if self.find_piece_by_position(piece.position - 9).color == piece.color:
                        piece.protected_moves.append(piece.position - 9)
                        piece.possible_moves.remove(piece.position - 9)
                else:
                    try:
                        piece.possible_moves.remove(piece.position - 9)
                    except ValueError:
                        pass
                if self.find_piece_by_position(piece.position - 7) and piece.position % 8 != 0:
                    if self.find_piece_by_position(piece.position - 7).color == piece.color:
                        piece.protected_moves.append(piece.position - 7)
                        piece.possible_moves.remove(piece.position - 7)
                else:
                    try:
                        piece.possible_moves.remove(piece.position - 7)
                    except ValueError:
                        pass
                if self.find_piece_by_position(piece.position - 8):
                    try:
                        piece.possible_moves.remove(piece.position - 8)
                        piece.possible_moves.remove(piece.position - 16)
                    except ValueError:
                        pass
                if self.find_piece_by_position(piece.position - 16):
                    try:
                        piece.possible_moves.remove(piece.position - 16)
                    except ValueError:
                        pass
            if self.en_passant:
                if piece.color != self.en_passant[2]:
                    possibility_checker = piece.position // 8
                    if piece.position % 8 == 0:
                        possibility_checker -= 1
                    if possibility_checker == self.en_passant[1] // 8:
                        if piece.position % 8 == 0 and piece.position - 1 == self.en_passant[1]:
                            piece.possible_moves.append(self.en_passant[1] + (- 8 if piece.color == 'black' else 8))
                        elif piece.position % 8 == 1 and piece.position + 1 == self.en_passant[1]:
                            piece.possible_moves.append(self.en_passant[1] + (- 8 if piece.color == 'black' else 8))
                        elif abs(piece.position - self.en_passant[1]) == 1:
                            piece.possible_moves.append(self.en_passant[1] + (- 8 if piece.color == 'black' else 8))
            return piece.possible_moves

    def test_position(self):
        for piece in self.chess_pieces:
            self.piece_current_moves(piece)
        return self.king_check('white'), self.king_check('black')

    def king_check(self, side):
        king = None
        for piece in self.chess_pieces:
            if piece.piece_type == 'king':
                if piece.color == side:
                    king = piece
        if king:
            king_position = king.position
            for piece in self.chess_pieces:
                if piece.color != king.color:
                    if king_position in self.piece_current_moves(piece):
                        return True
        else:
            return False

    def copy_board(self):
        new_pieces = []
        for piece in self.chess_pieces:
            new_piece_type = piece.piece_type
            new_piece_color = piece.color
            new_piece_position = piece.position
            new_piece = ChessPiece(new_piece_type, new_piece_position, new_piece_color)
            new_pieces.append(new_piece)
        return new_pieces

    def king_castle_possibility(self, king):

        def check_castle_block(field_1, field_2):
            for piece in self.chess_pieces:
                if piece.color != king.color:
                    self.piece_current_moves(piece)
                    if field_1 in piece.possible_moves or field_2 in piece.possible_moves:
                        return True
            return False

        def check_fields_emptiness(fields):
            for piece in self.chess_pieces:
                if piece.position in fields:
                    return False
            return True

        if king.color == 'black':
            if self.black_short_castle_possibility:
                if check_fields_emptiness((62, 63)):
                    if not check_castle_block(62, 63):
                        king_index = self.chess_pieces.index(king)
                        self.chess_pieces.remove(king)
                        king.possible_moves.append(63)
                        rook = self.find_piece_by_position(64)
                        rook.possible_moves.append(62)
                        self.chess_pieces.insert(king_index, king)
            if self.black_long_castle_possibility:
                if check_fields_emptiness((58, 59, 60)):
                    if not check_castle_block(59, 60):
                        king_index = self.chess_pieces.index(king)
                        self.chess_pieces.remove(king)
                        king.possible_moves.append(59)
                        rook = self.find_piece_by_position(57)
                        rook.possible_moves.append(60)
                        self.chess_pieces.insert(king_index, king)
        else:
            if self.white_short_castle_possibility:
                if check_fields_emptiness((6, 7)):
                    if not check_castle_block(6, 7):
                        king_index = self.chess_pieces.index(king)
                        self.chess_pieces.remove(king)
                        king.possible_moves.append(7)
                        rook = self.find_piece_by_position(8)
                        rook.possible_moves.append(6)
                        self.chess_pieces.insert(king_index, king)
                        # self.castle(king, rook, 'short')
            if self.white_long_castle_possibility:
                if check_fields_emptiness((2, 3, 4)):
                    if not check_castle_block(3, 4):
                        king_index = self.chess_pieces.index(king)
                        self.chess_pieces.remove(king)
                        king.possible_moves.append(3)
                        rook = self.find_piece_by_position(1)
                        rook.possible_moves.append(4)
                        self.chess_pieces.insert(king_index, king)

    def castle(self, king, rook, mode):
        if king.color == 'black':
            if mode == 'short':
                self.chess_piece_move(king, 63)
                self.chess_piece_move(rook, 62)
            else:
                self.chess_piece_move(king, 59)
                self.chess_piece_move(rook, 60)

class TwoPlayersGame:
    def __init__(self):
        self.move_counter = 0
        self.board = ChessBoard()
        self.pieces = self.board.chess_pieces
        self.set_all_pieces()

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
            '''
        for i in range(0, 2):
            piece = ChessPiece('bishop', 3 + i * 3)
            black_piece = ChessPiece('bishop', 59 + i * 3, 'black')
            self.pieces.append(piece)
            self.pieces.append(black_piece)

        white_queen = ChessPiece('queen', 4)

        black_queen = ChessPiece('queen', 60, 'black')'''
        white_king = ChessPiece('king', 5)
        black_king = ChessPiece('king', 61, 'black')

        '''self.pieces.append(white_queen)
        self.pieces.append(black_queen)'''
        self.pieces.append(white_king)
        self.pieces.append(black_king)

        for piece in self.pieces:
            index = self.pieces.index(piece)
            self.pieces.remove(piece)
            self.board.piece_current_moves(piece)
            self.pieces.insert(index, piece)

    def king_check(self, side):
        king = None
        for piece in self.pieces:
            if piece.piece_type == 'king':
                if piece.color == side:
                    king = piece
        if king:
            king_position = king.position
            for piece in self.pieces:
                if piece.color != king.color:
                    if king_position in self.board.piece_current_moves(piece):
                        return True
        else:
            return False

    def white_move(self,):
        pass

    def black_move(self):
        pass

    def game(self):
        if self.move_counter % 2 == 0:
            self.white_move()
        else:
            self.black_move()


test_game = '''
1. c4 e6 2. Nf3 d5 3. d4 Nf6 4. Nc3 Be7 5. Bg5 O-O 6. e3 h6
7. Bh4 b6 8. cxd5 Nxd5 9. Bxe7 Qxe7 10. Nxd5 exd5 11. Rc1 Be6
12. Qa4 c5 13. Qa3 Rc8 14. Bb5 a6 15. dxc5 bxc5 16. O-O Ra7
17. Be2 Nd7 18. Nd4 Qf8 19. Nxe6 fxe6 20. e4 d4 21. f4 Qe7
22. e5 Rb8 23. Bc4 Kh8 24. Qh3 Nf8 25. b3 a5 26. f5 exf5
27. Rxf5 Nh7 28. Rcf1 Qd8 29. Qg3 Re7 30. h4 Rbb7 31. e6 Rbc7
32. Qe5 Qe8 33. a4 Qd8 34. R1f2 Qe8 35. R2f3 Qd8 36. Bd3 Qe8
37. Qe4 Nf6 38. Rxf6 gxf6 39. Rxf6 Kg8 40. Bc4 Kh8 41. Qf4 1-0
'''
test_2 = '1. e4 b5 2. h4 Nc6 3. d4 Rb8 4. g4'
