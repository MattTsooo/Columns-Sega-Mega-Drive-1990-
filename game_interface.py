import pygame
import random
import game_state_model as game_state
from pathlib import Path

_COLUMNS = 6
_ROWS = 13
_FPS = 10
_JEWELS = ['X', 'Y', 'Z', 'W', 'T', 'V', 'S']


class ColumnsGame:
    def __init__(self) -> None:
        self._surface = pygame.display.set_mode((800,800))
        self._surface_width = self._surface.get_width()
        self._surface_height = self._surface.get_height()
        self.game_state = game_state.GameState(_ROWS, _COLUMNS)
        self.game_is_running = True
        self.tick_tracker = 0
        self._y_buffer = .08
        self._jewel_size = (1.0 - self._y_buffer) / _ROWS
        self._x_buffer = 1.0 - (self._jewel_size * _COLUMNS)
        self._upcoming_faller_jewels = random.choices(_JEWELS, k=3)
        self._score = 0
        self._high_score = 0
        self._matched_positions_score = []


    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        self._set_surface((800, 800))

        while self.game_is_running:
            clock.tick(_FPS)
            self._handle_events()

            self.tick_tracker += 2
            if self.tick_tracker == _FPS:
                self._tick_faller_down()
                self.tick_tracker = 0

            self._draw_game_interface()

        pygame.quit()


    def _set_surface(self, size: tuple[float, float]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)


    def _end_game(self) -> bool:
        self.game_is_running = False

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()

        self._handle_keys()


    def _handle_keys(self) -> None:
        input = pygame.key.get_pressed()

        if input[pygame.K_RIGHT]:
            self.game_state.shift_faller(game_state.RIGHT)
        elif input[pygame.K_LEFT]:
            self.game_state.shift_faller(game_state.LEFT)
        elif input[pygame.K_SPACE]:
            self.game_state.switch_jewel_positions()
        elif input[pygame.K_DOWN]:
            self.game_state.move_gems_down()
        elif input[pygame.K_UP]:
            self.game_state.rotate_faller()


    def _draw_game_interface(self) -> None:
        self._surface.fill(pygame.Color(37, 109, 123))
        self._draw_game_board_and_fallers()
        for row in range(_ROWS):
            for column in range(_COLUMNS):
                self._store_and_display_next_jewel(self._upcoming_faller_jewels, row, column)
        pygame.display.flip()


    def _draw_game_board_and_fallers(self) -> None:
        
        frac_x = self._x_buffer / 2
        frac_y = self._y_buffer / 2
        topleft_frac_x = int(frac_x * self._surface_width) - 100
        topleft_frac_y = int(frac_y * self._surface_height)

        width = int(self._jewel_size * _COLUMNS * self._surface_width)
        height = int(self._jewel_size * _ROWS * self._surface_height)

        game_board = pygame.Rect(topleft_frac_x, topleft_frac_y, width, height)
        pygame.draw.rect(self._surface, pygame.Color(0,0,0), game_board)

                         
        self._draw_grid(topleft_frac_x, topleft_frac_y, width, height)

        for row in range(_ROWS):
            for column in range(_COLUMNS):
                self._draw_a_jewel(row, column, topleft_frac_x, topleft_frac_y)
    

    def _draw_grid(self, topleft_frac_x: float, topleft_frac_y: float, width: int, height: int) -> None:
        row_spacing = self._jewel_size * self._surface_height
        column_spacing = self._jewel_size * self._surface_width
        jewel_window_x = topleft_frac_x * width
        
        for row in range(1, _ROWS):
            y_coord = topleft_frac_y + int(row * row_spacing)
            pygame.draw.lines(self._surface, pygame.Color(255,255,255), False, [(topleft_frac_x, y_coord), 
                                                                                (topleft_frac_x + width, y_coord)], 2)

        for column in range(1, _COLUMNS):
            x_coord = topleft_frac_x + int(column * column_spacing)
            pygame.draw.lines(self._surface, pygame.Color(255,255,255), False, [(x_coord, topleft_frac_y), 
                                                                                (x_coord, topleft_frac_y + height)], 2)

        for row in range(1,3):
            y_coord = topleft_frac_y + int(row * row_spacing)
            pygame.draw.lines(self._surface, pygame.Color(255,255,255), False, [(jewel_window_x, y_coord), 
                                                                                (jewel_window_x + row_spacing, y_coord)], 2)
            

    def _draw_a_jewel(self, row: int, column: int, topleft_frac_x: float, topleft_frac_y: float) -> None:
        jewel = self.game_state.get_position_content(row, column)

        if jewel is game_state.EMPTY:
            return 
        
        if self.game_state.get_position_state(row, column) == game_state.MATCHED_POSITION:
            color = self._flashing_animation(row, column, self.tick_tracker)
        else:
            color = self._get_jewel_color(jewel)
        
        jewel_color = pygame.Color(color[0], color[1], color[2])
        
        jewel_width = self._jewel_size * self._surface_width
        jewel_height = self._jewel_size * self._surface_height
        jewel_x = int(topleft_frac_x + column * jewel_width) + 1
        jewel_y = int(topleft_frac_y + row * jewel_height) + 1

        rect = pygame.Rect(jewel_x, jewel_y, jewel_width, jewel_height)
        pygame.draw.rect(self._surface, jewel_color, rect)

        if self.game_state.get_position_state(row, column) == game_state.FALLER_STOPPED:
            color = self._flashing_animation(row, column, self.tick_tracker)
            pygame.draw.rect(self._surface, color, rect, 3)


    def _store_and_display_next_jewel(self, next_faller: list, rows: int, columns: int) -> None:
        preview_x = int(((self._x_buffer / 2) * self._surface_width) + (self._jewel_size * 7 * self._surface_width))
        preview_y = int((self._y_buffer / 2) * self._surface_height)
        jewel_width = int(self._jewel_size * self._surface_width)
        jewel_height = int(self._jewel_size * self._surface_height)

        for the_row, jewel in enumerate(reversed(next_faller)):
            if self.game_state.get_position_state(rows, columns) == game_state.FALLER_STOPPED:
                rect = pygame.Rect(preview_x, preview_y + the_row * jewel_height + 80, jewel_width, jewel_height)
                color = self._flashing_animation(rows, columns, self.tick_tracker)
                pygame.draw.rect(self._surface, color, rect, 3)
            else:
                colors = self._get_jewel_color(jewel)
                jewel_colors = pygame.Color(colors[0], colors[1], colors[2])
                rect = pygame.Rect(preview_x, preview_y + the_row * jewel_height + 80, jewel_width, jewel_height)
                pygame.draw.rect(self._surface, jewel_colors, rect)
        


        font = pygame.font.SysFont('timesnewroman', 48)
        text = font.render('Next Faller', True, (0,0,0))
        self._surface.blit(text, (preview_x, preview_y))

        self._show_game_score()

    def _get_jewel_color(self, jewel: str) -> tuple[int, int, int]:
        if jewel == 'X':
            return (252,3,182) #Pink
        elif jewel == 'Y':
            return (136,3,252) #Purple
        elif jewel == 'Z':
            return (3,152,252) #Blue
        elif jewel == 'W':
            return (3,252,11) #Green
        elif jewel == 'T':
            return (252,211,3) #Yellow
        elif jewel == 'V':
            return (252,94,3) #Orange
        elif jewel == 'S':
            return (252,3,3) #Red
    

    def _tick_faller_down(self) -> None:
        jewels = ['X', 'Y', 'Z', 'W', 'T', 'V', 'S']
        self.game_is_running = not self.game_state.faller_tick()

        for row in range(_ROWS):
            for column in range(_COLUMNS):
                if not self.game_state.falling_faller():
                    column_to_drop = random.randint(1,6)
                    self.game_state.create_faller(column_to_drop, self._upcoming_faller_jewels)

                    self._upcoming_faller_jewels = random.choices(jewels, k=3)
                    self._store_and_display_next_jewel(self._upcoming_faller_jewels, row, column)


    def _flashing_animation(self, row: int, column: int, tick_num: int) -> tuple[int, int, int]:
        if tick_num % 3 < 1:
            jewel = self.game_state.get_position_content(row, column)
            return self._get_jewel_color(jewel)
        else:
            return (255,255,255)


    def _show_game_score(self) -> None:
        preview_x = int((self._x_buffer / 2) * (self._surface_width) + (self._jewel_size * 7 * self._surface_width))
        preview_y = int(self._y_buffer * (self._surface_height * 5))

        font = pygame.font.SysFont('timesnewroman', 48)
        score_title_text = font.render('Score', True, (0,0,0))
        high_score_title_text = font.render('High Score', True, (0,0,0))

        self._surface.blit(score_title_text, (preview_x, preview_y))
        self._surface.blit(high_score_title_text, (preview_x, preview_y + 200))

        current_matched_positions = []

        for row in range(_ROWS):
            for column in range(_COLUMNS):
                matched_jewels = self.game_state.get_position_state(row, column)
                if matched_jewels == game_state.MATCHED_POSITION:
                    current_matched_positions.append((row, column))

        
        for position in current_matched_positions:
            if position not in self._matched_positions_score:
                row, column = position
                jewel_type = self.game_state.get_position_content(row, column)
                score_to_add = self._jewel_score_values(jewel_type)
                self._score += score_to_add
        
        self._matched_positions_score = current_matched_positions
        
        self._high_score = self._change_and_get_high_score(self._score)
    
        score_text = font.render(str(self._score), True, (0,0,0))
        high_score_text = font.render(self._high_score, True, (0,0,0))

        self._surface.blit(score_text, (preview_x, preview_y + 100))
        self._surface.blit(high_score_text,(preview_x, preview_y + 300))


    def _change_and_get_high_score(self, score: int) -> str:
            p = Path('/Users/matthewtso/ICS Fall 2024/ICS H32 Project 5/highscore.txt')
            path = open(p, 'r')
            high_score = path.readline()
            path.close()

            if score > int(high_score):
                path = open(p, 'w')
                path.write(str(score))
                path.close()
                return str(score)
            else:
                return high_score

    
    def _jewel_score_values(self, jewel: str) -> int:
        if jewel == 'X':
            return 100 #Pink
        elif jewel == 'Y':
            return 150 #Purple
        elif jewel == 'Z':
            return 125 #Blue
        elif jewel == 'W':
            return 75 #Green
        elif jewel == 'T':
            return 200 #Yellow
        elif jewel == 'V':
            return 500 #Orange
        elif jewel == 'S':
            return 250 #Red

if __name__ == '__main__':
    ColumnsGame().run()