import time
import pygame
from typing import List, Tuple
from ..utils.constants import GAME_CONFIG, COLORS

class Explosion:
    """
    Representa a "chama" da explosão por um curto período (ms).
    Guarda os tiles atingidos e oferece teste de contenção.
    """
    def __init__(self, tiles: List[Tuple[int, int]]):
        self.tiles = tiles[:]  # lista de (grid_x, grid_y)
        self.started = time.time()
        self.duration_ms = GAME_CONFIG['EXPLOSION_DURATION_MS']
        self.tile_size = GAME_CONFIG['TILE_SIZE']

    def is_active(self) -> bool:
        return (time.time() - self.started) * 1000.0 < self.duration_ms

    def contains(self, grid_x: int, grid_y: int) -> bool:
        return (grid_x, grid_y) in self.tiles

    def render(self, screen: pygame.Surface):
        alpha = 180
        surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        for gx, gy in self.tiles:
            # centro mais amarelo; braços alaranjados (mesma cor aqui para simplicidade)
            surf.fill((*COLORS['ORANGE'], alpha))
            screen.blit(surf, (gx * self.tile_size, gy * self.tile_size))
