import pygame
from typing import Tuple
from ..utils.constants import GAME_CONFIG, COLORS

class PowerUpType:
    BOMB = "BOMB_UP"
    FIRE = "FIRE_UP"
    SPEED = "SPEED_UP"
    HEART = "HEART"

POWERUP_COLORS = {
    PowerUpType.BOMB: COLORS['CYAN'],
    PowerUpType.FIRE: COLORS['ORANGE'],
    PowerUpType.SPEED: COLORS['YELLOW'],
    PowerUpType.HEART: COLORS['PINK'],
}

class PowerUp:
    def __init__(self, grid_x: int, grid_y: int, ptype: str):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.ptype = ptype
        self.tile_size = GAME_CONFIG['TILE_SIZE']
        self.rect = pygame.Rect(grid_x * self.tile_size, grid_y * self.tile_size,
                                self.tile_size, self.tile_size)

    def apply_to(self, player) -> None:
        if self.ptype == PowerUpType.BOMB:
            player.bomb_capacity = min(player.bomb_capacity + 1, GAME_CONFIG['MAX_BOMB_CAPACITY'])
        elif self.ptype == PowerUpType.FIRE:
            player.flame_radius = min(player.flame_radius + 1, GAME_CONFIG['MAX_FLAME_RADIUS'])
        elif self.ptype == PowerUpType.SPEED:
            player.speed = min(player.speed + GAME_CONFIG['SPEED_UP_DELTA'], GAME_CONFIG['MAX_SPEED'])
        elif self.ptype == PowerUpType.HEART:
            player.lives += 1  # vida extra

    def render(self, screen: pygame.Surface):
        color = POWERUP_COLORS.get(self.ptype, COLORS['WHITE'])
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLORS['BLACK'], self.rect, 2)
