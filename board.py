from tkinter import *
from PIL import Image, ImageTk
from game import ChessPiece, NewGame, TwoPlayersGame

white_pawn = ChessPiece('pawn', 9)
white_pawn_2 = ChessPiece('pawn', 13)
black_pawn = ChessPiece('pawn', 55, 'black')

alphabet2 = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')

test_3 = '''1. h4 e5 2. e4 f5 3. Qh5+ g6 4. Nc3 Ne7
5. Qxg6+ Nxg6 6. Ke2 Qxh4 7. Kf3 Qh3+ 8. g3 Nh4+
9. Ke3 f4+ 10. Ke2 b6 11. b3 Ba6+ 12. Kd1 Qxf1#'''


class GameMenu:
    def __init__(self, env):
        self.env = env
        self.main_canvas = None
        self.bg_image = ImageTk.PhotoImage(Image.open('img/gettyimages-138125883.png'))
        self.load_exemplary_game_button = None
        self.load_game_button = None
        self.return_button = None
        self.read_text_button = None
        self.game = None
        self.game_board = None
        self.game_frame = None
        self.game_text_window = None
        self.two_players_button = None
        self.run_game()

    def main_menu(self):
        self.env.geometry('800x520')
        self.env.configure(bg='black')
        self.main_canvas = Canvas(self.env, width=800, height=520)
        self.main_canvas.place(x=0, y=0)
        self.main_canvas.create_image(400, 260, image=self.bg_image)
        self.load_exemplary_game_button = Button(self.env, text='Load Exemplary', command=self.load_exemplary_game)
        self.load_exemplary_game_button.place(x=50, y=50)
        self.load_game_button = Button(self.env, text='Paste Game Description', command=self.display_text_window)
        self.load_game_button.place(x=50, y=100)
        self.two_players_button = Button(self.env, text='2 Players Game', command=self.two_players_game)
        self.two_players_button.place(x=50, y=150)

    def two_players_game(self):
        self.main_canvas.place_forget()
        self.load_exemplary_game_button.place_forget()
        self.load_game_button.place_forget()
        self.env.geometry('1550x1000')
        self.env.configure(bg='black')
        self.return_button = Button(self.env, text='X', command=self.return_to_menu)
        self.return_button.place(x=1510, y=25)
        self.game_frame = Frame(self.env, width=1500, height=1000, bg='black')
        self.game_frame.place(x=0, y=0)
        self.game = Board(self.game_frame, TwoPlayersGame(), '2')

    def display_text_window(self):
        if not self.game_text_window:
            self.game_text_window = Text(self.main_canvas, height=27, width=67)
            self.game_text_window.place(x=250, y=10)
        self.read_text_button = Button(self.main_canvas, text='Load Game', command=self.load_pasted_game)
        self.read_text_button.place(x=465, y=480)

    def test_pasted_game(self, test_game):
        for i in range(0, len(test_game.game_moves)):
            if not test_game.move(i):
                return False
        return True

    def load_pasted_game(self):
        pasted_text = self.game_text_window.get('1.0', 'end-1c')
        self.game = NewGame(pasted_text)
        test = self.test_pasted_game(self.game)
        if test:
            self.game = NewGame(pasted_text)
            self.load_game()
        else:
            self.game_text_window.delete('1.0', END)
            self.game_text_window.insert(INSERT, 'Wrong format!')

    def load_exemplary_game(self):
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
        self.game = NewGame(test_game)
        self.load_game()

    def load_game(self):
        self.main_canvas.place_forget()
        self.load_exemplary_game_button.place_forget()
        self.load_game_button.place_forget()
        self.env.geometry('1550x1000')
        self.env.configure(bg='black')
        self.return_button = Button(self.env, text='X', command=self.return_to_menu)
        self.return_button.place(x=1510, y=25)
        self.game_frame = Frame(self.env, width=1500, height=1000, bg='black')
        self.game_frame.place(x=0, y=0)
        self.game_board = Board(self.game_frame, self.game, '1')
        self.run_game()

    def return_to_menu(self):
        self.game = None
        self.game_frame.place_forget()
        self.return_button.place_forget()
        self.env.geometry('800x520')
        self.main_canvas.place(x=0, y=0)
        self.load_exemplary_game_button.place(x=50, y=50)
        self.load_game_button.place(x=50, y=100)

    def run_game(self):
        self.main_menu()
        self.env.mainloop()


