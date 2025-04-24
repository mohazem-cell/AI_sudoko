import tkinter as tk
from tkinter import messagebox
import sudoko_ai as s_ai
from sudoku import Sudoku # type: ignore

class Sudokuu:
    def __init__(self):
        self.window1 = tk.Tk()
        self.center_window(self.window1, 700, 600)
        self.window1.title("Sudoku")
        self.window1.configure(bg="#FFE1FF")

        self.flag = 0
        self.board = None

        self.label1 = tk.Label(
            self.window1, 
            text="Welcome! Please Choose mode", 
            font=('Ink Free', 35, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF"
        )
        self.label1.pack(pady=40)

        self.mode_1_button = tk.Button(
            self.window1,
            width= 15, 
            text="Mode 1", 
            font=('Ink Free', 30, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF",
            command=self.mode_1
        )
        self.mode_1_button.pack(pady=(60,20))

        self.mode_2_button = tk.Button(
            self.window1,
            width= 15, 
            text="Mode 2", 
            font=('Ink Free', 30, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF",
            command=self.mode_2
        )
        self.mode_2_button.pack(pady=40)

        self.window1.mainloop()
    
    def mode_1(self):
        self.window2 = tk.Tk()
        self.center_window(self.window2, 700, 600)
        self.window2.title("Sudoku")
        self.window2.configure(bg="#FFE1FF")

        self.flag = 1

        self.label2 = tk.Label(
            self.window2, 
            text="Please Choose Difficulty", 
            font=('Ink Free', 35, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF"
        )
        self.label2.pack(pady=40)

        self.easy = tk.Button(
            self.window2,
            width= 15, 
            text="Easy", 
            font=('Ink Free', 30, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF",
            command=lambda: self.set_values(0.2)
        )
        self.easy.pack(pady=(60,20))

        self.medium  = tk.Button(
            self.window2,
            width= 15, 
            text="Medium", 
            font=('Ink Free', 30, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF",
            command=lambda: self.set_values(0.5)
        )
        self.medium.pack(pady=(20,20))

        self.Hard  = tk.Button(
            self.window2,
            width= 15, 
            text="Hard", 
            font=('Ink Free', 30, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF",
            command=lambda: self.set_values(0.8)
        )
        self.Hard.pack(pady=(20,20))

        self.window2.mainloop()

    def set_values(self, value):
        puzzle = Sudoku(3).difficulty(value)
        self.puzzle_board = puzzle.board
        
        self.window2.destroy()
        self.mode_2()

    def mode_2(self):
        self.window = tk.Tk()
        self.center_window(self.window, 900, 800)
        self.window.title("Sudoku")
        self.window.configure(bg="#FFE1FF")

        self.label = tk.Label(
            self.window, 
            text="Welcome! Please enter the initial state", 
            font = ('Ink Free', 35, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF"
        )
        self.label.pack(pady=20)

        self.entries_frame = tk.Frame(self.window, bg="#FFE1FF")
        self.entries_frame.pack(pady=(15,0))

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.solver= s_ai.sudoko_ai()

        frame_ = tk.Frame(self.window )
        frame_.pack(pady=5)
        frame_.config(bg="#FFE1FF")

        self.submit_button = tk.Button(
            frame_, 
            text="Submit", 
            font = ('Ink Free', 30, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF",
            command=self.solve_puzzle
        ).grid(row=0, column=0, padx=30, pady=2)

        self.check_button = tk.Button(
            frame_, 
            text="Check", 
            font = ('Ink Free', 30, 'bold'), 
            bg="#FFE1FF", 
            fg="#7E60BF",
            command=self.chech_solution
        ).grid(row=0, column=1, padx=30, pady=2)

        # s_ai= new s_ai()
        self.window.mainloop()

    def chech_solution(self):
        state = [[0 for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value != "":
                    state[i][j] = int(value)
                else:
                    state[i][j] = None
        
        self.solver.solve_game(self.entries)

        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                value = state[i][j]
                if value is not None:
                    self.entries[i][j].insert(0, str(value))
                else:
                    self.entries[i][j].delete(0, tk.END)
        
    def solve_puzzle(self):
        """
        pass the entries to ai agent to solve the puzzle
        """
        self.solver.solve_game(self.entries)
        # self.solver.print_tree(self.entries)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                padx = 20 if (j+1) % 3 == 0 and j != 0 else 5
                pady = 20 if (i+1) % 3 == 0 and i != 0 else 5

                entry = tk.Entry(
                    self.entries_frame,
                    width=3,
                    font=('Ink Free', 27, 'bold'),
                    justify='center',
                    bg="#FFE1FF",
                    fg="#7E60BF"
                )
                entry.grid(row=i, column=j, padx=(5, padx), pady=(5, pady))
                self.entries[i][j] = entry

                if self.flag == 1:
                    value = self.puzzle_board[i][j]
                    if value is not None:
                        self.entries[i][j].insert(0, str(value))
                    else:
                        self.entries[i][j].delete(0, tk.END)

    def get_initial_state(self):
        state = ""

        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value != "":
                    state += value
                else:
                    state += '0'
        
        print(state)

GUI = Sudokuu()
