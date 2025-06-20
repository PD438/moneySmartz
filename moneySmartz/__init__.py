"""
Money Smartz: Financial Life Simulator

A 2D graphical financial education game inspired by the classic Oregon Trail.
This game simulates the financial journey of life, from your first bank account
as a teenager to retirement.
"""

# Export main modules
from .game import Game
from .models import Player, BankAccount, Card, Loan, Asset
from .ui import Button, TextInput, Screen, GUIManager

# Version information
__version__ = "1.0.0"
