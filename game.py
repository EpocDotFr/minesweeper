from collections import OrderedDict
from field import Field, AreaState
import save_game_manager
import stats_manager
import settings
import logging
import helpers
import pygame
import sys


class Game:
    # TODO Make something with this
    stats = OrderedDict([
        ('play_time', {'name': 'Play time', 'value': 0, 'format': helpers.humanize_seconds}),
        ('longest_game', {'name': 'Longest game', 'value': 0, 'format': helpers.humanize_seconds}),
        ('shortest_game', {'name': 'Shortest game', 'value': 0, 'format': helpers.humanize_seconds}),
        ('games_won', {'name': 'Total games won', 'value': 0, 'format': helpers.humanize_integer}),
        ('games_lost', {'name': 'Total games lost', 'value': 0, 'format': helpers.humanize_integer})
    ])

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(settings.WINDOW_SIZE, pygame.DOUBLEBUF)
        self.window_rect = self.window.get_rect()

        pygame.display.set_caption('Minesweeper')
        pygame.display.set_icon(helpers.load_image('icon.png'))

        self._load_fonts()
        self._load_images()

        self._start_new_game()

    def _load_fonts(self):
        """Load the fonts."""
        logging.info('Loading fonts')

        self.fonts = {
            'info_panel': helpers.load_font('coolvetica.ttf', 26),
            'nearby_mines_count': helpers.load_font('coolvetica.ttf', 16),
            'normal': helpers.load_font('coolvetica.ttf', 18),
            'title': helpers.load_font('coolvetica.ttf', 30)
        }

    def _load_images(self):
        """Load all images."""
        logging.info('Loading images')

        self.images = {
            'area_cleared': helpers.load_image('area_cleared.png'),
            'area_uncleared': helpers.load_image('area_uncleared.png'),
            'mine_marker': helpers.load_image('mine_marker.png'),
            'mine_exploded': helpers.load_image('mine_exploded.png'),
            'mine': helpers.load_image('mine.png')
        }

    def _start_new_game(self):
        """Start a new game."""
        logging.info('Initializing new game')

        self.field = Field(
            width=settings.WIDTH,
            height=settings.HEIGHT,
            mines=settings.MINES,
            images=self.images,
            fonts=self.fonts
        )

        print(self.field)

        self.duration = 0
        self.state = settings.GameState.PLAYING

        self._toggle_duration_counter(True)

    def _toggle_duration_counter(self, enable=True):
        """Update the game duration counter event."""
        pygame.time.set_timer(settings.GAME_DURATION_EVENT, 1000 if enable else 0) # Every seconds

    def _check_win_condition(self):
        """Check if the player won the game."""
        if self.field.is_clear():
            logging.info('Game won')

            self.state = settings.GameState.WON

            self._toggle_duration_counter(False)

    def update(self):
        """Perform every updates of the game logic, events handling and drawing.
        Also known as the game loop."""

        # Events handling
        for event in pygame.event.get():
            event_handlers = [
                self._event_quit,
                self._event_area_left_click,
                self._event_area_right_click,
                self._event_game_key,
                self._event_game_duration
            ]

            for handler in event_handlers:
                if handler(event):
                    break

        # Drawings
        self.window.fill(settings.WINDOW_BACKGROUND_COLOR)

        self._draw_info_panel()
        self._draw_grid()
        self._draw_field()

        if self.state == settings.GameState.LOST:
            self._draw_lost_screen()
        elif self.state == settings.GameState.WON:
            self._draw_won_screen()

        # PyGame-related updates
        pygame.display.update()

        self.clock.tick(settings.FPS)

    # --------------------------------------------------------------------------
    # Events handlers

    def _event_quit(self, event):
        """Called when the game must be closed."""
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        return False

    def _event_area_left_click(self, event):
        """Left click handler on an area."""
        area = self._get_clicked_area(event, settings.MOUSE_BUTTON_LEFT)

        if not area:
            return False

        if area.mark_as_clear():
            if area.state == AreaState.EXPLODED:
                logging.info('Game lost')

                self.field.show_mines = True
                self.state = settings.GameState.LOST

                self._toggle_duration_counter(False)
            else:
                self._check_win_condition()

        return True

    def _event_area_right_click(self, event):
        """Right click handler on an area."""
        area = self._get_clicked_area(event, settings.MOUSE_BUTTON_RIGHT)

        if not area:
            return False

        if area.toggle_mine_marker():
            self._check_win_condition()

        return True

    def _event_game_duration(self, event):
        """Count the duration of the current game."""
        if event.type != settings.GAME_DURATION_EVENT:
            return False

        self.duration += 1

        return True

    def _event_game_key(self, event):
        """Handle the game keys."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self._start_new_game()

                return True

        return False

    def _get_clicked_area(self, event, required_button):
        """Return the area that was clicked."""
        if self.state != settings.GameState.PLAYING or event.type != pygame.MOUSEBUTTONUP or event.button != required_button:
            return False

        for row in self.field.field:
            for area in row:
                if area.rect.collidepoint(event.pos):
                    return area

        return False

    # --------------------------------------------------------------------------
    # Drawing handlers

    def _draw_info_panel(self):
        """Draws the information panel."""
        # Mines left text
        mines_left_text = self.fonts['info_panel'].render(str(self.field.mines_left), True, settings.TEXT_COLOR)
        mines_left_text_rect = mines_left_text.get_rect()
        mines_left_text_rect.left = 25
        mines_left_text_rect.top = 10

        self.window.blit(mines_left_text, mines_left_text_rect)

        # Game duration text
        duration_text = self.fonts['info_panel'].render(helpers.humanize_seconds(self.duration), True, settings.TEXT_COLOR)
        duration_text_rect = duration_text.get_rect()
        duration_text_rect.right = self.window_rect.w - 25
        duration_text_rect.top = 10

        self.window.blit(duration_text, duration_text_rect)

    def _draw_grid(self):
        """Draws the grid which separates the areas."""
        for x in range(0, settings.WIDTH + 1):
            pygame.draw.rect(
                self.window,
                settings.GRID_COLOR,
                pygame.Rect(
                    (x * settings.AREAS_SIDE_SIZE + (x - 1) * settings.GRID_SPACING, settings.INFO_PANEL_HEIGHT),
                    (settings.GRID_SPACING, self.window_rect.h)
                )
            )

        for y in range(0, settings.HEIGHT + 1):
            pygame.draw.rect(
                self.window,
                settings.GRID_COLOR,
                pygame.Rect(
                    (0, y * settings.AREAS_SIDE_SIZE + (y - 1) * settings.GRID_SPACING + settings.INFO_PANEL_HEIGHT),
                    (self.window_rect.w, settings.GRID_SPACING)
                )
            )

    def _draw_field(self):
        """Draws each areas of the mines field."""
        for y, row in enumerate(self.field.field):
            for x, area in enumerate(row):
                area.rect.top = y * settings.AREAS_SIDE_SIZE + y * settings.GRID_SPACING + settings.INFO_PANEL_HEIGHT
                area.rect.left = x * settings.AREAS_SIDE_SIZE + x * settings.GRID_SPACING

                self.window.blit(area.image, area.rect)

    def _draw_fullscreen_transparent_background(self):
        """Draws a transparent rect that takes the whole window."""
        rect = pygame.Surface(self.window_rect.size)
        rect.set_alpha(150)
        rect.fill(settings.WINDOW_BACKGROUND_COLOR)

        self.window.blit(
            rect,
            pygame.Rect(
                (0, 0),
                self.window_rect.size
            )
        )

    def _draw_fullscreen_window(self, title, text):
        """Draws a title and a text in the middle of the screen."""
        if isinstance(text, str):
            text = [text]

        self._draw_fullscreen_transparent_background()

        # Title
        title_label = self.fonts['title'].render(title, True, settings.TEXT_COLOR)
        title_label_rect = title_label.get_rect()
        title_label_rect.center = self.window_rect.center
        title_label_rect.centery -= 15

        self.window.blit(title_label, title_label_rect)

        # Text
        spacing = 15

        for t in text:
            text_label = self.fonts['normal'].render(t, True, settings.TEXT_COLOR)
            text_label_rect = text_label.get_rect()
            text_label_rect.center = self.window_rect.center
            text_label_rect.centery += spacing

            self.window.blit(text_label, text_label_rect)

            spacing += 20

    def _draw_lost_screen(self):
        """Draws the Lost screen."""
        lost_string = [
            'Looks like this area wasn\'t this safe after all :/',
            'Press "F1" to start a new game.'
        ]

        self._draw_fullscreen_window('Game over!', lost_string)

    def _draw_won_screen(self):
        """Draws the Won screen."""
        lost_string = [
            'You cleared this field from all the mines, well done!',
            'Press "F1" to start a new game.'
        ]

        self._draw_fullscreen_window('All done!', lost_string)