class Board:
    def __init__(self, env, game_, mode):
        self.env = env
        self.game = game_
        self.board = None
        self.description = None
        self.drawing_board()
        self.pieces = self.game.pieces
        self.counter = 0
        self.game_desc_window = Canvas(self.env, width=450, height=350, bg='#FFF9BC')
        self.game_desc_window.place(x=975, y=250)
        self.row = 1
        self.mode = mode
        if self.mode == '1':
            self.game_description()
            self.display()
        else:
            self.display_two_players_game()

    def set_counter(self, event, num):
        self.counter = num + 2
        self.temp_situation()
        self.board.focus_set()

    def game_description(self):
        move_number = 1
        row = 1
        for i in range(0, len(self.game.game_moves)):
            if i % 8 == 0:
                if i != 0:
                    row += 1
            if i % 2 == 0:
                if i == 0:
                    self.game_desc_window.create_text(10, row * 20, text=f'{move_number}.', fill='black',
                                                      font=('Arial bold', 12), anchor=W,
                                                      tag='move_nr{}'.format(move_number))
                    move_number += 1
                else:
                    if i % 8 != 0:
                        x = self.game_desc_window.bbox(self.game_desc_window.find_withtag(f'move{i - 1}'))[2]
                    else:
                        x = 5
                    self.game_desc_window.create_text(x + 5, row * 20, text=f'{move_number}.', fill='black',
                                                      font=('Arial bold', 12), anchor=W,
                                                      tag='move_nr{}'.format(move_number))
                    move_number += 1
                    pass
                x = self.game_desc_window.bbox(self.game_desc_window.find_withtag(f'move_nr{move_number - 1}'))[2]
                self.game_desc_window.create_text(x + 5, row * 20, text=f'{self.game.game_moves[i]}', fill='black',
                                                  font=('Arial bold', 12), anchor=W, tag='move{}'.format(i))
            else:

                x = self.game_desc_window.bbox(self.game_desc_window.find_withtag(f'move{i - 1}'))[2]
                self.game_desc_window.create_text(x + 5, row * 20, text=f'{self.game.game_moves[i]}', fill='black',
                                                  font=('Arial bold', 12), anchor=W, tag='move{}'.format(i))

            self.game_desc_window.tag_bind('move{}'.format(i), '<1>', lambda event, i=i: self.set_counter(event, i))

    def drawing_board(self):
        self.description = Canvas(self.env, bg='black', width=900, height=900)
        self.description.place(x=50, y=50)
        self.board = Canvas(self.env, bg='#e68a00', width=800, height=800)
        self.board.place(x=100, y=100)

        # create fields

        def create_field(color, x_start, y_start):
            self.board.create_rectangle(x_start, y_start, x_start + 100, y_start + 100, fill=color, outline='')

        for x in range(0, 4):
            for y in range(0, 8):
                if y % 2 == 0:
                    create_field('#ffd699', 200 * x, 100 * y)
                    # self.board.create_text((200 * x) + 25, 100 * y + 25, text=str(((7 - y) * 8 + x * 2) + 1))
                else:
                    create_field('#ffd699', (200 * x) + 100, 100 * y)
                    # self.board.create_text((200 * x) + 125, 100 * y + 25, text=str((7 - y) * 8 + (x + 1) * 2))

        alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')

        def create_line_description(text, color, size, x_place, y_place):
            self.description.create_text(x_place, y_place, text=text, fill=color, font=str(size))

        for i in range(1, 9):
            create_line_description(alphabet[i - 1], 'white', 20, 100 * i + 10, 25)
            create_line_description(alphabet[i - 1], 'white', 20, 100 * i + 10, 875)

        for i in range(1, 9)[::-1]:
            create_line_description(str(i), 'white', 20, 25, 910 - 100 * i)
            create_line_description(str(i), 'white', 20, 875, 910 - 100 * i)

    def decode_position_number(self, position_number):
        text = ''
        if position_number % 8 != 0:
            text += alphabet2[position_number % 8 - 1]
            text += str(position_number // 8 + 1)
        else:
            text += alphabet2[7]
            text += str(position_number // 8)
        return text

    def change_field_description_to_number(self, field_description):
        number = (alphabet2.index(field_description[0]) + 1) + (int(field_description[1]) - 1) * 8
        return number

    def move_piece(self, piece_to_move, new_position, piece_index):
        field = self.board.find_withtag('field')
        old_field = self.board.find_withtag('old_field')
        if old_field:
            self.board.delete(old_field[0])
        if field:
            self.board.delete(field[0])
        text = self.decode_position_number(piece_to_move)
        text_2 = self.decode_position_number(new_position)
        tags = self.board.gettags(self.board.find_withtag(text)[0])
        try:
            tags_2 = self.board.gettags(self.board.find_withtag(text_2)[0])
            self.board.delete(self.board.find_withtag(text_2)[0])
        except IndexError:
            pass
        self.board.delete(self.board.find_withtag(text)[0])
        piece = self.pieces[piece_index]
        piece_image = piece.representation()
        piece_old_x = (piece_to_move % 8 - 1) * 100 + 50 if piece_to_move % 8 != 0 else 750
        piece_old_y = 800 - (piece_to_move // 8) * 100 - 50 if piece_to_move % 8 != 0 else 750 - (
                piece_to_move // 8 - 1) * 100
        piece.new_position(new_position)
        piece_x = (piece.position % 8 - 1) * 100 + 50 if piece.position % 8 != 0 else 750
        piece_y = 800 - (piece.position // 8) * 100 - 50 if piece.position % 8 != 0 else 750 - (
                piece.position // 8 - 1) * 100
        self.board.create_rectangle(piece_x - 50, piece_y - 50, piece_x + 50, piece_y + 50, fill='#EEC134', tag='field',
                                    outline='')
        self.board.create_rectangle(piece_old_x - 50, piece_old_y - 50, piece_old_x + 50, piece_old_y + 50,
                                    fill='#D9AF2D', tag='old_field', outline='')
        self.board.create_image(piece_x, piece_y, image=piece_image,
                                tags=(f'{piece.piece_notation_position()}', f'{self.pieces.index(piece)}', 'piece'))

    def left_click(self, event):
        self.piece_move()

    def right_click(self, event):
        self.temp_situation()

    def piece_move(self):
        current_move = self.game_desc_window.find_withtag('current_move')
        if current_move:
            self.game_desc_window.delete(current_move)
        field_check = self.board.find_withtag('field_check')
        try:
            desc = self.game_desc_window.find_withtag('move{}'.format(self.counter))
            self.game_desc_window.create_rectangle(self.game_desc_window.bbox(desc), fill='#E9967A', tag='current_move',
                                                   outline='')
            self.game_desc_window.tag_raise(desc)

        except IndexError:
            pass
        if field_check:
            self.board.delete(field_check[0])

        end_condition = self.board.find_withtag('game_finished')
        if end_condition:
            self.board.delete(end_condition[0])
        if self.game.game_moves[self.counter] == 'O-O':
            a, b, c, d, e, f = self.game.move(self.counter)
            self.move_piece(a, b, c)
            self.move_piece(d, e, f)
        elif self.game.game_moves[self.counter] in ('1-0', '0-1', '1/2-1/2'):
            if not end_condition:
                if self.game.game_moves[self.counter] == '1-0':
                    self.board.create_text(400, 400, fill='#CBCBCB', font=('Verdana bold', 66), text='White won!',
                                           tag='game_finished')
                elif self.game.game_moves[self.counter] == '0-1':
                    self.board.create_text(400, 400, fill='#363636', font=('Verdana bold', 66), text='Black won!',
                                           tag='game_finished')
                else:
                    self.board.create_text(400, 400, fill='#818181', font=('Verdana bold', 66), text='DRAW!',
                                           tag='game_finished')
        else:
            a, b, c = self.game.move(self.counter)
            self.move_piece(a, b, c)
            if self.game.game_moves[self.counter][-1] in ('+', '#'):
                color = 'black' if self.counter % 2 == 0 else 'white'
                for piece in self.pieces:
                    if piece.color == color and piece.piece_type == 'king':
                        king_position = self.decode_position_number(piece.position)
                        piece_x = (piece.position % 8 - 1) * 100 + 50 if piece.position % 8 != 0 else 750
                        piece_y = 800 - (piece.position // 8) * 100 - 50 if piece.position % 8 != 0 else 750 - (
                                piece.position // 8 - 1) * 100
                        fill = '#FF8269' if self.game.game_moves[self.counter][-1] == '+' else '#FF2D03'
                        self.board.create_rectangle(piece_x - 50, piece_y - 50, piece_x + 50, piece_y + 50,
                                                    fill=fill, tag='field_check', outline='')
                        self.board.lift(self.board.find_withtag(king_position)[0])
        self.counter += 1
        if self.counter == len(self.game.game_moves):
            self.counter = len(self.game.game_moves) - 1

        self.board.focus_set()

    def temp_situation(self):
        move_number = self.counter - 1 if self.counter > 0 else 0
        self.counter = 0
        all_pieces = self.board.find_withtag('piece')
        for piece in all_pieces:
            self.board.delete(piece)
        self.game.reset()
        self.pieces = self.game.pieces
        for piece in self.pieces:
            piece_image = piece.representation()
            piece_x = (piece.position % 8 - 1) * 100 + 50 if piece.position % 8 != 0 else 750
            piece_y = 800 - (piece.position // 8) * 100 - 50 if piece.position % 8 != 0 else 750 - (
                    piece.position // 8 - 1) * 100
            self.board.create_image(piece_x, piece_y, image=piece_image,
                                    tags=(
                                        f'{piece.piece_notation_position()}', f'{self.pieces.index(piece)}', 'piece'))
        for _ in range(0, move_number):
            self.piece_move()

        self.board.focus_set()

    def display(self):
        for piece in self.pieces:
            piece_image = piece.representation()
            piece_x = (piece.position % 8 - 1) * 100 + 50 if piece.position % 8 != 0 else 750
            piece_y = 800 - (piece.position // 8) * 100 - 50 if piece.position % 8 != 0 else 750 - (
                    piece.position // 8 - 1) * 100
            self.board.create_image(piece_x, piece_y, image=piece_image,
                                    tags=(f'{piece.piece_notation_position()}', f'{self.pieces.index(piece)}', 'piece'))

        self.board.focus_set()

        self.board.bind('<1>', self.left_click)
        self.board.bind('<3>', self.right_click)
        self.board.bind('<Right>', self.left_click)
        self.board.bind('<Left>', self.right_click)
        self.env.mainloop()

    def quit(self):
        self.env.quit()

    def display_two_players_game(self):
        for piece in self.pieces:
            piece_image = piece.representation()
            piece_x = (piece.position % 8 - 1) * 100 + 50 if piece.position % 8 != 0 else 750
            piece_y = 800 - (piece.position // 8) * 100 - 50 if piece.position % 8 != 0 else 750 - (
                    piece.position // 8 - 1) * 100
            self.board.create_image(piece_x, piece_y, image=piece_image,
                                    tags=(f'{piece.piece_notation_position()}', f'{self.pieces.index(piece)}', 'piece'))

        self.board.bind('<1>', self.pick_a_piece)
        self.board.bind('<B1-Motion>', self.piece_move_game)
        self.board.bind('<ButtonRelease-1>', self.piece_new_place)

    def pick_a_piece(self, event):
        x = event.x
        y = event.y
        pieces = self.board.find_withtag('piece')
        picked_piece = self.board.find_closest(x, y)[0]
        points = self.board.find_withtag('green_point')
        red_points = self.board.find_withtag('red_point')
        if points:
            for point in points:
                self.board.delete(point)
        if red_points:
            for point in red_points:
                self.board.delete(point)
        if picked_piece in pieces:
            self.board.tag_raise(picked_piece)
            tags = self.board.itemcget(picked_piece, 'tags')
            piece_possible_moves = self.pieces[int(tags.split()[1])].possible_moves
            piece_protected_moves = self.pieces[int(tags.split()[1])].protected_moves
            for num in piece_possible_moves:
                x_coord = ((num % 8) - 1) * 100 + 40 if num % 8 != 0 else 740
                y_coord = 740 - (num // 8) * 100 if num % 8 != 0 else 740 - ((num // 8) - 1) * 100
                self.board.create_oval(x_coord, y_coord, x_coord + 20, y_coord + 20, fill='green', tag='green_point')
            for num in piece_protected_moves:
                x_coord = ((num % 8) - 1) * 100 + 40 if num % 8 != 0 else 740
                y_coord = 740 - (num // 8) * 100 if num % 8 != 0 else 740 - ((num // 8) - 1) * 100
                self.board.create_oval(x_coord, y_coord, x_coord + 20, y_coord + 20, fill='red', tag='red_point')
            return picked_piece

    def piece_move_game(self, event):
        piece = self.pick_a_piece(event)
        self.board.tag_raise(piece)
        self.board.coords(piece, event.x, event.y)
        field_nr = 0
        field_x = event.x // 100
        field_y = (800 - event.y) // 100
        field_nr = field_x + 1 + (field_y * 8)
        return field_nr

    def piece_new_place(self, event):
        moved_piece = self.pick_a_piece(event)
        print(moved_piece)
        piece_tags = self.board.itemcget(moved_piece, 'tags')
        old_field = self.change_field_description_to_number(piece_tags.split()[0])
        new_field = self.piece_move_game(event)
        x_coord = ((new_field % 8) - 1) * 100 + 50 if new_field % 8 != 0 else 750
        y_coord = 750 - (new_field // 8) * 100 if new_field % 8 != 0 else 750 - ((new_field // 8) - 1) * 100
        self.board.coords(moved_piece, x_coord, y_coord)
        self.game.board.chess_piece_move(self.game.board.find_piece_by_position(old_field), new_field)


'''board = Board(Tk())
board.display()'''

game = GameMenu(Tk())
