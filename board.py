from tkinter import *
from PIL import Image, ImageTk


class Piece:
    def __init__(self, name):
        self.name = name
        self.image = ImageTk.PhotoImage(Image.open("pieces/{}.png".format(name)))
        self.position = None

    def representation(self):
        return self.image


class Board:
    def __init__(self, env):
        self.env = env
        self.env.geometry('1000x1000')
        self.env.configure(bg='black')
        self.board = None
        self.description = None
        self.white_king = Piece('white_king')
        self.drawing_board()
        self.piece_move()
        self.obraz = None

    def drawing_board(self):
        self.description = Canvas(self.env, bg='black', width=900, height=900)
        self.description.place(x=50, y=50)
        self.board = Canvas(self.env, bg='#e68a00', width=800, height=800)
        self.board.place(x=100, y=100)

        # create fields

        def create_field(color, x_start, y_start):
            self.board.create_rectangle(x_start, y_start, x_start + 100, y_start + 100, fill=color)

        for x in range(0, 4):
            for y in range(0, 8):
                if y % 2 == 0:
                    create_field('#ffd699', 200 * x, 100 * y)
                else:
                    create_field('#ffd699', (200 * x) + 100, 100 * y)

        alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')

        def create_line_description(text, color, size, x_place, y_place):
            self.description.create_text(x_place, y_place, text=text, fill=color, font=str(size))

        for i in range(1, 9):
            create_line_description(alphabet[i - 1], 'white', 20, 100 * i + 10, 25)
            create_line_description(alphabet[i - 1], 'white', 20, 100 * i + 10, 875)

        for i in range(1, 9)[::-1]:
            create_line_description(str(i), 'white', 20, 25, 910 - 100 * i)
            create_line_description(str(i), 'white', 20, 875, 910 - 100 * i)

    def piece_move(self):

        self.obraz = self.board.create_image(50, 50, image=self.white_king.representation(), tag='wK')

    def move(self, event):
        self.board.move('wK', 10, 10)

    def display(self):
        self.board.bind('<1>', self.move)
        self.env.mainloop()



board = Board(Tk())
board.display()

