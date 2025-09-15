import pygame
from typing import List, Callable
from ..utils.constants import COLORS


class Menu:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.selected_option = 0
        self.options = []
        self.actions = []
    
    def add_option(self, text: str, action: Callable):
        self.options.append(text)
        self.actions.append(action)
    
    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.actions[self.selected_option]:
                    self.actions[self.selected_option]()
    
    def render(self, screen: pygame.Surface):
        screen.fill(COLORS['BLACK'])
        
        title_text = self.font_large.render("BOMBERMAN", True, COLORS['WHITE'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_text, title_rect)
        
        for i, option in enumerate(self.options):
            color = COLORS['GREEN'] if i == self.selected_option else COLORS['WHITE']
            option_text = self.font_medium.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen_width // 2, 200 + i * 50))
            screen.blit(option_text, option_rect)
        
        instructions = [
            "Use ARROW KEYS to navigate",
            "Press ENTER to select",
            "In game: WASD/Arrow keys to move, SPACE to plant bomb"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, COLORS['GRAY'])
            inst_rect = inst_text.get_rect(center=(self.screen_width // 2, 400 + i * 30))
            screen.blit(inst_text, inst_rect)
