EMPTY = ' '
EMPTY_POSITION = 'EMPTY STATE'
MATCHED_POSITION = 'MATCHED STATE'
FILLED_POSITION = 'FILLED POSITION'
FALLER_FALLING = 'FALLER_FALLING'
FALLER_STOPPED = 'FALLER_STOPPED'
FALLING_NUM = 1
NOT_FALLING_NUM = 0
LEFT = -1
RIGHT = 1
ROTATE_ONE = 1
ROTATE_TWO = 2
DOWN = 0
DOWN_LEFT = 2

def _active_state(state: str) -> bool:
    '''
    helper method that confirms a position is
    either filled or in a matched state
    '''
    return state == FILLED_POSITION or state == MATCHED_POSITION

class FallingGems:
    def __init__(self) -> None:
        '''
        creates a Faller class for when a faller
        needs to be created
        '''
        self.falling = False
        self._row = 0
        self._column = 0
        self.content = [EMPTY, EMPTY, EMPTY]
        self.current_state = FALLING_NUM
    
    def get_row(self) -> int:
        return self._row
    
    def get_column(self) -> int:
        return self._column
    
    def set_row(self, row: int) -> None:
        self._row = row

    def set_column(self, column: int) -> None:
        self._column = column


class GameState:
    def __init__(self, rows: int, columns: int) -> None:
        self._rows = rows
        self._columns = columns
        self._rows_on_board = []
        self._state_of_board = []
        self._faller = FallingGems()
        for x in range(rows):
            row = []
            state_of_row = []
            for y in range(columns):
                row.append(EMPTY)
                state_of_row.append(EMPTY_POSITION)
            self._rows_on_board.append(row)
            self._state_of_board.append(state_of_row)


    def make_game_board(self, content: list) -> None:
        '''
        if user inputs CONTENTS,sets the state of 
        each position based of the content that was inputed
        moves gems down if there is open space
        matches gems if there is a valid match 
        '''
        for row in range(self.get_rows()):
            for column in range(self.get_columns()):
                position = content[row][column]
                if position is EMPTY:
                    self._set_position(row, column, EMPTY, EMPTY_POSITION)
                else:
                    self._set_position(row, column, position, FILLED_POSITION)
        self.faller_gravity()
        self._match_gems()


    def get_rows(self) -> int:
        return self._rows
    

    def get_columns(self) -> int:
        return self._columns
    

    def falling_faller(self) -> bool:
        '''
        determines if a faller is 
        still falling or is stopped
        '''
        return self._faller.falling
    

    def get_position_state(self, row: int, column: int) -> str:
        '''
        returns state of a given position
        '''
        return self._state_of_board[row][column]


    def get_position_content(self, row: int, column: int) -> str:
        '''
        returns the gem that is in the given position
        '''
        return self._rows_on_board[row][column]


    def _set_position(self, row: int, column: int, content: str, state: str) -> None:
        '''
        sets the gem and state of a given position
        '''
        if row < 0:
            return
        self._set_position_content(row, column, content)
        self._set_position_state(row, column, state)


    def _set_position_content(self, row: int, column: int, content: str) -> None:
        '''
        sets the gem of a given position
        '''
        if row < 0:
            return
        self._rows_on_board[row][column] = content


    def _set_position_state(self, row: int, column: int, state: str) -> None:
        '''
        sets the state of given position
        '''
        if row < 0:
            return 
        self._state_of_board[row][column] = state


    def faller_tick(self) -> bool:
        '''
        checks
        '''
        if self._faller.falling:
            if self._faller.current_state == NOT_FALLING_NUM:
                self._update_faller_state()

                if self._faller.current_state == NOT_FALLING_NUM:
                    state = False
                    if self._faller.get_row() - 2 < 0:
                        state = True

                    for x in range(3):
                        self._set_position(self._faller.get_row() - x, self._faller.get_column(),
                                           self._faller.content[x], FILLED_POSITION)
                    self._faller.falling = False

                    self._match_gems()
                    return state
                
            self.move_gems_down()
            self._update_faller_state()

        self._match_gems()
        return False
    

    def _update_faller_state(self) -> None:
        '''
        
        '''
        state = None
        desired_row = self._faller.get_row() + 1
        if self._column_taken(desired_row, self._faller.get_column()):
            state = FALLER_STOPPED
            self._faller.current_state = NOT_FALLING_NUM
        else:
            state = FALLER_FALLING
            self._faller.current_state = FALLING_NUM
        
        for x in range(3):
            row = self._faller.get_row() - x
            if row < 0:
                return 
            self._set_position(row, self._faller.get_column(), self._faller.content[x], state)
    

    def _column_taken(self, row: int, column: int) -> bool:
        '''
        returns True if the state of the position is 
        filled 
        returns False otherwise
        '''
        if row >= self.get_rows():
            return True

        if self.get_position_state(row, column) == FILLED_POSITION:
            return True
        
        return False
    

    def create_faller(self, column: int, faller: list) -> None:
        '''
        creates a faller 
        '''
        if self._faller.falling:
            return 
        
        self._faller.falling = True
        self._faller.content = faller
        self._faller.set_row(0)
        self._faller.set_column(column - 1)
        self._set_position(0, self._faller.get_column(), self._faller.content[0],
                           FALLER_FALLING)
        self._update_faller_state()


    def shift_faller(self, left_or_right: int) -> None:
        '''
        checks if the falling is currently falling and 
        if input is RIGHT or LEFT
        if column is not taken or a valid column
        the faller is shifted
        '''
        if not self._faller.falling:
            return 
        
        if not left_or_right == RIGHT and not left_or_right == LEFT:
            return 
        
        if (left_or_right == LEFT and self._faller.get_column() == 0) or (
            left_or_right == RIGHT and self._faller.get_column() == self.get_columns() - 1):
            return

        final_position = self._faller.get_column() + left_or_right
        for x in range(3):
            if self._faller.get_row() - x < 0:
                break
            if self.get_position_state(self._faller.get_row() - x, final_position) == FILLED_POSITION:
                return
        
        for x in range(3):
            if self._faller.get_row() - x < 0:
                break
            self._move_position(self._faller.get_row() - x, self._faller.get_column(), left_or_right)
        
        self._faller.set_column(final_position)
        self._update_faller_state()


    def switch_jewel_positions(self) -> None:
        '''
        checks if falling is currently falling
        splits gems into their own variables
        and rotates the positions into a tuple
        changes position contents accordingly
        '''
        if not self._faller.falling:
            return
        
        first = self._faller.content[0]
        second = self._faller.content[1]
        third = self._faller.content[2]

        self._faller.content = [second, third, first]

        for x in range(3):
            self._set_position_content(self._faller.get_row() - x, self._faller.get_column(),
                                       self._faller.content[x])
        self._update_faller_state()


    def rotate_faller(self) -> None:
        current_column = self._faller.get_column()
        current_row = self._faller.get_row()
        current_jewel_content = self._faller.content
        board_width = self.get_columns()

        faller_len = len(current_jewel_content)
        right_bound = current_column + faller_len - 1
        left_bound = current_column

        if right_bound >= board_width:
            shift = right_bound - (board_width - 1)
            current_column -= shift
        elif left_bound < 0:
            current_column = 0
        
        for x in range(faller_len):
            row = current_row - x
            column = current_column
            if self.get_position_content(row, column) != EMPTY:
                return
            
        self._clear_faller()
        self._faller.set_column(current_column)
        for x, jewel in enumerate(current_jewel_content):
            self._set_position(current_row - x, current_column + x, jewel, FALLER_FALLING)

    
    def _clear_faller(self) -> None:
        column = self._faller.get_column()
        row = self._faller.get_row()
        faller_len = len(self._faller.content)

        for x in range(faller_len):
            self._set_position(row - x, column, EMPTY, EMPTY_POSITION)


    def faller_gravity(self) -> None:
        '''
        
        '''
        for column in range(self.get_columns()):
            for row in range(self.get_rows() - 1, -1, -1):
                state = self.get_position_state(row, column)

                if state == FALLER_FALLING or state == FALLER_STOPPED:
                    continue 
                if state == FILLED_POSITION:
                    x = 1
                    while not self._column_taken(row + x, column):
                        self._move_position(row + x - 1, column, DOWN)
                        x += 1


    def move_gems_down(self) -> None:
        '''
        
        '''
        if self._column_taken(self._faller.get_row() + 1, self._faller.get_column()):
            return
        
        
        self._move_position(self._faller.get_row(), self._faller.get_column(), DOWN)

        if self._faller.get_row() - 1 >= 0:
            self._move_position(self._faller.get_row() - 1, self._faller.get_column(), DOWN)

            if self._faller.get_row() - 2 >= 0:
                self._move_position(self._faller.get_row() - 2, self._faller.get_column(), DOWN)
            else:
                self._set_position(self._faller.get_row() - 1, self._faller.get_column(), self._faller.content[2],
                                   FALLER_FALLING)
        else:
            self._set_position(self._faller.get_row(), self._faller.get_column(), self._faller.content[1], 
                               FALLER_FALLING)

        self._faller.set_row(self._faller.get_row() + 1)



    def _move_position(self, row: int, column: int, left_or_right: int) -> None:
        '''
        
        '''
        original_letter_position = self._rows_on_board[row][column]
        original_state = self._state_of_board[row][column]

        self._rows_on_board[row][column] = EMPTY
        self._state_of_board[row][column] = EMPTY_POSITION

        if left_or_right == DOWN:
            desired_row = row + 1
            self._rows_on_board[desired_row][column] = original_letter_position
            self._state_of_board[desired_row][column] = original_state
        else:
            desired_column = column + left_or_right
            self._rows_on_board[row][desired_column] = original_letter_position
            self._state_of_board[row][desired_column] = original_state


    def _change_to_matched_position(self, row: int, column: int, left_or_right: int, matches: int) -> None:
        '''
        
        '''
        if left_or_right == LEFT:
            for desired_column in range(column, column - matches, -1):
                self._set_position_state(row, desired_column, MATCHED_POSITION)

        elif left_or_right == DOWN:
            for desired_row in range(row, row + matches):
                self._set_position_state(desired_row, column, MATCHED_POSITION)

        elif left_or_right == DOWN_LEFT:
            for x in range(matches):
                self._set_position_state(row + x, column - x, MATCHED_POSITION)


    def _match_gems(self) -> None:
        for row in range(self.get_rows()):
            for column in range(self.get_columns()):
                if self.get_position_state(row, column) == MATCHED_POSITION:
                    self._set_position(row, column, EMPTY, EMPTY_POSITION)
        
        self.faller_gravity()

        self._match_gems_x()
        self._match_gems_y()
        self._match_diagonal_gems()
    

    def _match_gems_x(self) -> None:
        '''
        
        '''
        for row in range(self.get_rows() - 1, -1, -1):
            matches = 0
            gem = 'NONE'

            for column in range(self.get_columns()):
                content = self.get_position_content(row, column)
                state = self.get_position_state(row, column)
                position_matches = (content == gem and _active_state(state))

                if position_matches:
                    matches += 1
                
                if column == self.get_columns() - 1:
                    if matches >= 3:
                        if position_matches:
                            self._change_to_matched_position(row, column, LEFT, matches)
                        else:
                            self._change_to_matched_position(row, column - 1, LEFT, matches)
                elif not position_matches:
                    if matches >= 3:
                        self._change_to_matched_position(row, column - 1, LEFT, matches)

                    if _active_state(state):
                        gem = content
                        matches = 1
                    else:
                        gem = 'NONE'
                        matches = 1


    def _match_gems_y(self) -> None:
        '''
        
        '''
        for column in range(self.get_columns()):
            matches = 0
            gem = 'NONE'
            
            for row in range(self.get_rows() - 1, -1, -1):
                content = self.get_position_content(row, column)
                state = self.get_position_state(row, column)
                position_matches = (content == gem and _active_state(state))

                if position_matches:
                    matches += 1
                
                if row == 0:
                    if matches >= 3:
                        if position_matches:
                            self._change_to_matched_position(row, column, DOWN, matches)
                        else:
                            self._change_to_matched_position(row + 1, column, DOWN, matches)
                elif not position_matches:
                    if matches >= 3:
                        self._change_to_matched_position(row + 1, column, DOWN, matches)
                    
                    if _active_state(state):
                        gem = content
                        matches = 1
                    else:
                        gem = 'NONE'
                        matches = 1
            

    def _match_diagonal_gems(self) -> None:
        '''
        
        '''
        for row in range(self.get_rows() - 1, -1 , -1):
            for column in range(self.get_columns()):
                matches = 0
                gem = 'NONE'
                row_count = 0
                column_count = 0
                
                while True:
                    the_row = row - row_count
                    the_column = column + column_count

                    content = self.get_position_content(the_row, the_column)
                    state = self.get_position_state(the_row, the_column)
                    position_matches = (content == gem and _active_state(state))

                    if position_matches:
                        matches += 1

                    if the_column == self.get_columns() - 1 or the_row == 0:
                        if matches >= 3:
                            if position_matches:
                                self._change_to_matched_position(the_row, the_column, DOWN_LEFT, matches)
                            else:
                                self._change_to_matched_position(the_row + 1, the_column - 1, DOWN_LEFT, matches)
                    elif not position_matches:
                        if matches >= 3:
                            self._change_to_matched_position(the_row + 1, the_column - 1, DOWN_LEFT, matches)
                        
                        if _active_state(state):
                            gem = content
                            matches = 1
                        else:
                            gem = 'NONE'
                            matches = 1
                    
                    row_count += 1
                    column_count += 1

                    if row - row_count < 0 or column + column_count >= self.get_columns():
                        break

    