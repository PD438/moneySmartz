"""Title screen implementation"""
import pygame
from ..ui import Screen, Button
from ..constants import *

class TitleScreen(Screen):
    """Initial title screen"""
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont('Arial', FONT_TITLE, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', FONT_MEDIUM)

        # Create buttons
        start_button = Button(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT // 2, 
            200, 60, 
            "Start Game", 
            action=lambda: game.gui_manager.set_screen(NameInputScreen(game))
        )

        quit_button = Button(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT // 2 + 100, 
            200, 60, 
            "Quit", 
            color=RED,
            hover_color=LIGHT_RED,
            action=lambda: setattr(game.gui_manager, 'running', False)
        )

        self.buttons = [start_button, quit_button]

    def draw(self, surface):
        surface.fill(WHITE)

        # Draw title
        title_text = self.title_font.render("MONEY SMARTZ", True, BLUE)
        subtitle_text = self.subtitle_font.render("Financial Life Simulator", True, BLACK)

        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60))

        surface.blit(title_text, title_rect)
        surface.blit(subtitle_text, subtitle_rect)

        # Draw tagline
        tagline_font = pygame.font.SysFont('Arial', FONT_SMALL)
        tagline_text = tagline_font.render("Inspired by the classic Oregon Trail", True, DARK_GRAY)
        tagline_rect = tagline_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))
        surface.blit(tagline_text, tagline_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)