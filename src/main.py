import pygame
import sys
from typing import Optional
from .game.game_engine import GameEngine
from .ui.menu import Menu
from .ui.score_display import ScoreDisplay
from .database.score_manager import ScoreManager
from .utils.constants import GAME_CONFIG


class BombermanApp:
    def __init__(self):
        pygame.init()
        self.screen_width = GAME_CONFIG['SCREEN_WIDTH']
        self.screen_height = GAME_CONFIG['SCREEN_HEIGHT']
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Bomberman")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.current_state = "menu"
        self.game_engine: Optional[GameEngine] = None
        self.score_manager = ScoreManager()
        
        self.menu = Menu(self.screen_width, self.screen_height)
        self.score_display = ScoreDisplay(self.screen_width, self.screen_height)
        
        self.player_name = ""
        self.is_entering_name = False
        
        self._setup_menu()
    
    def _setup_menu(self):
        self.menu.add_option("Start Game", self._start_game)
        self.menu.add_option("High Scores", self._show_high_scores)
        self.menu.add_option("Quit", self._quit_game)
    
    def _start_game(self):
        self.current_state = "game"
        self.game_engine = GameEngine(self.screen_width, self.screen_height)
    
    def _show_high_scores(self):
        self.current_state = "high_scores"
    
    def _quit_game(self):
        self.running = False
    
    def _back_to_menu(self):
        self.current_state = "menu"
        self.is_entering_name = False
        self.player_name = ""
    
    def _handle_menu_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._quit_game()
        else:
            self.menu.handle_events(event)
    
    def _handle_game_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.current_state = "menu"
            self.game_engine = None
        else:
            # >>> CORREÇÃO: repasse o evento diretamente para o engine (sem engine ler pygame.event.get())
            if self.game_engine:
                self.game_engine.handle_event(event)
    
    def _handle_high_scores_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._back_to_menu()
    
    def _handle_name_input_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.player_name.strip():
                    self.score_manager.add_score(self.player_name, self.game_engine.get_score())
                    self._back_to_menu()
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_ESCAPE:
                self._back_to_menu()
            elif event.unicode.isalnum() or event.unicode == ' ':
                if len(self.player_name) < 20:
                    self.player_name += event.unicode
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.current_state == "menu":
                self._handle_menu_events(event)
            elif self.current_state == "game":
                self._handle_game_events(event)
            elif self.current_state == "high_scores":
                self._handle_high_scores_events(event)
            elif self.current_state == "name_input":
                self._handle_name_input_events(event)
    
    def update(self):
        if self.current_state == "game" and self.game_engine:
            self.game_engine.update()
            
            if self.game_engine.is_game_over() or self.game_engine.is_victory():
                if self.score_manager.is_high_score(self.game_engine.get_score()):
                    self.current_state = "name_input"
                    self.is_entering_name = True
                else:
                    self.current_state = "menu"
                    self.game_engine = None
    
    def render(self):
        if self.current_state == "menu":
            self.menu.render(self.screen)
        elif self.current_state == "game" and self.game_engine:
            self.game_engine.render()
        elif self.current_state == "high_scores":
            high_scores = self.score_manager.get_high_scores()
            self.score_display.render_high_scores(self.screen, high_scores)
        elif self.current_state == "name_input":
            self.score_display.render_score_input(self.screen, 
                                                self.game_engine.get_score() if self.game_engine else 0,
                                                self.player_name)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(GAME_CONFIG['FPS'])
        
        pygame.quit()
        sys.exit()


def main():
    app = BombermanApp()
    app.run()


if __name__ == "__main__":
    main()
