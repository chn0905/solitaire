from solver import *
from tkinter import Tk, Frame, Canvas, Button, LEFT
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pickle

X_LIM, Y_LIM = 4, 4
SIZE = 100

class App:
    def __init__(self, master):
        self.master = master
        self.marked = []
        self.pieces = []
        self.texts  = []
        self.canvas = Canvas(self.master, width=X_LIM*SIZE, height=Y_LIM*SIZE)
        self.frame  = Frame(self.master)
        self.button1= Button(self.frame, text="Solve", command=self.solve)
        self.button2= Button(self.frame, text="Clear", command=self.clear)
        self.button3= Button(self.frame, text="Save", command=self.save)
        self.button4= Button(self.frame, text="Load", command=self.load)

        self.master.title("Solitaire Chess Solver")
        self.master.bind("<Key>", self.key)
        self._draw_board()
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.pack()
        self.frame.pack()
        self.button1.pack(side=LEFT)
        self.button2.pack(side=LEFT)
        self.button3.pack(side=LEFT)
        self.button4.pack(side=LEFT)
        
    def _draw_board(self):
        fill = "blue","white"
        for x in range(X_LIM):
            for y in range(Y_LIM):
                self.canvas.create_rectangle(SIZE*x, SIZE*y, SIZE*(x+1), SIZE*(y+1), fill=fill[(x+y)%2])

    def _add_piece(self, name, pos):
        self.pieces.append((name, pos))
        self.texts.append((pos, self.canvas.create_text(SIZE*pos[0] + SIZE//2, SIZE*((Y_LIM-1)-pos[1]) + SIZE//2, font=("Courier", SIZE//5), text=name)))

    def _remove_piece(self, pos):
        for piece in self.pieces:
            if pos == piece[1]:
                self.pieces.remove(piece)
        for text in self.texts:
            if pos == text[0]:
                self.texts.remove(text)
                self.canvas.delete(text[1])


    def clear(self):
        self.pieces = []
        for _, text_id in self.texts:
            self.canvas.delete(text_id)

    def save(self):
        fname = asksaveasfilename(filetypes=(("pickle files", "*.pkl"), ("All files", "*.*") ))
        if fname:
            with open(fname, "wb") as f:
                pickle.dump(self.pieces, f)

    def load(self):
        fname = askopenfilename(filetypes=(("pickle files", "*.pkl"), ("All files", "*.*") ))
        if fname:
            self.clear()
            with open(fname, "rb") as f:
                for piece in pickle.load(f):
                    self._add_piece(*piece)

    def clicked(self, event):
        self.marked = [event.x//SIZE, (Y_LIM-1) - event.y//SIZE]

    def key(self, event):
        m = tuple(self.marked)
        if not m: return
        name = event.char.upper() 
        if name in ("K", "Q", "B", "R", "H", "P"):
            if m not in [piece[1] for piece in self.pieces]:
                self._add_piece(name, m)
        elif name == "D":
            self._remove_piece(m)

    def solve(self):
        print("="*20)
        print("Finding Solution for ...")
        for piece in self.pieces:
            print(piece)
        print("Total {} Pieces".format(len(self.pieces)))
        print()
        game = Solver( tuple(self.pieces) )
        if game.findSolution():
            print("[Solution]")
            for line in game.solution:
                print(line)
        else:
            print("No Solution")


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
