import pygame
from typing import List, Tuple, Optional
from ..utils.constants import GAME_CONFIG


class GameMap:
    def __init__(self):
        self.width = GAME_CONFIG['MAP_WIDTH']
        self.height = GAME_CONFIG['MAP_HEIGHT']
        self.tile_size = GAME_CONFIG['TILE_SIZE']
        
        self.walls: List[List[int]] = []
        self.destructible_walls: List[List[int]] = []
        
        self._generate_map()
    
    def _generate_map(self):
        self.walls = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.destructible_walls = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.walls[y][x] = 1
                elif x % 2 == 0 and y % 2 == 0:
                    self.walls[y][x] = 1
                elif self._should_place_destructible_wall(x, y):
                    self.destructible_walls[y][x] = 1
    
    def _should_place_destructible_wall(self, x: int, y: int) -> bool:
        if x < 2 or y < 2 or x >= self.width - 2 or y >= self.height - 2:
            return False
        
        if (x == 1 and y == 1) or (x == 2 and y == 1) or (x == 1 and y == 2):
            return False
        
        import random
        return random.random() < 0.3
    
    def is_wall(self, x: int, y: int) -> bool:
        if not self.is_valid_position(x, y):
            return True
        return self.walls[y][x] == 1
    
    def is_destructible_wall(self, x: int, y: int) -> bool:
        if not self.is_valid_position(x, y):
            return False
        return self.destructible_walls[y][x] == 1
    
    def destroy_wall(self, x: int, y: int):
        if self.is_valid_position(x, y):
            self.destructible_walls[y][x] = 0
    
    def can_place_bomb(self, x: int, y: int) -> bool:
        if not self.is_valid_position(x, y):
            return False
        return not self.is_wall(x, y) and not self.is_destructible_wall(x, y)
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def world_to_grid(self, world_x: float, world_y: float) -> Tuple[int, int]:
        grid_x = int(world_x // self.tile_size)
        grid_y = int(world_y // self.tile_size)
        return grid_x, grid_y
    
    def grid_to_world(self, grid_x: int, grid_y: int) -> Tuple[float, float]:
        world_x = grid_x * self.tile_size
        world_y = grid_y * self.tile_size
        return world_x, world_y
    
    def is_player_position(self, x: int, y: int) -> bool:
        return x == 1 and y == 1
    
    def get_enemy_spawn_positions(self) -> List[Tuple[int, int]]:
        positions = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if not self.is_wall(x, y) and not self.is_destructible_wall(x, y):
                    if not (x == 1 and y == 1):
                        positions.append((x, y))
        
        import random
        return random.sample(positions, min(5, len(positions)))
    
    def render(self, screen: pygame.Surface):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, 
                                 self.tile_size, self.tile_size)
                
                if self.is_wall(x, y):
                    pygame.draw.rect(screen, (100, 100, 100), rect)
                elif self.is_destructible_wall(x, y):
                    pygame.draw.rect(screen, (139, 69, 19), rect)
                else:
                    pygame.draw.rect(screen, (50, 50, 50), rect)
                
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
