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


class AreaState:
    INITIAL = 2
    CLEARED = 4 # This area has been cleared, i.e do not contain any mine
    MARKED = 8 # This area has been marked as mined by the player
    EXPLODED = 16 # The player tried to walk on a mine and it doesn't ended well


class Area(pygame.sprite.Sprite):
    def __init__(self, field, has_mine, images, fonts):
        super(Area, self).__init__()

        self.field = field
        self.has_mine = has_mine
        self.images = images
        self.fonts = fonts

        self.nearby_mines_count = 0
        self.state = AreaState.INITIAL

    def __getstate__(self):
        """Needed by Pickle to give the proper attributes to be picked."""
        state = self.__dict__.copy()

        del state['field']
        del state['images']
        del state['fonts']
        del state['image']
        del state['rect']

        return state

    def __setstate__(self, state):
        """Needed by Pickle to properly initialize this Area instance."""
        self.__dict__.update(state)

    @property
    def state(self):
        """state getter."""
        return self._state

    @state.setter
    def state(self, value):
        """state setter."""
        self._state = value

        self.draw()

    def toggle_mine_marker(self):
        """Try to toggle this area's mine marker."""
        if self.state not in [AreaState.INITIAL, AreaState.MARKED]:
            return False

        if self.state == AreaState.INITIAL:
            if self.field.mines_left > 0:
                self.state = AreaState.MARKED
                self.field.mines_left -= 1
            else:
                return False
        else:
            self.state = AreaState.INITIAL
            self.field.mines_left += 1

        return True

    def mark_as_clear(self):
        """Try to mark this area as clear."""
        if self.state != AreaState.INITIAL:
            return False

        if self.has_mine:
            self.state = AreaState.EXPLODED
        else:
            self.state = AreaState.CLEARED

        return True

    def draw(self):
        """Draw this area."""
        if self.state in [AreaState.INITIAL, AreaState.MARKED, AreaState.EXPLODED]:
            background = self.images['area_uncleared']
        elif self.state == AreaState.CLEARED:
            background = self.images['area_cleared']

        # Create an empty surface and assign it to this area
        background_rect = background.get_rect()

        self.image = pygame.Surface(background_rect.size, pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

        # Blit the area background on the empty surface
        background_rect.center = self.rect.center

        self.image.blit(background, background_rect)

        # Game over: show all mines
        if self.field.show_mines and self.has_mine and self.state != AreaState.EXPLODED:
            mine_rect = self.images['mine'].get_rect()
            mine_rect.center = self.rect.center

            self.image.blit(self.images['mine'], mine_rect)

        if self.state == AreaState.MARKED: # Blit the mine marker, if any
            mine_marker_rect = self.images['mine_marker'].get_rect()
            mine_marker_rect.center = self.rect.center

            self.image.blit(self.images['mine_marker'], mine_marker_rect)
        elif self.state == AreaState.CLEARED and self.nearby_mines_count > 0: # Blit the nearby mines count if > 0
            nearby_mines_text = self.fonts['nearby_mines_count'].render(str(self.nearby_mines_count), True, self.nearby_mines_count_color)
            nearby_mines_text_rect = nearby_mines_text.get_rect()
            nearby_mines_text_rect.center = self.rect.center

            self.image.blit(nearby_mines_text, nearby_mines_text_rect)
        elif self.state == AreaState.EXPLODED: # The player walked on a mine (game over)
            mine_exploded_rect = self.images['mine_exploded'].get_rect()
            mine_exploded_rect.center = self.rect.center

            self.image.blit(self.images['mine_exploded'], mine_exploded_rect)

    @property
    def nearby_mines_count_color(self):
        """Return the color corresponding to the nearby mines count of this area."""
        return settings.NEARBY_MINES_COUNT_COLORS[self.nearby_mines_count] if self.nearby_mines_count in settings.NEARBY_MINES_COUNT_COLORS else None


class Field:
    _show_mines = False

    def __init__(self, width, height, mines, images, fonts):
        self.width = width
        self.height = height
        self.mines = self.mines_left = mines
        self.images = images
        self.fonts = fonts

        self.areas = self.width * self.height

        if self.mines > self.areas:
            raise ValueError('Not enough space for {} mines'.format(self.mines))

        self.field = []

        self._populate()
        self._compute_nearby_mines()

    def __getstate__(self):
        """Needed by Pickle to give the proper attributes to be picked."""
        state = self.__dict__.copy()

        del state['images']
        del state['fonts']

        return state

    def __setstate__(self, state):
        """Needed by Pickle to properly initialize this Field instance."""
        self.__dict__.update(state)

    def set_state(self, field, images, fonts):
        """Update attributes in this Field instance and all of its Area children."""
        self.images = images
        self.fonts = fonts

        for row in self.field:
            for area in row:
                area.field = field
                area.images = images
                area.fonts = fonts

                area.draw()

    @property
    def show_mines(self):
        """show_mines getter."""
        return self._show_mines

    @show_mines.setter
    def show_mines(self, value):
        """show_mines setter."""
        self._show_mines = value

        if self._show_mines:
            for row in self.field:
                for area in row:
                    if area.has_mine:
                        area.draw()

    def is_clear(self):
        """Determine if the field has been cleared of all of its mines (win condition)."""
        for row in self.field:
            for area in row:
                if (area.has_mine and area.state != AreaState.MARKED) or area.state == AreaState.INITIAL:
                    return False

        return True

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
                    field=self,
                    has_mine=area_number in areas_with_mine,
                    images=self.images,
                    fonts=self.fonts
                ))

                area_number += 1

            self.field.append(row)

    def _compute_nearby_mines(self):
        """For each area that aren't mined, compute the surrounding areas that are mined."""
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
