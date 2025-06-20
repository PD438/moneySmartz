"""End game screen implementation"""
import pygame
from ..ui import Screen, Button
from ..constants import *

class EndGameScreen(Screen):
    """Screen shown at game end"""
    def __init__(self, game, reason):
        super().__init__(game)
        self.reason = reason
        self.font = pygame.font.SysFont('Arial', FONT_MEDIUM)
        self.title_font = pygame.font.SysFont('Arial', FONT_LARGE, bold=True)
        self.calculate_net_worth()

        quit_button = Button(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT - 100, 
            200, 60, 
            "Quit Game", 
            color=RED,
            hover_color=LIGHT_RED,
            action=lambda: setattr(game.gui_manager, 'running', False)
        )

        new_game_button = Button(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT - 180, 
            200, 60, 
            "New Game", 
            action=lambda: game.gui_manager.set_screen(TitleScreen(game))
        )

        self.buttons = [new_game_button, quit_button]

    def calculate_net_worth(self):
        """Calculate player's final net worth"""
        if not self.game.player:
            return
            
        self.cash = self.game.player.cash
        self.bank_balance = self.game.player.bank_account.balance if self.game.player.bank_account else 0
        self.credit_card_debt = self.game.player.credit_card.balance if self.game.player.credit_card else 0

        self.loan_debt = 0
        for loan in self.game.player.loans:
            self.loan_debt += loan.current_balance

        self.asset_value = 0
        for asset in self.game.player.assets:
            self.asset_value += asset.current_value

        self.net_worth = self.cash + self.bank_balance - self.credit_card_debt - self.loan_debt + self.asset_value

        # Financial rating
        if self.net_worth >= 1000000:
            self.rating = "Financial Wizard"
        elif self.net_worth >= 500000:
            self.rating = "Financially Secure"
        elif self.net_worth >= 100000:
            self.rating = "Financially Stable"
        elif self.net_worth >= 0:
            self.rating = "Breaking Even"
        else:
            self.rating = "In Debt"

    def draw(self, surface):
        if not self.game.player:
            return
            
        surface.fill(WHITE)
        # ... rest of drawing logic ...