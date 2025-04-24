import tkinter as tk
import time as t
class sudoko_ai:
    def __init__(self):
        self.board=None

    def get_board(self,entries):
        """
        To get the board from the class gui of the game
        """
        board= [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = entries[i][j].get()
                if value.isdigit():
                    board[i][j]=int(value)
        return board

    def is_valid_uint(self,unit):
        nums=[x for x in unit if x != 0]
        return len(nums) == len(set(nums))

    def is_valid_board(self,board):
        # check_unit=is_valid_uint()
        """
        to check if the board is valid or not
        """
        for row in board:
            if not self.is_valid_uint(row):
                return False
        
        for col in zip(*board):
            if not self.is_valid_uint(col):
                return False

        for i in range(0,9,3):
            for j in range(0,9,3):
                if not self.is_valid_uint([board[r][c] for r in range(i, i+3) for c in range(j, j+3)]):
                    return False

        return True

    def solve_game(self,entries):
        """
        to get the the board from get board 
        ,then solve the puzzle the
        ,then print the board
        """
        start_time=t.time()
        self.board=self.get_board(entries)
        if not self.is_valid_board(self.board):
            print( "Invalid Sudoku Puzzle!")
            return
        if self.solve_csp(self.board):
            end_time=t.time()
            print(f"The excution time is {end_time - start_time}")
            self.display_the_solution(entries,self.board)
            print("the game can be solved ")
        else:
            print("No solution exists for the given Sudoku!")

    def display_the_solution(self,entries,board):
        """
        to display the final solution in the gui board 
        """
        # for i in range(9):
        #     for j
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(board[i][j]))


    def solve_csp(self,board):
        """
        To solve sudoko using backtracking algo and arc consistency
        """
        variables = {(row, col): set(range(1, 10)) for row in range(9) for col in range(9) if board[row][col] == 0}
        for row in range(9):
            for col in range(9):
                if board[row][col]!=0:
                    self.arc_consistency((row,col),board[row][col],variables)

        return self.backTrack(board,variables)

    def arc_consistency(self,cell,value,variable):
        """
        Applying arc consistency to reduce the domain of  connected cells
        """
        row,col=cell
        # row checker
        for r in range(9):
            if (r,col) in variable and value in variable[(r,col)]:
                variable[(r,col)].remove(value)
        
        for c in range(9):
            if (row,c) in variable and value in variable[(row,c)]:
                variable[(row,c)].remove(value)

        row_start, col_start= 3*(row//3) ,3*(col//3) 

        for r in range(row_start,row_start+3):
            for c in range(col_start,col_start+3):
                if (r,c) in variable and value in variable [(r,c)]:
                    variable[(r,c)].remove(value)

    def backTrack(self,board,variables):
        """
        Perform back tracking to solve soduko problem
        """

        if not variables:
            return True

        cell = min(variables, key=lambda x: len(variables[x]))
        values = list(variables[cell])
        row,col=cell

        for v in values:
            board[row][col]=v
            new_variables = {k: v.copy() for k, v in variables.items() if k != cell}
            self.arc_consistency(cell,v,new_variables)
            self.print_tree(new_variables)

            if self.backTrack(board,new_variables):
                return True
            board[row][col]=0

        return False

    def print_tree(self,domain):
        print("The tree of the arc consistency")
        # for i in range(9):
        #     for j in range(9):
        #         print(f"Cell {(i,j)} : {entries}")
        for cell,domain in (domain.items()):
            print(f"Cell {cell} : {domain}")
        print("_________________________________________________")
