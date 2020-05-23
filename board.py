from tkinter import *


class Board:
    def __init__(self, env):
        self.env = env
        self.env.geometry('1000x1000')
        self.env.configure(bg='black')
        self.board = None
        self.drawing_board()

    def drawing_board(self):
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


    def display(self):
        self.env.mainloop()


board = Board(Tk())
board.display()
