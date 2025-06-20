"""Data models for Money Smartz game"""
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.age = 16
        self.education = "High School"
        self.job = None
        self.salary = 0
        self.cash = 50  # Starting cash
        self.bank_account = None
        self.credit_card = None
        self.debit_card = None
        self.credit_score = 650  # Starting credit score
        self.assets = []  # Cars, houses, etc.
        self.loans = []  # Student loans, mortgages, etc.
        self.family = []  # Spouse, children
        self.life_events = []  # History of major life events

class BankAccount:
    def __init__(self, account_type="Checking"):
        self.account_type = account_type
        self.balance = 0
        self.interest_rate = 0.01 if account_type == "Savings" else 0.0
        self.transaction_history = []

    def deposit(self, amount):
        """Deposit money into account"""
        self.balance += amount
        self.transaction_history.append(f"Deposit: ${amount}")
        return True

    def withdraw(self, amount):
        """Withdraw money from account"""
        if amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawal: ${amount}")
            return True
        return False

    def apply_interest(self):
        """Apply annual interest for savings accounts"""
        if self.account_type == "Savings":
            interest = self.balance * self.interest_rate
            self.balance += interest
            self.transaction_history.append(f"Interest: ${interest:.2f}")

class Card:
    def __init__(self, card_type, limit=0):
        self.card_type = card_type
        self.limit = limit
        self.balance = 0
        self.transaction_history = []

    def charge(self, amount):
        """Charge amount to card"""
        if self.card_type == "Credit":
            if self.balance + amount <= self.limit:
                self.balance += amount
                self.transaction_history.append(f"Charge: ${amount}")
                return True
            return False
        else:  # Debit card
            # Debit card is linked to bank account, handled elsewhere
            self.transaction_history.append(f"Charge: ${amount}")
            return True

    def pay(self, amount):
        """Make payment toward card balance"""
        if self.card_type == "Credit":
            if amount <= self.balance:
                self.balance -= amount
                self.transaction_history.append(f"Payment: ${amount}")
                return True
            return False
        return True  # No action needed for debit card

class Loan:
    def __init__(self, loan_type, amount, interest_rate, term_years):
        self.loan_type = loan_type
        self.original_amount = amount
        self.current_balance = amount
        self.interest_rate = interest_rate
        self.term_years = term_years
        self.monthly_payment = self.calculate_payment()
        self.payment_history = []

    def calculate_payment(self):
        """Calculate monthly payment amount"""
        monthly_rate = self.interest_rate / 12
        num_payments = self.term_years * 12
        return (self.original_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -num_payments)

    def make_payment(self, amount):
        """Make payment toward loan"""
        if amount >= self.monthly_payment:
            self.current_balance -= (amount - (self.monthly_payment * self.interest_rate / 12))
            self.payment_history.append(f"Payment: ${amount}")
            return True
        return False

class Asset:
    def __init__(self, asset_type, name, value, condition="Good"):
        self.asset_type = asset_type  # Car, House, etc.
        self.name = name
        self.purchase_value = value
        self.current_value = value
        self.condition = condition
        self.age = 0

    def age_asset(self):
        """Age asset and adjust value accordingly"""
        self.age += 1
        # Depreciate value based on type and age
        if self.asset_type == "Car":
            self.current_value *= 0.85  # 15% depreciation per year
        elif self.asset_type == "House":
            # Houses might appreciate
            appreciation = random.uniform(-0.05, 0.1)  # -5% to +10%
            self.current_value *= (1 + appreciation)

    def repair(self, cost):
        """Repair asset to good condition"""
        self.condition = "Good"
        return cost