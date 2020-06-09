from tkinter import *
from PIL import Image, ImageTk
from game import ChessPiece, NewGame

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
        self.load_exemplary_game = None
        self.load_game_button = None
        self.return_button = None
        self.game = None
        self.game_board = None
        self.game_frame = None
        self.run_game()

    def main_menu(self):
        self.env.geometry('800x520')
        self.env.configure(bg='black')
        self.main_canvas = Canvas(self.env, width=800, height=520)
        self.main_canvas.place(x=0, y=0)
        self.main_canvas.create_image(400, 260, image=self.bg_image)
        self.load_exemplary_game = Button(self.env, text='Load Exemplary', command=self.load_game)
        self.load_exemplary_game.place(x=100, y=100)
        self.load_game_button = Button(self.env, text='Paste Game Description')
        self.load_game_button.place(x=300, y=100)

    def load_game(self):
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
        self.main_canvas.place_forget()
        self.load_exemplary_game.place_forget()
        self.load_game_button.place_forget()
        self.env.geometry('1550x1000')
        self.env.configure(bg='black')
        self.return_button = Button(self.env, text='X', command=self.return_to_menu)
        self.return_button.place(x=1510, y=25)
        self.game_frame = Frame(self.env, width=1500, height=1000, bg='black')
        self.game_frame.place(x=0, y=0)
        self.game_board = Board(self.game_frame, self.game)

    def return_to_menu(self):
        self.game_frame.place_forget()
        self.return_button.place_forget()
        self.env.geometry('800x520')
        self.main_canvas.place(x=0, y=0)
        self.load_exemplary_game.place(x=100, y=100)
        self.load_game_button.place(x=300, y=100)

    def run_game(self):
        self.main_menu()
        self.env.mainloop()

class Board:
    def __init__(self, env, game_):
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
        self.game_description()
        self.display()

    def set_counter(self, event, num):
        self.counter = num + 2
        self.temp_situation(event)

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

    def piece_move(self, event):
        current_move = self.game_desc_window.find_withtag('current_move')
        if current_move:
            self.game_desc_window.delete(current_move)
        desc = self.game_desc_window.find_withtag('move{}'.format(self.counter))
        self.game_desc_window.create_rectangle(self.game_desc_window.bbox(desc), fill='#E9967A', tag='current_move',
                                               outline='')
        self.game_desc_window.tag_raise(desc)
        field_check = self.board.find_withtag('field_check')
        if field_check:
            self.board.delete(field_check[0])

        if self.game.game_moves[self.counter] == 'O-O':
            a, b, c, d, e, f = self.game.move(self.counter)
            self.move_piece(a, b, c)
            self.move_piece(d, e, f)
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

    def temp_situation(self, event):
        move_number = self.counter - 1
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
            self.piece_move(event)

    def display(self):
        for piece in self.pieces:
            piece_image = piece.representation()
            piece_x = (piece.position % 8 - 1) * 100 + 50 if piece.position % 8 != 0 else 750
            piece_y = 800 - (piece.position // 8) * 100 - 50 if piece.position % 8 != 0 else 750 - (
                    piece.position // 8 - 1) * 100
            self.board.create_image(piece_x, piece_y, image=piece_image,
                                    tags=(f'{piece.piece_notation_position()}', f'{self.pieces.index(piece)}', 'piece'))
        self.board.bind('<1>', self.piece_move)
        self.board.bind('<3>', self.temp_situation)
        self.env.mainloop()

    def quit(self):
        self.env.quit()


'''board = Board(Tk())
board.display()'''

game = GameMenu(Tk())
