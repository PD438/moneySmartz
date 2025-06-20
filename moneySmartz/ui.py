"""UI components for Money Smartz"""
import pygame
from pygame.locals import *
from .constants import *

class Button:
    """Interactive button UI component"""
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=LIGHT_BLUE, 
                 text_color=WHITE, font_size=FONT_MEDIUM, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont('Arial', font_size)
        self.action = action
        self.hovered = False

    def draw(self, surface):
        """Draw button on surface"""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos, mouse_click):
        """Update button state and handle clicks"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_click and self.action:
            return self.action
        return None

class TextInput:
    """Text input field UI component"""
    def __init__(self, x, y, width, height, font_size=FONT_MEDIUM, max_length=20, initial_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = initial_text
        self.font = pygame.font.SysFont('Arial', font_size)
        self.active = False
        self.max_length = max_length

    def draw(self, surface):
        """Draw text input on surface"""
        color = LIGHT_BLUE if self.active else WHITE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        surface.blit(text_surface, text_rect)

    def update(self, events):
        """Update text input with events"""
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)

            if event.type == KEYDOWN and self.active:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == K_RETURN:
                    self.active = False
                elif len(self.text) < self.max_length:
                    self.text += event.unicode
        return self.text

class Screen:
    """Base class for all game screens"""
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.next_screen = None

    def handle_events(self, events):
        """Handle events for the screen"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        for button in self.buttons:
            action = button.update(mouse_pos, mouse_click)
            if action:
                return action
        return None

    def update(self):
        """Update screen state"""
        pass

    def draw(self, surface):
        """Draw screen content"""
        surface.fill(WHITE)
        for button in self.buttons:
            button.draw(surface)

class GUIManager:
    """Manages GUI screens and rendering"""
    def __init__(self, game):
        self.game = game
        try:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Money Smartz: Financial Life Simulator")
        except pygame.error as e:
            print(f"Display initialization failed: {e}")
            raise
        self.clock = pygame.time.Clock()
        self.current_screen = None
        self.running = True

    def set_screen(self, screen):
        """Set current active screen"""
        self.current_screen = screen

    def run(self):
        """Main GUI loop"""
        while self.running:
            try:
                events = pygame.event.get()
                for event in events:
                    if event.type == QUIT:
                        self.running = False

                if self.current_screen:
                    action = self.current_screen.handle_events(events)
                    if action:
                        action()

                    self.current_screen.update()
                    self.current_screen.draw(self.screen)

                pygame.display.flip()
                self.clock.tick(FPS)
            except Exception as e:
                print(f"Error in game loop: {e}")
                import traceback
                traceback.print_exc()
                self.running = False

        pygame.quit()
        sys.exit()