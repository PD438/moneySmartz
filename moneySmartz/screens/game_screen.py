"""Main game screen implementation"""
import random
import pygame
from ..ui import Screen, Button
from ..constants import *

class GameScreen(Screen):
    """Main gameplay screen"""
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('Arial', FONT_MEDIUM)
        self.title_font = pygame.font.SysFont('Arial', FONT_LARGE, bold=True)
        self.small_font = pygame.font.SysFont('Arial', FONT_SMALL)
        self.create_buttons()

    def create_buttons(self):
        """Create dynamic buttons based on game state"""
        self.buttons = []
        continue_button = Button(
            SCREEN_WIDTH - 220, 
            SCREEN_HEIGHT - 70, 
            200, 50, 
            "Continue to next month", 
            action=self.continue_to_next_month
        )
        self.buttons.append(continue_button)

        # Dynamic buttons based on player state
        button_y = 400
        button_height = 50
        button_spacing = 10

        # Banking actions
        if not self.game.player.bank_account:
            self.buttons.append(Button(
                20, button_y, 250, button_height, 
                "Open a bank account", 
                action=lambda: self.game.gui_manager.set_screen(BankAccountScreen(self.game))
            ))
        # ... rest of button creation logic ...

    def continue_to_next_month(self):
        """Advance to next month"""
        if not self.game.player:
            return
            
        # Advance time
        self.game.current_month += 1
        if self.game.current_month > 12:
            self.game.current_month = 1
            self.game.current_year += 1
            self.game.player.age += 1

            # Apply interest to savings
            if self.game.player.bank_account and self.game.player.bank_account.account_type == "Savings":
                self.game.player.bank_account.apply_interest()

            # Age assets
            for asset in self.game.player.assets:
                asset.age_asset()

        # Process monthly finances
        self.game.process_monthly_finances()

        # Random events
        if random.random() < 0.3:  # 30% chance of an event each month
            event_type = "positive" if random.random() < 0.5 else "negative"
            event = random.choice(self.game.events[event_type])
            cash_effect = event["cash_effect"]()
            self.game.gui_manager.set_screen(RandomEventScreen(self.game, event, cash_effect))
            return

        # Life stage events
        if self.game.check_life_stage_events_gui():
            return

        # Refresh the screen with updated info
        self.create_buttons()

    def draw(self, surface):
        """Draw game screen"""
        if not self.game.player:
            return
            
        surface.fill(WHITE)
        # ... rest of drawing logic ...

    def draw_text(self, surface, text, x, y, is_title=False):
        """Helper for drawing text"""
        font = self.title_font if is_title else self.font
        text_surface = font.render(text, True, BLACK)
        surface.blit(text_surface, (x, y))

class RandomEventScreen(Screen):
    """Screen for random life events"""
    def __init__(self, game, event, cash_effect):
        super().__init__(game)
        self.event = event
        self.cash_effect = cash_effect
        self.font = pygame.font.SysFont('Arial', FONT_MEDIUM)
        self.title_font = pygame.font.SysFont('Arial', FONT_LARGE, bold=True)
        self.process_event()

        continue_button = Button(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT - 100, 
            200, 60, 
            "Continue", 
            action=lambda: game.gui_manager.set_screen(GameScreen(game))
        )
        self.buttons = [continue_button]

    def process_event(self):
        """Process event effects"""
        if self.cash_effect > 0:
            self.game.player.cash += self.cash_effect
            self.result_message = f"You received ${self.cash_effect}!"
            self.message_color = GREEN
        else:
            self.result_message = f"This costs you ${abs(self.cash_effect)}."
            cost = abs(self.cash_effect)
            
            if self.game.player.cash >= cost:
                self.game.player.cash -= cost
                self.payment_message = "You paid in cash."
            elif (self.game.player.bank_account and 
                  self.game.player.bank_account.balance >= cost):
                self.game.player.bank_account.withdraw(cost)
                self.payment_message = "You paid using your bank account."
            elif (self.game.player.credit_card and 
                  (self.game.player.credit_card.balance + cost) <= self.game.player.credit_card.limit):
                self.game.player.credit_card.charge(cost)
                self.payment_message = "You paid using your credit card."
            else:
                self.game.player.credit_score = max(300, self.game.player.credit_score - 15)
                self.payment_message = "You couldn't afford this expense! Your credit score has been affected."

    def draw(self, surface):
        surface.fill(WHITE)
        # ... rest of drawing logic ...