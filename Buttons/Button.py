import pygame

class Button:
    def __init__(self, pos, size, color, screen, button_sprite=None, text='', font_size=20,text_color=(0, 0, 0), on_click=None):
        self.screen = screen
        self.button_sprite = button_sprite
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.font = pygame.font.Font(None, self.font_size)
        self.on_click = on_click
        self.hovered = False

    def update(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.on_click:
                        self.on_click()

    def draw(self, surface):
        draw_color = tuple(min(255, c + 30) if self.hovered else c for c in self.color)

        if self.button_sprite:
            surface.blit(self.button_sprite, self.rect.topleft)
        else:
            pygame.draw.rect(surface, draw_color, self.rect, border_radius=30)

        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
