"""Game logic and controller for Money Smartz"""
import random
from .models import Player, BankAccount, Card, Loan, Asset
from .screens import TitleScreen

class Game:
    """Main game controller class"""
    def __init__(self):
        self.player = None
        self.current_month = 1
        self.current_year = 0
        self.game_over = False
        self.events = self.initialize_events()
        self.gui_manager = None

    def initialize_events(self):
        """Initialize possible random events"""
        return {
            "positive": [
                {"name": "Tax Refund", "description": "You received a tax refund!", "cash_effect": lambda: random.randint(100, 1000)},
                {"name": "Birthday Gift", "description": "You received money as a birthday gift!", "cash_effect": lambda: random.randint(20, 200)},
                {"name": "Found Money", "description": "You found money on the ground!", "cash_effect": lambda: random.randint(5, 50)},
                {"name": "Bonus", "description": "You received a bonus at work!", "cash_effect": lambda: int(self.player.salary * random.uniform(0.01, 0.1)) if self.player.salary > 0 else 0},
            ],
            "negative": [
                {"name": "Car Repair", "description": "Your car needs repairs.", "cash_effect": lambda: -random.randint(100, 2000) if any(a.asset_type == "Car" for a in self.player.assets) else 0},
                {"name": "Medical Bill", "description": "You have unexpected medical expenses.", "cash_effect": lambda: -random.randint(50, 5000)},
                {"name": "Lost Wallet", "description": "You lost your wallet!", "cash_effect": lambda: -min(50, self.player.cash)},
                {"name": "Phone Repair", "description": "Your phone screen cracked.", "cash_effect": lambda: -random.randint(50, 300)},
            ]
        }

    def process_monthly_finances(self):
        """Process monthly income and expenses"""
        # Process income
        if self.player and self.player.job:
            monthly_income = self.player.salary / 12
            self.player.cash += monthly_income

            # Auto deposit to bank if account exists
            if self.player.bank_account:
                self.player.bank_account.deposit(monthly_income * 0.8)
                self.player.cash -= monthly_income * 0.8

        # Process loan payments
        if self.player:
            for loan in self.player.loans:
                if self.player.cash >= loan.monthly_payment:
                    self.player.cash -= loan.monthly_payment
                    loan.make_payment(loan.monthly_payment)
                elif self.player.bank_account and self.player.bank_account.balance >= loan.monthly_payment:
                    self.player.bank_account.withdraw(loan.monthly_payment)
                    loan.make_payment(loan.monthly_payment)
                else:
                    # Missed payment - credit score impact
                    self.player.credit_score -= 20

        # Process credit card payments
        if self.player and self.player.credit_card and self.player.credit_card.balance > 0:
            min_payment = max(25, self.player.credit_card.balance * 0.03)
            if self.player.cash >= min_payment:
                self.player.cash -= min_payment
                self.player.credit_card.pay(min_payment)
            elif self.player.bank_account and self.player.bank_account.balance >= min_payment:
                self.player.bank_account.withdraw(min_payment)
                self.player.credit_card.pay(min_payment)
            else:
                self.player.credit_score -= 30

    def end_game_gui(self, reason):
        """End game and show final stats (GUI version)"""
        if self.gui_manager:
            from .screens import EndGameScreen  # Local import to avoid circular dependency
            self.game_over = True
            self.gui_manager.set_screen(EndGameScreen(self, reason))

    def check_life_stage_events_gui(self):
        """Check for life stage events and show appropriate screens"""
        if not self.player:
            return False
            
        # Retirement event
        if self.player.age >= 65:
            self.end_game_gui("retirement")
            return True
        return False