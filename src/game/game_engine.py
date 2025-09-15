import pygame
import time
import random
from typing import List, Tuple, Optional

from .game_map import GameMap
from .player import Player
from .bomb import Bomb
from .enemy import Enemy
from .explosion import Explosion
from .powerup import PowerUp, PowerUpType
from ..utils.constants import GAME_CONFIG, COLORS


class GameEngine:
    def __init__(self, screen_width: int, screen_height: int):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Bomberman")

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.victory = False
        self.score = 0
        self.level = 1

        self.game_map = GameMap()
        self.player = Player(1, 1, GAME_CONFIG['PLAYER_SPEED'])
        self.enemies: List[Enemy] = []
        self.bombs: List[Bomb] = []
        self.explosions: List[Explosion] = []
        self.powerups: List[PowerUp] = []

        self.last_bomb_time = 0.0
        self.bomb_cooldown = GAME_CONFIG['BOMB_COOLDOWN']

        self._initialize_enemies()

    # ---------------------------------------------------------------------
    # Eventos: AGORA recebemos um evento por vez (sem pygame.event.get() aqui)
    # ---------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._plant_bomb()
            elif event.key == pygame.K_r and (self.game_over or self.victory):
                self._restart_game()

    # ---------------------------------------------------------------------
    def _initialize_enemies(self):
        enemy_positions = self.game_map.get_enemy_spawn_positions()
        for pos in enemy_positions:
            self.enemies.append(Enemy(pos[0], pos[1], GAME_CONFIG['ENEMY_SPEED']))

    def _restart_game(self):
        self.game_over = False
        self.victory = False
        self.score = 0
        self.level = 1

        self.player = Player(1, 1, GAME_CONFIG['PLAYER_SPEED'])
        self.enemies.clear()
        self.bombs.clear()
        self.explosions.clear()
        self.powerups.clear()

        self.game_map = GameMap()
        self._initialize_enemies()

    # ---------------------------------------------------------------------
    # Update principal
    # ---------------------------------------------------------------------
    def update(self):
        if self.game_over or self.victory:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys, self.game_map, self.bombs, self.player.soft_bomb_tile)

        # Se já saiu do tile da bomba recém-plantada, remove pass-through
        if self.player.soft_bomb_tile is not None:
            px, py = self.player.get_position()
            pgx, pgy = self.game_map.world_to_grid(px, py)
            if (pgx, pgy) != self.player.soft_bomb_tile:
                self.player.soft_bomb_tile = None

        # Inimigos
        for enemy in self.enemies[:]:
            enemy.update(self.game_map, self.player)
            if enemy.is_dead():
                self.enemies.remove(enemy)
                self.score += GAME_CONFIG['ENEMY_SCORE']

        # Bombas -> explosão
        for bomb in self.bombs[:]:
            bomb.update()
            if bomb.should_explode():
                tiles = bomb.get_explosion_positions(self.game_map)
                self._apply_destruction_and_spawn_powerups(tiles)
                self.explosions.append(Explosion(tiles))
                self.bombs.remove(bomb)

        # Limpa explosões expiradas
        self.explosions = [e for e in self.explosions if e.is_active()]

        # Coleta power-ups
        self._check_player_powerups()

        # Colisões (chamas / contato)
        self._check_collisions()

        # Vitória?
        self._check_victory_condition()

    # ---------------------------------------------------------------------
    def _plant_bomb(self):
        current_time = time.time()
        # capacidade: número de bombas ativas < capacidade do jogador
        if len(self.bombs) >= self.player.bomb_capacity:
            return
        if current_time - self.last_bomb_time < self.bomb_cooldown:
            return

        player_x, player_y = self.player.get_position()
        grid_x, grid_y = self.game_map.world_to_grid(player_x, player_y)

        # não planta em parede ou em tile com outra bomba
        if not self.game_map.can_place_bomb(grid_x, grid_y):
            return
        if any(b.grid_x == grid_x and b.grid_y == grid_y for b in self.bombs):
            return

        bomb = Bomb(grid_x, grid_y, GAME_CONFIG['BOMB_TIMER'])
        self.bombs.append(bomb)
        self.last_bomb_time = current_time

        # libera pass-through somente para o tile atual
        self.player.soft_bomb_tile = (grid_x, grid_y)

    def _apply_destruction_and_spawn_powerups(self, explosion_tiles: List[Tuple[int, int]]):
        for gx, gy in explosion_tiles:
            if not self.game_map.is_valid_position(gx, gy):
                continue
            if self.game_map.is_destructible_wall(gx, gy):
                self.game_map.destroy_wall(gx, gy)
                self.score += GAME_CONFIG['WALL_SCORE']
                # drop chance
                if random.random() < GAME_CONFIG['POWERUP_DROP_CHANCE']:
                    ptype = random.choice([PowerUpType.BOMB, PowerUpType.FIRE,
                                           PowerUpType.SPEED, PowerUpType.HEART])
                    self.powerups.append(PowerUp(gx, gy, ptype))

    def _check_player_powerups(self):
        px, py = self.player.get_position()
        pgx, pgy = self.game_map.world_to_grid(px, py)
        for pu in self.powerups[:]:
            if (pu.grid_x, pu.grid_y) == (pgx, pgy):
                pu.apply_to(self.player)
                self.powerups.remove(pu)

    def _damage_player(self):
        if self.player.is_invincible():
            return
        self.player.lives -= 1
        if self.player.lives <= 0:
            self.game_over = True
            return
        # respawn
        self.player.x, self.player.y = self.game_map.grid_to_world(1, 1)
        self.player.rect.x = int(self.player.x)
        self.player.rect.y = int(self.player.y)
        self.player.grant_invincibility(GAME_CONFIG['PLAYER_INVINCIBILITY_TIME'])

    def _check_collisions(self):
        # contato com inimigo (pode desligar se quiser)
        px, py = self.player.get_position()
        pgx, pgy = self.game_map.world_to_grid(px, py)

        for enemy in self.enemies[:]:
            ex, ey = enemy.get_position()
            egx, egy = self.game_map.world_to_grid(ex, ey)
            if (pgx, pgy) == (egx, egy):
                self._damage_player()
                break

        # chamas atingem jogador e inimigos
        if any(expl.contains(pgx, pgy) for expl in self.explosions):
            self._damage_player()

        for enemy in self.enemies[:]:
            egx, egy = self.game_map.world_to_grid(*enemy.get_position())
            if any(expl.contains(egx, egy) for expl in self.explosions):
                enemy.take_damage()
                if enemy.is_dead():
                    self.enemies.remove(enemy)
                    self.score += GAME_CONFIG['ENEMY_SCORE']

    def _check_victory_condition(self):
        if len(self.enemies) == 0:
            self.victory = True
            self.score += GAME_CONFIG['LEVEL_COMPLETE_BONUS']

    # ---------------------------------------------------------------------
    # Render
    # ---------------------------------------------------------------------
    def render(self):
        self.screen.fill(COLORS['BLACK'])
        self.game_map.render(self.screen)

        # power-ups (chão), bombas, explosões, inimigos, jogador
        for pu in self.powerups:
            pu.render(self.screen)
        for bomb in self.bombs:
            bomb.render(self.screen)
        for expl in self.explosions:
            expl.render(self.screen)
        for enemy in self.enemies:
            enemy.render(self.screen)
        self.player.render(self.screen)

        self._render_ui()
        pygame.display.flip()

    def _render_ui(self):
        font = pygame.font.Font(None, 36)

        score_text = font.render(f"Score: {self.score}", True, COLORS['WHITE'])
        level_text = font.render(f"Level: {self.level}", True, COLORS['WHITE'])

        # status do player
        status_text = font.render(
            f"Lives: {self.player.lives}  Bombs: {len(self.bombs)}/{self.player.bomb_capacity}  Fire: {self.player.flame_radius}",
            True, COLORS['WHITE']
        )

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 44))
        self.screen.blit(status_text, (10, 78))

        if self.game_over:
            go_text = font.render("GAME OVER - Press R to restart", True, COLORS['RED'])
            rect = go_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(go_text, rect)

        if self.victory:
            vc_text = font.render("VICTORY! - Press R to restart", True, COLORS['GREEN'])
            rect = vc_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(vc_text, rect)

    # ---------------------------------------------------------------------
    def run(self):
        while self.running:
            # mantive por compat: se alguém chamar run direto
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)
            self.update()
            self.render()
            self.clock.tick(GAME_CONFIG['FPS'])

        pygame.quit()

    def get_score(self) -> int:
        return self.score

    def is_game_over(self) -> bool:
        return self.game_over

    def is_victory(self) -> bool:
        return self.victory
