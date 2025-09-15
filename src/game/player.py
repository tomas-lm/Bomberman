import time
import pygame
from typing import Tuple, List, Optional
from ..utils.constants import GAME_CONFIG, COLORS

class Player:
    def __init__(self, x: int, y: int, speed: float):
        self.x = x * GAME_CONFIG['TILE_SIZE']
        self.y = y * GAME_CONFIG['TILE_SIZE']
        self.speed = speed
        self.size = GAME_CONFIG['TILE_SIZE'] - 6
        self.color = COLORS['BLUE']

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # Bomberman attrs
        self.lives = GAME_CONFIG['PLAYER_LIVES']
        self.invincible_until = 0.0
        self.bomb_capacity = GAME_CONFIG['PLAYER_BOMB_CAPACITY']
        self.flame_radius = GAME_CONFIG['EXPLOSION_RADIUS']
        # Tile da última bomba plantada pelo jogador (pass-through até sair deste tile)
        self.soft_bomb_tile: Optional[Tuple[int, int]] = None

    # --- Helpers ---
    def is_invincible(self) -> bool:
        return time.time() < self.invincible_until

    def grant_invincibility(self, seconds: float):
        self.invincible_until = time.time() + seconds

    def get_position(self) -> Tuple[float, float]:
        return self.x, self.y

    # --- Update & movement ---
    def update(self,
               keys: pygame.key.ScancodeWrapper,
               game_map,
               bombs: List,
               soft_bomb_tile: Optional[Tuple[int, int]]):
        dx = 0.0
        dy = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed if dx == 0 else dx  # sem diagonais rápidas
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed if dy == 0 else dy

        new_x = self.x + dx
        new_y = self.y + dy

        if self._can_move_to(new_x, self.y, game_map, bombs, soft_bomb_tile):
            self.x = new_x

        if self._can_move_to(self.x, new_y, game_map, bombs, soft_bomb_tile):
            self.y = new_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def _can_move_to(self, x: float, y: float, game_map, bombs, soft_bomb_tile) -> bool:
        # Criar retângulo do player na nova posição
        player_rect = pygame.Rect(x, y, self.size, self.size)
        
        # Verificar colisão com todos os tiles que o player pode tocar
        # O player pode ocupar até 4 tiles simultaneamente
        start_grid_x = int(x // GAME_CONFIG['TILE_SIZE'])
        start_grid_y = int(y // GAME_CONFIG['TILE_SIZE'])
        end_grid_x = int((x + self.size) // GAME_CONFIG['TILE_SIZE'])
        end_grid_y = int((y + self.size) // GAME_CONFIG['TILE_SIZE'])
        
        # Verificar todos os tiles que o player pode tocar
        for grid_x in range(start_grid_x, end_grid_x + 1):
            for grid_y in range(start_grid_y, end_grid_y + 1):
                # Se está fora dos limites do mapa
                if not game_map.is_valid_position(grid_x, grid_y):
                    return False
                
                # Se é uma parede (sólida ou destrutível)
                if game_map.is_wall(grid_x, grid_y) or game_map.is_destructible_wall(grid_x, grid_y):
                    # Verificar se o player está realmente colidindo com este tile
                    tile_rect = pygame.Rect(grid_x * GAME_CONFIG['TILE_SIZE'],
                                          grid_y * GAME_CONFIG['TILE_SIZE'],
                                          GAME_CONFIG['TILE_SIZE'], GAME_CONFIG['TILE_SIZE'])
                    if player_rect.colliderect(tile_rect):
                        return False

        # Colisão com bombas (todas são parede), exceto a recém-plantada
        for b in bombs:
            if (b.grid_x, b.grid_y) == soft_bomb_tile:
                # enquanto o jogador ainda estiver neste mesmo tile, permitimos sair
                continue
            bomb_rect = pygame.Rect(b.grid_x * GAME_CONFIG['TILE_SIZE'],
                                    b.grid_y * GAME_CONFIG['TILE_SIZE'],
                                    GAME_CONFIG['TILE_SIZE'], GAME_CONFIG['TILE_SIZE'])
            if player_rect.colliderect(bomb_rect):
                return False

        return True

    def render(self, screen: pygame.Surface):
        color = self.color
        # efeito visual de invencibilidade
        if self.is_invincible():
            color = COLORS['CYAN']
        pygame.draw.rect(screen, color, self.rect)
