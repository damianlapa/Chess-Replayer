from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import websockets
import asyncio
import json
from game import ChessPiece, NewGame, TwoPlayersGame, ChessBoard
from database import load_game_from_database, save_game_to_database, update_game, return_all_games

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
        self.two_players_online_button = None
        self.save_button = None
        self.load_button = None
        self.all_database_games = None
        self.load_selected_game = None
        self.game_id = None
        self.server_connection = None
        self.ip_entry = None
        self.main_menu()

    def main_menu(self):
        self.env.geometry('800x520')
        self.env.configure(bg='black')
        self.main_canvas = Canvas(self.env, width=800, height=520)
        self.main_canvas.place(x=0, y=0)
        self.main_canvas.create_image(400, 260, image=self.bg_image)
        self.set_buttons()

    def set_buttons(self):
        self.env.geometry('800x520')
        self.env.configure(bg='black')
        self.main_canvas.place(x=0, y=0)
        if self.load_selected_game:
            self.load_selected_game.place_forget()
        if self.game_text_window:
            self.game_text_window.place_forget()
        if self.all_database_games:
            self.all_database_games.place_forget()
        self.load_exemplary_game_button = Button(self.env, text='Load Exemplary', command=self.load_exemplary_game)
        self.load_exemplary_game_button.place(x=50, y=50)
        self.load_game_button = Button(self.env, text='Paste Game Description', command=self.display_text_window)
        self.load_game_button.place(x=50, y=100)
        self.two_players_button = Button(self.env, text='2 Players Offline Game', command=self.two_players_game)
        self.two_players_button.place(x=50, y=150)
        self.two_players_online_button = Button(self.env, text='2 Players Online Game', command=self.set_ip_address)
        self.two_players_online_button.place(x=50, y=200)
        self.load_button = Button(self.env, text='Load game from database', command=self.load_database_game)
        self.load_button.place(x=50, y=250)

    def set_ip_address(self):
        self.server_connection = Frame(self.env, width=220, height=150, bg='black')
        self.server_connection.place(x=275, y=150)
        ip_text = Label(self.server_connection, text='Enter an IP server address:', bg='black', fg='white')
        ip_text.place(x=5, y=10)
        self.ip_entry = Entry(self.server_connection, width=25)
        self.ip_entry.place(x=5, y=55)
        self.ip_entry.insert(0, 'localhost')

        def get_an_address():
            try:
                async def ready():
                    uri = "ws://{}:8765".format(self.ip_entry.get())
                    async with websockets.connect(uri) as websocket:
                        await websocket.send('ready')
                        pass
                response = asyncio.get_event_loop().run_until_complete(ready())
                self.two_players_online_game(self.ip_entry.get())
            except Exception as e:
                print(e)
                statement = Label(self.server_connection, text='Connection Failed!', fg='red', bg='black')
                statement.place(x=44, y=122)
                self.server_connection.after(2000, statement.destroy)


        connect_button = Button(self.server_connection, text='CONNECT', command=get_an_address)
        connect_button.place(x=66, y=88)

    def load_database_game(self):
        database_game = StringVar(self.env)
        games = return_all_games()
        self.all_database_games = Combobox(self.env, textvariable=database_game, values=games, state='readonly',
                                           width=50)
        self.all_database_games.place(x=300, y=40)

        def get_value():
            self.game = NewGame(database_game.get())
            self.load_game()

        self.load_selected_game = Button(self.env, text='LOAD', command=get_value, bg='darkgreen', fg='white')
        self.load_selected_game.place(x=300, y=10)

    def two_players_game(self):
        self.main_canvas.place_forget()
        self.load_exemplary_game_button.place_forget()
        self.load_game_button.place_forget()
        self.env.geometry('1425x1000')
        self.env.configure(bg='black')
        self.return_button = Button(self.env, text='X', command=self.return_to_menu)
        self.return_button.place(x=1385, y=25)
        self.game_frame = Frame(self.env, width=1375, height=1000, bg='black')
        self.game_frame.place(x=0, y=0)
        self.save_button = Button(self.game_frame, text='SAVE', command=self.save)
        self.save_button.place(x=1165, y=625)
        self.game = Board(self.game_frame, TwoPlayersGame(), '2')

    def two_players_online_game(self, ip):
        self.main_canvas.place_forget()
        self.load_exemplary_game_button.place_forget()
        self.load_game_button.place_forget()
        self.env.geometry('1425x1000')
        self.env.configure(bg='black')
        self.return_button = Button(self.env, text='X', command=self.return_to_menu)
        self.return_button.place(x=1385, y=25)
        self.game_frame = Frame(self.env, width=1375, height=1000, bg='black')
        self.game_frame.place(x=0, y=0)
        self.save_button = Button(self.game_frame, text='SAVE', command=self.save)
        self.save_button.place(x=1165, y=625)
        self.game = OnlineBoard(self.game_frame, TwoPlayersGame(), '0', ip)

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
        test_2 = '1. e4 e5 2. d4 d5 3. exd5 exd4 4. Qe2+ Qe7 5. Nc3 Qxe2+ 6. Bxe2 dxc3 7. bxc3'
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
        # self.run_game()

    def return_to_menu(self):
        self.game = None
        self.game_frame.place_forget()
        self.return_button.place_forget()
        '''self.env.geometry('800x520')
        self.main_canvas.place(x=0, y=0)
        self.load_exemplary_game_button.place(x=50, y=50)
        self.load_game_button.place(x=50, y=100)'''
        self.set_buttons()
        self.game_id = None

    def run_game(self):
        self.load_game()

    def save(self):
        if not self.game_id:
            self.game_id = save_game_to_database(self.game.game.board.create_pgn())
            statement = Label(self.game_frame, text='GAME SAVED', fg='green', bg='black')
            statement.place(x=1175, y=625)
            self.game_frame.after(2000, statement.destroy)
        else:
            update_game(self.game_id, self.game.game.board.create_pgn())
            statement = Label(self.game_frame, text='GAME UPDATED', fg='green', bg='black')
            statement.place(x=1175, y=625)
            self.game_frame.after(2000, statement.destroy)


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
        self.promotion_board = Canvas(self.env, width=400, height=100, bg='grey')
        self.game_desc_window.place(x=975, y=250)
        self.row = 1
        self.mode = mode
        self.moved_piece_tag = None
        self.tour = 0
        self.move_counter = 0
        self.check = False
        self.possible_promotions = []
        self.promotion_data = None

        if self.mode == '1':
            self.game_description()
            self.display()
        elif self.mode == '2':
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
        if self.game.game_moves[self.counter] == 'O-O' or self.game.game_moves[self.counter] == 'O-O-O':
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
        # self.env.mainloop()

    def quit(self):
        self.env.quit()

    def display_two_players_game(self):
        for piece in self.pieces:
            piece_image = piece.representation()
            piece_x = (piece.position % 8 - 1) * 100 + 50 if piece.position % 8 != 0 else 750
            piece_y = 800 - (piece.position // 8) * 100 - 50 if piece.position % 8 != 0 else 750 - (
                    piece.position // 8 - 1) * 100
            self.board.create_image(piece_x, piece_y, image=piece_image,
                                    tags=(f'{piece.piece_notation_position()}', f'{piece.color}', f'{piece.piece_type}',
                                          'piece'))

        # self.online_move_listener()

        self.board.bind('<1>', self.pick_a_piece)
        self.board.bind('<B1-Motion>', self.piece_move_game)
        self.board.bind('<ButtonRelease-1>', self.piece_new_place)

    def create_coords(self, field):
        x_coord = ((field % 8) - 1) * 100 + 50 if field % 8 != 0 else 750
        y_coord = 750 - (field // 8) * 100 if field % 8 != 0 else 750 - ((field // 8) - 1) * 100
        return x_coord, y_coord

    def pick_a_piece(self, event):
        self.promotion_data = None
        picked_piece = None
        x = event.x
        y = event.y
        pieces = self.board.find_withtag('piece')
        black_pieces = self.board.find_withtag('black')
        white_pieces = self.board.find_withtag('white')
        if not self.moved_piece_tag:
            picked_piece = self.board.find_closest(x, y)[0]
        points = self.board.find_withtag('green_point')
        red_points = self.board.find_withtag('red_point')
        if points:
            for point in points:
                self.board.delete(point)
        if red_points:
            for point in red_points:
                self.board.delete(point)

        if self.tour % 2 == 0:
            choose_side = white_pieces
        else:
            choose_side = black_pieces
        if picked_piece:
            if picked_piece in choose_side:
                tags = self.board.itemcget(picked_piece, 'tags')
                picked_piece_object = self.game.board.find_piece_by_position(
                    self.change_field_description_to_number(tags.split()[0]))
                self.game.board.piece_current_moves(picked_piece_object)
                if picked_piece_object.piece_type == 'king':
                    self.game.board.king_castle_possibility(picked_piece_object)
                elif picked_piece_object.piece_type == 'pawn':
                    self.game.board.piece_current_moves(picked_piece_object)
                self.board.tag_raise(picked_piece)
                self.moved_piece_tag = tags.split()[0]
                field_number = self.change_field_description_to_number(self.moved_piece_tag)
                piece_possible_moves = self.game.board.find_piece_by_position(field_number).possible_moves
                piece_protected_moves = self.game.board.find_piece_by_position(field_number).protected_moves
                for num in piece_possible_moves:
                    x_coord = ((num % 8) - 1) * 100 + 40 if num % 8 != 0 else 740
                    y_coord = 740 - (num // 8) * 100 if num % 8 != 0 else 740 - ((num // 8) - 1) * 100
                    self.board.create_oval(x_coord, y_coord, x_coord + 20, y_coord + 20, fill='green',
                                           tag='green_point')
                '''for num in piece_protected_moves:
                    x_coord = ((num % 8) - 1) * 100 + 40 if num % 8 != 0 else 740
                    y_coord = 740 - (num // 8) * 100 if num % 8 != 0 else 740 - ((num // 8) - 1) * 100
                    self.board.create_oval(x_coord, y_coord, x_coord + 20, y_coord + 20, fill='red', tag='red_point')'''
                return self.moved_piece_tag

    def piece_move_game(self, event):
        piece = None
        if self.moved_piece_tag:
            piece = self.board.find_withtag(self.moved_piece_tag)
        if piece:
            self.board.tag_raise(piece)
            self.board.coords(piece, event.x, event.y)
            field_x = event.x // 100
            field_y = (800 - event.y) // 100
            field_nr = field_x + 1 + (field_y * 8)

            return field_nr

    def piece_new_place(self, event):
        castle_rook = None
        rook_new_field = 0
        rook_old_field = 0
        moved_piece_object = None
        old_field = None
        new_field = None


        def castle(king, rook, king_position, rook_position):
            if self.mode == '0':
                self.send_move_to_server(king.position, king_position, 'castle', self.tour)
                self.send_move_to_server(rook.position, rook_position, 'castle', self.tour)

            rook_old_field = rook_position
            king_coords = self.create_coords(king_position)
            rook_coords = self.create_coords(rook_position)
            king_on_board = self.board.find_withtag(self.decode_position_number(king.position))[0]
            rook_on_board = self.board.find_withtag(self.decode_position_number(rook.position))[0]

            self.game.board.castle(king, rook, king_position, rook_position)
            self.display_current_game_moves()

            self.board.coords(king_on_board, king_coords[0], king_coords[1])
            self.board.coords(rook_on_board, rook_coords[0], rook_coords[1])

            king_tags = self.board.itemcget(king_on_board, 'tags')
            king_old_tags = king_tags.split()
            king_new_field_description = self.decode_position_number(king_position)

            rook_tags = self.board.itemcget(rook_on_board, 'tags')
            rook_old_tags = rook_tags.split()
            rook_new_field_description = self.decode_position_number(rook_position)

            king_new_tags = king_new_field_description
            for i in range(1, len(king_old_tags)):
                king_new_tags += ' ' + king_old_tags[i]
            self.board.itemconfig(king_on_board, tags=king_new_tags)

            rook_new_tags = rook_new_field_description
            for i in range(1, len(rook_old_tags)):
                rook_new_tags += ' ' + rook_old_tags[i]
            self.board.itemconfig(rook_on_board, tags=rook_new_tags)

            self.moved_piece_tag = None
            self.tour += 1

        special_move = False
        promotion = False
        error = None
        moved_piece = None
        if self.moved_piece_tag:
            moved_piece = self.board.find_withtag(self.moved_piece_tag)
        if moved_piece:
            try:
                piece_tags = self.board.itemcget(moved_piece, 'tags')
                old_tags = piece_tags.split()
                old_field = self.change_field_description_to_number(old_tags[0])
                new_field = self.piece_move_game(event)

                moved_piece_object = self.game.board.find_piece_by_position(old_field)
                self.game.board.piece_current_moves(moved_piece_object)

            except IndexError:
                print('error')

            if moved_piece_object.piece_type == 'king':
                self.game.board.king_castle_possibility(moved_piece_object)
                if new_field in moved_piece_object.possible_moves:
                    if abs(old_field - new_field) == 2:
                        if new_field > old_field:
                            rook_field = new_field + 1
                            rook_new_field = new_field - 1
                        else:
                            rook_field = new_field - 2
                            rook_new_field = new_field + 1
                        castle_rook = self.game.board.find_piece_by_position(rook_field)
                        special_move = True

            if moved_piece_object.piece_type == 'pawn':
                if new_field in moved_piece_object.possible_moves:
                    if moved_piece_object.color == 'black':
                        if new_field in range(1, 9):
                            promotion = True
                    else:
                        if new_field in range(57, 65):
                            promotion = True

            # castle
            if special_move:
                castle(moved_piece_object, castle_rook, new_field, rook_new_field)



            else:
                # checking check threat ends
                check_end = True
                king_safety = True
                if self.check:
                    if old_field != new_field:
                        check_end = False
                        test_board = ChessBoard()
                        test_board.chess_pieces = self.game.board.copy_board()
                        piece = test_board.find_piece_by_position(old_field)
                        field_occupancy = test_board.find_piece_by_position(new_field)
                        if field_occupancy:
                            test_board.chess_piece_capture(piece, new_field)
                        else:
                            test_board.chess_piece_move(piece, new_field)
                        if not test_board.test_position()[1] and self.tour % 2 == 1:
                            check_end = True
                            self.check = None
                        elif not test_board.test_position()[0] and self.tour % 2 == 0:
                            check_end = True
                            self.check = None
                # checking if move do not undercover the king
                if king_safety:
                    if not old_field == new_field:
                        test_king_safety = ChessBoard()
                        test_king_safety.chess_pieces = self.game.board.copy_board()
                        piece = test_king_safety.find_piece_by_position(old_field)
                        field_occupancy = test_king_safety.find_piece_by_position(new_field)
                        if field_occupancy:
                            test_king_safety.chess_piece_capture(piece, new_field)
                        else:
                            test_king_safety.chess_piece_move(piece, new_field)
                        if test_king_safety.test_position()[0] and self.tour % 2 == 0:
                            king_safety = False
                        elif test_king_safety.test_position()[1] and self.tour % 2 == 1:
                            king_safety = False
                        test_king_safety = None

                if new_field and check_end and king_safety:
                    new_field_occupancy = self.game.board.find_piece_by_position(new_field)
                    old_field_piece = self.game.board.find_piece_by_position(old_field)
                    if new_field in old_field_piece.possible_moves:
                        new_coords = self.create_coords(new_field)
                        self.board.coords(moved_piece, new_coords[0], new_coords[1])
                        new_field_description = self.decode_position_number(new_field)
                        if new_field_occupancy:
                            if new_field_occupancy.color != old_field_piece.color:
                                self.board.delete(self.board.find_withtag(new_field_description)[0])
                                self.game.board.chess_piece_capture(self.game.board.find_piece_by_position(old_field),
                                                                    new_field)
                                if self.mode == '0':
                                    self.send_move_to_server(old_field, new_field, 'c', self.tour)
                                self.tour += 1
                            else:
                                old_field_coords = self.create_coords(old_field)
                                self.board.coords(moved_piece, old_field_coords[0], old_field_coords[1])
                                error = True
                        else:
                            self.game.board.chess_piece_move(self.game.board.find_piece_by_position(old_field),
                                                             new_field)
                            if self.mode == '0':
                                self.send_move_to_server(old_field, new_field, None, self.tour)
                            self.tour += 1
                        if not error:
                            new_tags = new_field_description
                            for i in range(1, len(old_tags)):
                                new_tags += ' ' + old_tags[i]
                            self.board.itemconfig(moved_piece, tags=new_tags)

                        if promotion:
                            self.promotion_board.place(x=300, y=400)
                            self.promotion_board_pick()

                            self.promotion_data = (new_field, moved_piece_object)

                        for piece in self.pieces:
                            self.game.board.piece_current_moves(piece)
                        self.moved_piece_tag = None

                        self.display_current_game_moves()

                    else:
                        old_coords = self.create_coords(old_field)
                        self.board.coords(moved_piece, old_coords[0], old_coords[1])
                        self.moved_piece_tag = None
                    points = self.board.find_withtag('green_point')
                    red_points = self.board.find_withtag('red_point')
                    if points:
                        for point in points:
                            self.board.delete(point)
                    if red_points:
                        for point in red_points:
                            self.board.delete(point)

                    if self.tour % 2 == 0:
                        if self.game.king_check('white'):
                            self.check = True
                    else:
                        if self.game.king_check('black'):
                            self.check = True

                else:
                    old_coords = self.create_coords(old_field)
                    self.board.coords(moved_piece, old_coords[0], old_coords[1])
                    self.moved_piece_tag = None
            points = self.board.find_withtag('green_point')
            if points:
                for point in points:
                    self.board.delete(point)

            print('#1', self.game.board.game_description)

    def promotion_board_pick(self):

        self.board.unbind('<1>')
        self.board.unbind('<B1-Motion>')
        self.board.unbind('<ButtonRelease-1>')

        if self.tour % 2 == 1:
            self.possible_promotions = [ChessPiece('queen'), ChessPiece('rook'), ChessPiece('bishop'),
                                        ChessPiece('knight')]
        else:
            self.possible_promotions = [ChessPiece('queen', None, 'black'), ChessPiece('rook', None, 'black'),
                                        ChessPiece('bishop', None, 'black'),
                                        ChessPiece('knight', None, 'black')]
        for i in range(0, len(self.possible_promotions)):
            self.promotion_board.create_image(50 + (80 * i), 50, image=self.possible_promotions[i].representation(),
                                              tags=(self.possible_promotions[i].piece_type, 'piece'))

        self.promotion_board.bind('<1>', self.pawn_promotion_board)

    def pawn_promotion_board(self, event):

        possibilities = self.promotion_board.find_withtag('piece')

        choice = self.promotion_board.find_closest(event.x, event.y)[0]

        if choice in possibilities:
            new_field = self.promotion_data[0]
            moved_piece_object = self.promotion_data[1]
            piece_type = self.promotion_board.itemcget(choice, 'tags').split()[0]

            self.board.delete(self.board.find_withtag(self.decode_position_number(new_field)))
            new_piece = self.game.board.pawn_promotion(moved_piece_object, new_field, piece_type)
            piece_image = new_piece.representation()
            piece_x = (new_piece.position % 8 - 1) * 100 + 50 if new_piece.position % 8 != 0 else 750
            piece_y = 800 - (
                    new_piece.position // 8) * 100 - 50 if new_piece.position % 8 != 0 else 750 - (
                    new_piece.position // 8 - 1) * 100
            self.board.create_image(piece_x, piece_y, image=piece_image,
                                    tags=(f'{new_piece.piece_notation_position()}',
                                          f'{new_piece.color}', f'{new_piece.piece_type}',
                                          'piece'))

            self.promotion_board.unbind('<1>')

            self.promotion_board.place_forget()

            self.board.bind('<1>', self.pick_a_piece)
            self.board.bind('<B1-Motion>', self.piece_move_game)
            self.board.bind('<ButtonRelease-1>', self.piece_new_place)

    def display_current_game_moves(self):
        try:
            previous = self.game_desc_window.find_withtag('move{}'.format(self.move_counter - 1))[0]
            if self.move_counter % 12 == 0:
                self.game_desc_window.create_text(10, 10 + self.move_counter // 12 * 20,
                                                  text='{}.'.format(self.move_counter // 3 + 1), anchor='w',
                                                  tags=('move{}'.format(self.move_counter), 'new_line'),
                                                  font=('Arial bold', 12))
                self.move_counter += 1
                previous = self.game_desc_window.find_withtag('move{}'.format(self.move_counter - 1))[0]
                previous_bbox = self.game_desc_window.bbox(previous)
                self.game_desc_window.create_text(previous_bbox[2] + 5, previous_bbox[1] + 9,
                                                  text=self.game.board.game_description[-1],
                                                  anchor='w', tag='move{}'.format(self.move_counter),
                                                  font=('Arial bold', 12))
                self.move_counter += 1
            elif self.move_counter % 3 == 0 or self.move_counter == 1:
                previous_coords = self.game_desc_window.bbox(previous)

                self.game_desc_window.create_text(previous_coords[2] + 5, previous_coords[1] + 9,
                                                  text='{}.'.format(self.move_counter // 3 + 1), anchor='w',
                                                  tag='move{}'.format(self.move_counter), font=('Arial bold', 12))
                self.move_counter += 1
                previous = self.game_desc_window.find_withtag('move{}'.format(self.move_counter - 1))[0]
                previous_coords = self.game_desc_window.bbox(previous)
                self.game_desc_window.create_text(previous_coords[2] + 5, previous_coords[1] + 9,
                                                  text=self.game.board.game_description[-1],
                                                  anchor='w', tag='move{}'.format(self.move_counter),
                                                  font=('Arial bold', 12))
                self.move_counter += 1
            else:
                previous = self.game_desc_window.find_withtag('move{}'.format(self.move_counter - 1))[0]
                previous_coords = self.game_desc_window.bbox(previous)
                self.game_desc_window.create_text(previous_coords[2] + 5, previous_coords[1] + 9,
                                                  text=self.game.board.game_description[-1],
                                                  anchor='w', tag='move{}'.format(self.move_counter),
                                                  font=('Arial bold', 12))
                self.move_counter += 1
        except IndexError:
            if self.move_counter % 2 == 0 or self.move_counter == 1:
                self.game_desc_window.create_text(10, 10,
                                                  text='{}.'.format(self.move_counter // 3 + 1), anchor='w',
                                                  tags=('move{}'.format(self.move_counter), 'new_line'),
                                                  font=('Arial bold', 12))
                self.move_counter += 1
            new_line = self.game_desc_window.find_withtag('new_line')[0]
            new_line_bbox = self.game_desc_window.bbox(new_line)
            self.game_desc_window.create_text(new_line_bbox[2] + 5, 10,
                                              text=self.game.board.game_description[-1],
                                              anchor='w', tag='move{}'.format(self.move_counter),
                                              font=('Arial bold', 12))
            self.move_counter += 1
        '''all_moves = self.game.board.game_description
        move_text = all_moves[-1]
        if move_text:
            if len(all_moves) % 2 == 1:
                text = str(len(all_moves) // 2 + 1) + '.'
                previous_move = self.game_desc_window.find_withtag('move_desc')
                if previous_move:
                    prev_coords = self.game_desc_window.bbox(previous_move[0])
                    self.game_desc_window.create_text(prev_coords[2], 10, text=text, font=('Arial bold', 12), anchor='w',
                                                      tag='move_desc'.format(str(len(all_moves) // 2 + 1)))
                    previous_move = self.game_desc_window.find_withtag('move_desc')
                    prev_coords = self.game_desc_window.bbox(previous_move[0])
                    self.game_desc_window.create_text(prev_coords[2] + 3, 10, text=move_text)
            else:
                self.game_desc_window.create_text(10, 10, text='1. ', font=('Arial bold', 12), anchor='w',
                                                  tag='move_desc')'''

        '''row = 0
        move_num = 1
        row_text = ''
        for i in range(0, len(self.game.board.game_description)):
            if i % 2 == 0:
                row_text += str(move_num) + '. '
                move_num += 1
            row_text += self.game.board.game_description[i] + ' '
            print(i)
            if (i + 1) % 8 == 0:
                self.game_desc_window.create_text(10, 10 + 10 * row, text=f'{row_text}', tag='game_desc',
                                                  font=('Arial bold', 12), anchor='w')
                row += 1
                row_text = '''''

class OnlineBoard(Board):
    def __init__(self, env, game_, mode, ip):
        super(OnlineBoard, self).__init__(env, game_, mode)
        self.online_game_data = []
        self.ip_address = ip
        self.display_two_players_game()

    def display_two_players_game(self):
        super(OnlineBoard, self).display_two_players_game()
        self.online_move_listener()

    def online_move_listener(self):
        def receive_data():
            async def send_move():
                uri = "ws://{}:8765".format(self.ip_address)
                async with websockets.connect(uri) as websocket:
                    await websocket.send('ready')
                    all_moves = await websocket.recv()
                    return all_moves

            all_moves_data = asyncio.get_event_loop().run_until_complete(send_move())
            return all_moves_data
        server_game_moves = json.loads(receive_data())
        for move in server_game_moves:
            old_field, new_field, move_type, tour = move
            if move not in self.online_game_data:
                self.tour += 1
                if move_type == 'c':
                    self.game.board.chess_piece_capture(self.game.board.find_piece_by_position(old_field), new_field)
                elif move_type == 'castle':
                    self.tour -= .5
                    self.game.board.chess_piece_move(self.game.board.find_piece_by_position(old_field), int(new_field))
                else:
                    self.game.board.chess_piece_move(self.game.board.find_piece_by_position(old_field), int(new_field))

                self.board.bind('<1>', self.pick_a_piece)
                self.board.bind('<B1-Motion>', self.piece_move_game)
                self.board.bind('<ButtonRelease-1>', self.piece_new_place)

                self.online_game_data.append(move)
                self.opponent_move(old_field, new_field, move_type)

        self.board.after(1000, self.online_move_listener)

    def send_move_to_server(self, old_position, new_position, extra_info=None, tour=0):
        async def send_move():
            uri = "ws://{}:8765".format(self.ip_address)
            async with websockets.connect(uri) as websocket:
                move = [old_position, new_position, extra_info, tour]
                self.online_game_data.append(move)
                move_json = json.dumps(move)
                await websocket.send(move_json)

        asyncio.get_event_loop().run_until_complete(send_move())

        self.board.unbind('<1>')
        self.board.unbind('<B1-Motion>')
        self.board.unbind('<ButtonRelease-1>')

    def opponent_move(self, old_field, new_field, move_type):
        moved_piece = self.board.find_withtag(self.decode_position_number(old_field))
        if moved_piece:
            try:
                if move_type:
                    self.board.delete(self.board.find_withtag(self.decode_position_number(new_field)))
                piece_tags = self.board.itemcget(moved_piece, 'tags')
                old_tags = piece_tags.split()
                old_field = self.change_field_description_to_number(old_tags[0])

                moved_piece_object = self.game.board.find_piece_by_position(new_field)
                self.game.board.piece_current_moves(moved_piece_object)
                new_coords = self.create_coords(new_field)
                self.board.coords(moved_piece, new_coords[0], new_coords[1])
                new_field_description = self.decode_position_number(new_field)

                new_tags = new_field_description
                for i in range(1, len(old_tags)):
                    new_tags += ' ' + old_tags[i]
                self.board.itemconfig(moved_piece, tags=new_tags)
                self.display_current_game_moves()

            except IndexError:
                print('error')


if __name__ == '__main__':
    env = Tk()
    game = GameMenu(env)
    env.mainloop()
