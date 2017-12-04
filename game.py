import settings
import logging
import helpers
import pygame
import field
import sys


class Game:
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

        self.nearby_mines_count_font = helpers.load_font('coolvetica.ttf', 14)

    def _load_images(self):
        """Load all images."""
        logging.info('Loading images')

        self.images = {
            'area': {
                'cleared': [helpers.load_image('area/cleared_{}.png'.format(i)) for i in range(1, 3)],
                'uncleared': [helpers.load_image('area/uncleared_{}.png'.format(i)) for i in range(1, 3)]
            },
            'mine_marker': helpers.load_image('mine_marker.png')
        }

    def _start_new_game(self):
        """Start a new game."""
        logging.info('Initializing new game')

        self.field = field.Field(images=self.images, width=settings.WIDTH, height=settings.HEIGHT, mines=settings.MINES)
        self.field.print()

    def update(self):
        """Perform every updates of the game logic, events handling and drawing.
        Also known as the game loop."""

        # Events handling
        for event in pygame.event.get():
            event_handlers = [
                self._event_quit # TODO
            ]

            for handler in event_handlers:
                if handler(event):
                    break

        # Drawings
        self._draw_grid()
        self._draw_areas()

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

    # --------------------------------------------------------------------------
    # Drawing handlers

    def _draw_grid(self):
        """Draw the grid which separates the areas."""
        for x in range(0, settings.WIDTH + 1):
            pygame.draw.rect(
                self.window,
                settings.GRID_COLOR,
                pygame.Rect(
                    (x * settings.AREAS_SIDE_SIZE + (x - 1) * settings.GRID_SPACING, 0),
                    (settings.GRID_SPACING, self.window_rect.h)
                )
            )

        for y in range(0, settings.HEIGHT + 1):
            pygame.draw.rect(
                self.window,
                settings.GRID_COLOR,
                pygame.Rect(
                    (0, y * settings.AREAS_SIDE_SIZE + (y - 1) * settings.GRID_SPACING),
                    (self.window_rect.w, settings.GRID_SPACING)
                )
            )

    def _draw_areas(self):
        """Draw the areas."""
        for y, row in enumerate(self.field.field):
            for x, area in enumerate(row):
                area.rect.top = y * settings.AREAS_SIDE_SIZE + y * settings.GRID_SPACING
                area.rect.left = x * settings.AREAS_SIDE_SIZE + x * settings.GRID_SPACING

                self.window.blit(area.image, area.rect)
