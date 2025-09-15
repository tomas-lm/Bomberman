import pygame
import random
import time
from typing import Tuple
from ..utils.constants import GAME_CONFIG, COLORS

class Enemy:
    def __init__(self, x: int, y: int, speed: float):
        self.x = x * GAME_CONFIG['TILE_SIZE']
        self.y = y * GAME_CONFIG['TILE_SIZE']
        self.speed = speed
        self.size = GAME_CONFIG['TILE_SIZE'] - 6
        self.color = COLORS['RED']
        self.health = 1
        self.is_alive = True

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.last_direction_change = time.time()
        self.direction_change_interval = random.uniform(1.0, 2.5)

    def update(self, game_map, player):
        if not self.is_alive:
            return

        current_time = time.time()
        if current_time - self.last_direction_change >= self.direction_change_interval:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.last_direction_change = current_time
            self.direction_change_interval = random.uniform(1.0, 2.5)

        dx = self.direction[0] * self.speed
        dy = self.direction[1] * self.speed

        new_x = self.x + dx
        new_y = self.y + dy

        if self._can_move_to(new_x, self.y, game_map):
            self.x = new_x
        else:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        if self._can_move_to(self.x, new_y, game_map):
            self.y = new_y
        else:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def _can_move_to(self, x: float, y: float, game_map) -> bool:
        # Criar retângulo do enemy na nova posição
        enemy_rect = pygame.Rect(x, y, self.size, self.size)
        
        # Verificar colisão com todos os tiles que o enemy pode tocar
        start_grid_x = int(x // GAME_CONFIG['TILE_SIZE'])
        start_grid_y = int(y // GAME_CONFIG['TILE_SIZE'])
        end_grid_x = int((x + self.size) // GAME_CONFIG['TILE_SIZE'])
        end_grid_y = int((y + self.size) // GAME_CONFIG['TILE_SIZE'])
        
        # Verificar todos os tiles que o enemy pode tocar
        for grid_x in range(start_grid_x, end_grid_x + 1):
            for grid_y in range(start_grid_y, end_grid_y + 1):
                # Se está fora dos limites do mapa
                if not game_map.is_valid_position(grid_x, grid_y):
                    return False
                
                # Se é uma parede (sólida ou destrutível)
                if game_map.is_wall(grid_x, grid_y) or game_map.is_destructible_wall(grid_x, grid_y):
                    # Verificar se o enemy está realmente colidindo com este tile
                    tile_rect = pygame.Rect(grid_x * GAME_CONFIG['TILE_SIZE'],
                                          grid_y * GAME_CONFIG['TILE_SIZE'],
                                          GAME_CONFIG['TILE_SIZE'], GAME_CONFIG['TILE_SIZE'])
                    if enemy_rect.colliderect(tile_rect):
                        return False
        
        return True

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.is_alive = False

    def is_dead(self) -> bool:
        return not self.is_alive

    def is_at_position(self, x: int, y: int) -> bool:
        grid_x, grid_y = self._get_grid_position()
        return grid_x == x and grid_y == y

    def _get_grid_position(self) -> Tuple[int, int]:
        grid_x = int(self.x // GAME_CONFIG['TILE_SIZE'])
        grid_y = int(self.y // GAME_CONFIG['TILE_SIZE'])
        return grid_x, grid_y

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    def render(self, screen: pygame.Surface):
        if self.is_alive:
            pygame.draw.rect(screen, self.color, self.rect)
