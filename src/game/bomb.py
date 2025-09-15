import pygame
import time
from typing import List, Tuple
from ..utils.constants import GAME_CONFIG, COLORS

class Bomb:
    def __init__(self, x: int, y: int, timer: float):
        self.grid_x = x
        self.grid_y = y
        self.timer = timer
        self.plant_time = time.time()
        self.explosion_radius = GAME_CONFIG['EXPLOSION_RADIUS']

        self.world_x = x * GAME_CONFIG['TILE_SIZE']
        self.world_y = y * GAME_CONFIG['TILE_SIZE']
        self.size = GAME_CONFIG['TILE_SIZE'] - 6
        self.color = COLORS['RED']

        self.rect = pygame.Rect(self.world_x + 3, self.world_y + 3, self.size, self.size)

    def update(self):
        pass

    def should_explode(self) -> bool:
        return time.time() - self.plant_time >= self.timer

    def get_explosion_positions(self, game_map) -> List[Tuple[int, int]]:
        """
        Raycast em 4 direções:
         - Para em parede sólida (não inclui).
         - Inclui bloco destrutível e para (não atravessa).
        """
        positions = [(self.grid_x, self.grid_y)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            for i in range(1, self.explosion_radius + 1):
                nx = self.grid_x + dx * i
                ny = self.grid_y + dy * i
                if not game_map.is_valid_position(nx, ny):
                    break
                if game_map.is_wall(nx, ny):
                    # sólido: para sem incluir
                    break
                positions.append((nx, ny))
                if game_map.is_destructible_wall(nx, ny):
                    # inclui e para
                    break
        return positions

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        # timer visual
        time_left = max(0.0, self.timer - (time.time() - self.plant_time))
        if time_left > 0:
            font = pygame.font.Font(None, 24)
            timer_text = font.render(str(int(time_left) + 1), True, COLORS['WHITE'])
            text_rect = timer_text.get_rect(center=self.rect.center)
            screen.blit(timer_text, text_rect)
