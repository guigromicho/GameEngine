import pygame

class Tile:
    def __init__(self, editor, grid_pos, layer ,sprite=None):
        self.editor = editor
        self.grid_pos = grid_pos

        self.sprite = sprite
        self.sprite_key = None

        self.rect = pygame.Rect(
            grid_pos[0] * editor.tile_size,
            grid_pos[1] * editor.tile_size,
            editor.tile_size + 1,
            editor.tile_size + 1,
        )
        self.layer = 0

        self.hover = False

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def draw(self):
        if self.layer != self.editor.layer:
            return
        if self.sprite:
            img = pygame.transform.scale(self.sprite, (self.editor.tile_size + 1, self.editor.tile_size + 1))
            self.editor.screen.blit(img, (self.rect.x, self.rect.y))

            if self.hover:
                pygame.draw.rect(self.editor.screen, (200, 200, 200), self.rect, 2)

    def on_left_click(self):
        if self.editor.selected_sprite:
            folder, name = self.editor.selected_sprite

            self.sprite = self.editor.sprites[folder][name]
            self.sprite_key = (folder, name)
            self.layer = self.editor.layer
