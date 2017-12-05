import settings
import random
import pygame


DIRECTIONS = (
    (0, -1), # Top
    (1, -1), # Top right
    (1, 0),  # Right
    (1, 1),  # Bottom right
    (0, 1),  # Bottom
    (-1, 1), # Bottom left
    (-1, 0), # Left
    (-1, -1) # Top left
)


class Area(pygame.sprite.Sprite):
    nearby_mines_count = 0
    _is_cleared = False # This area has been cleared, i.e do not contain any mine
    _is_marked = False # This area has been marked as mined

    def __init__(self, images, has_mine):
        super(Area, self).__init__()

        self.images = images
        self.has_mine = has_mine

        self._draw()

    @property
    def is_cleared(self):
        """is_cleared getter."""
        return self._is_cleared

    @is_cleared.setter
    def is_cleared(self, value):
        """is_cleared setter."""
        self._is_cleared = value

        self._draw()

    @property
    def is_marked(self):
        """is_marked getter."""
        return self._is_marked

    @is_marked.setter
    def is_marked(self, value):
        """is_marked setter."""
        self._is_marked = value

        self._draw()

    def toggle_mine_marker(self):
        """Try to toggle this area's mine marker."""
        if self.is_cleared:
            return False

        self.is_marked = not self.is_marked

        return True

    def mark_as_clear(self):
        """Try to mark this area as clear."""
        if self.is_cleared:
            return False

        self.is_cleared = True

        return True

    def _draw(self):
        """Draw this area."""
        # Create an empty surface and assign it to this area
        self.image = pygame.Surface((settings.AREAS_SIDE_SIZE, settings.AREAS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

        # Blit the area background on the empty surface
        background = self.images['area_cleared' if self.is_cleared else 'area_uncleared']

        self.image.blit(background, background.get_rect())

        # Blit the mine marker, if any
        if self.is_marked:
            marked_rect = self.images['mine_marker'].get_rect()
            marked_rect.center = self.rect.center

            self.image.blit(self.images['mine_marker'], marked_rect)

    @property
    def nearby_mines_count_color(self):
        """Return the color corresponding to the nearby mines count of this area."""
        return settings.NEARBY_MINES_COUNT_COLORS[self.nearby_mines_count] if self.nearby_mines_count in settings.NEARBY_MINES_COUNT_COLORS else None


class Field:
    field = []

    def __init__(self, images, width, height, mines):
        self.images = images
        self.width = width
        self.height = height
        self.mines = mines
        self.areas = self.width * self.height

        if self.mines > self.areas:
            raise ValueError('Not enough space for {} mines'.format(self.mines))

        self._populate()
        self._compute_nearby_mines()

    def _generate_areas_with_mine(self):
        """Generate random mines position for the current field."""
        areas_with_mine = []

        for _ in range(0, self.mines):
            while True:
                random_area_number = random.randint(0, self.areas - 1)

                if random_area_number not in areas_with_mine:
                    areas_with_mine.append(random_area_number)

                    break

        return areas_with_mine

    def _populate(self):
        """Generate and place random mines for the current field."""
        areas_with_mine = self._generate_areas_with_mine()
        area_number = 0

        for y in range(0, self.height):
            row = []

            for x in range(0, self.width):
                row.append(Area(
                    has_mine=area_number in areas_with_mine,
                    images=self.images
                ))

                area_number += 1

            self.field.append(row)

    def _compute_nearby_mines(self):
        """For each area that isn't mined, compute the surrounding mined areas."""
        for y, row in enumerate(self.field):
            for x, area in enumerate(row):
                if area.has_mine:
                    continue

                for direction in DIRECTIONS:
                    dir_x, dir_y = direction

                    nearby_x = x + dir_x
                    nearby_y = y + dir_y

                    if nearby_x < 0 or nearby_x > self.width - 1:
                        continue

                    if nearby_y < 0 or nearby_y > self.height - 1:
                        continue

                    if self.field[nearby_y][nearby_x].has_mine:
                        area.nearby_mines_count += 1

    def __str__(self):
        """Return a text representation of this field."""
        ret = []

        for y, row in enumerate(self.field):
            ret_row = '{:>2}|'.format(y)

            for area in row:
                if area.has_mine:
                    out = 'X'
                elif area.nearby_mines_count > 0:
                    out = str(area.nearby_mines_count)
                else:
                    out = ' '

                ret_row += out

            ret.append(ret_row)

        return '\n'.join(ret)
