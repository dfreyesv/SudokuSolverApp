"""kivy modules needed for app"""
import time
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class MainGrid(GridLayout):
    """main grid 3x3"""

    values_board = [["_"] * 9 for _ in range(9)]
    grid = []
    id_cell = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 3
        padding_value = 20
        self.padding = [padding_value, padding_value, padding_value, padding_value]
        for _ in range(self.cols**2):
            small_grid_widget = GridLayout(
                cols=3, rows=3, spacing=[1.5, 1.5], padding=[2.5, 2.5, 2.5, 2.5]
            )
            small_grid_list = []

            cells = [
                NumberInput(text="", halign="center", font_size="15") for _ in range(9)
            ]
            for j, cell in enumerate(cells):
                main_grid_row = (self.id_cell // 3) * 3 + j // 3
                main_grid_col = (self.id_cell % 3) * 3 + j % 3
                self.values_board[main_grid_row][main_grid_col] = cell
                small_grid_widget.add_widget(cell)
                small_grid_list.append(cell)
            self.grid.append(small_grid_list)
            self.add_widget(small_grid_widget)
            self.id_cell += 1


class NumberInput(TextInput):
    """Cell Class"""

    id_widget_input = ""

    def insert_text(self, substring, from_undo=False):
        if substring in "0123456789" and len(self.text) == 0:
            s = substring
        else:
            s = ""
        return super().insert_text(s, from_undo=from_undo)


class MainScreen(BoxLayout):
    """Main Screen of app"""

    # board = [["_"]*9 for _ in range(9)]
    def solve_click(self):
        """what to do when solve is clicked"""
        puzzle = SolutionFinder()
        solved_board = MainGrid.values_board
        solved_board = puzzle.solution(solved_board)

    def clear_click(self):
        """what to do when clear is clicked"""
        print("clicked_clear")
        for i in range(9):
            for j in range(9):
                MainGrid.values_board[i][j].text = ""

    def get_input_texts(self):
        """Get the text stored in the input boxes"""
        input_texts = []
        for small_grid in self.ids.main_grid.children:
            for number_input in small_grid.children:
                input_texts.append(number_input.text)
        print(input_texts)
        return input_texts


class SolutionFinder:
    """Methods to find solution to puzzle"""

    def solution(self, board):
        """Method to test time"""
        start_time = time.time()

        # Solution of sudoku
        if not self.solve_sudoku(board):
            print("UNSOLVABLE!!")
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Print the result
        print(f"Script took {elapsed_time:.5f} seconds to execute.")

        return board

    def find_next_cell(self, board):
        """Finds best next cell to fill"""
        empty_cell_1 = None
        empty_cell_2 = None

        break_flag = False
        for i in range(0, 9):
            for j in range(0, 9):
                if board[i][j].text == "":
                    empty_cell_1 = [i, j]
                    break_flag = True
                    break
            if break_flag is True:
                break

        if empty_cell_1 is None:
            return None, None

        break_flag = False
        for j in range(0, 9):
            for i in range(0, 9):
                if board[i][j].text == "":
                    empty_cell_2 = [i, j]
                    break_flag = True
                    break
            if break_flag is True:
                break

        if empty_cell_1 == empty_cell_2:
            # print("same cell", empty_cell_1[0], empty_cell_1[1])
            # input()
            return empty_cell_1[0], empty_cell_1[1]

        empty_count_cell_row_1 = 0
        empty_count_cell_col_1 = 0

        empty_count_cell_row_2 = 0
        empty_count_cell_col_2 = 0

        for j in range(0, 9):
            if board[empty_cell_1[0]][j].text == "":
                empty_count_cell_row_1 += 1
        for i in range(0, 9):
            if board[i][empty_cell_1[1]].text == "":
                empty_count_cell_col_1 += 1

        for j in range(0, 9):
            if board[empty_cell_2[0]][j].text == "":
                empty_count_cell_row_2 += 1
        for i in range(0, 9):
            if board[i][empty_cell_2[1]].text == "":
                empty_count_cell_col_2 += 1

        if (
            empty_count_cell_row_1 == empty_count_cell_row_2
            and empty_count_cell_col_1 == empty_count_cell_col_2
        ):
            return empty_cell_1[0], empty_cell_1[1]

        if min(empty_count_cell_row_1, empty_count_cell_col_1) == min(
            empty_count_cell_row_2, empty_count_cell_col_2
        ):
            if max(empty_count_cell_row_1, empty_count_cell_col_1) < max(
                empty_count_cell_row_2, empty_count_cell_col_2
            ):
                return empty_cell_1[0], empty_cell_1[1]

        if min(empty_count_cell_row_1, empty_count_cell_col_1) < min(
            empty_count_cell_row_2, empty_count_cell_col_2
        ):
            return empty_cell_1[0], empty_cell_1[1]
        return empty_cell_2[0], empty_cell_2[1]

    def solve_sudoku(self, board):
        """Algorithm solver"""
        row, col = self.find_next_cell(board)

        if row is None:
            return True

        for guess in range(1, 10):
            if self.verification(board, row, col, str(guess)):
                board[row][col].text = str(guess)

                if self.solve_sudoku(board):
                    return True

        board[row][col].text = ""

        return False

    def verification(self, board, row, col, guess):
        """Verification of the values"""
        row_vals = [board[row][i].text for i in range(9)]
        if guess in row_vals:
            return False

        col_vals = [board[i][col].text for i in range(9)]
        if guess in col_vals:
            return False

        row_start = (row // 3) * 3  # 10 // 3 = 3, 5 // 3 = 1, 1 // 3 = 0
        col_start = (col // 3) * 3

        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if board[r][c].text == guess:
                    return False

        return True


class sudokusolverapp(App):
    """App to solve sudoku puzzle"""


sudokusolverapp().run()
