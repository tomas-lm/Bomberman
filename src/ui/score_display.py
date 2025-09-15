import pygame
from typing import List, Tuple
from ..utils.constants import COLORS


class ScoreDisplay:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
    
    def render_high_scores(self, screen: pygame.Surface, high_scores: List[Tuple[str, int]]):
        screen.fill(COLORS['BLACK'])
        
        title_text = self.font_large.render("HIGH SCORES", True, COLORS['WHITE'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        screen.blit(title_text, title_rect)
        
        if not high_scores:
            no_scores_text = self.font_medium.render("No scores yet!", True, COLORS['GRAY'])
            no_scores_rect = no_scores_text.get_rect(center=(self.screen_width // 2, 200))
            screen.blit(no_scores_text, no_scores_rect)
        else:
            for i, (player_name, score) in enumerate(high_scores[:10]):
                rank = i + 1
                color = COLORS['GREEN'] if rank <= 3 else COLORS['WHITE']
                
                rank_text = self.font_medium.render(f"{rank}.", True, color)
                name_text = self.font_medium.render(player_name, True, color)
                score_text = self.font_medium.render(str(score), True, color)
                
                y_pos = 120 + i * 35
                
                screen.blit(rank_text, (150, y_pos))
                screen.blit(name_text, (200, y_pos))
                screen.blit(score_text, (500, y_pos))
        
        back_text = self.font_small.render("Press ESC to go back", True, COLORS['GRAY'])
        back_rect = back_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(back_text, back_rect)
    
    def render_score_input(self, screen: pygame.Surface, score: int, player_name: str):
        screen.fill(COLORS['BLACK'])
        
        title_text = self.font_large.render("NEW HIGH SCORE!", True, COLORS['GREEN'])
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)
        
        score_text = self.font_medium.render(f"Score: {score}", True, COLORS['WHITE'])
        score_rect = score_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(score_text, score_rect)
        
        name_prompt = self.font_medium.render("Enter your name:", True, COLORS['WHITE'])
        name_prompt_rect = name_prompt.get_rect(center=(self.screen_width // 2, 250))
        screen.blit(name_prompt, name_prompt_rect)
        
        name_display = self.font_medium.render(player_name + "_", True, COLORS['GREEN'])
        name_display_rect = name_display.get_rect(center=(self.screen_width // 2, 300))
        screen.blit(name_display, name_display_rect)
        
        instruction_text = self.font_small.render("Type your name and press ENTER", True, COLORS['GRAY'])
        instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, 350))
        screen.blit(instruction_text, instruction_rect)
