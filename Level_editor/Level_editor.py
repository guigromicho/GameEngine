import pygame
import os
from Tile import Tile
import json

class LevelEditor:
    def __init__(self):
        pygame.init()
        #Screen setup
        self.map_width = 1000
        self.sidebar_width = 200
        self.width = 1000 + self.sidebar_width
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Level Editor")
        self.bg_color = (50,50,50)
        self.font = pygame.font.SysFont(None, 24)
        
        #update setup
        self.clock = pygame.time.Clock()
        self.running = True
        
        #grid setup
        self.tile_size = 32
        self.cols = self.map_width // self.tile_size
        self.rows = self.height // self.tile_size
        self.grid = {}
        self.sprites = {}
        self.selected_sprite = None
        self.ui_tile_size = 48
        self.show_grid = True
        
        #sidebar setup
        self.sidebar_x = self.map_width
        self.sidebar_padding = 10
        self.sidebar_scroll = 0
        self.scroll_speed = 30
        self.assets_to_load = [
            "GameEngine/Assets/Grass_tile",
            "GameEngine/Assets/Stone_tile"
        ]

        #load assets and create grid
        self.layer = 0
        self.create_grid()
        for p in self.assets_to_load:
            self.load_images(p)

        self.level_editor_state = "chose level"

        self.input_box = pygame.Rect(self.width//2 - 150, 200, 300, 40)
        self.input_active = False
        self.input_text = ""
        self.filename = ""

    def start(self):
        while self.running:
            self.update()
        pygame.quit()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.handle_events(mouse_pos)
        for tile in self.grid.values():
            tile.update(mouse_pos)
        self.draw()
        self.clock.tick(60)

    def chose_create_level(self):
        self.screen.fill((30, 30, 30))
        font = pygame.font.SysFont(None, 36)

        label = font.render("Choose / Create Level", True, (200, 200, 200))
        self.screen.blit(label, (self.width//2 - label.get_width()//2, 100))

        color = (255, 255, 255) if self.input_active else (150, 150, 150)
        pygame.draw.rect(self.screen, color, self.input_box)

        txt_surface = font.render(self.input_text, True, (100, 100, 100))
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        
        pygame.display.flip()
    
    def editing(self):
        self.screen.fill(self.bg_color)
        self.draw_level()
        self.draw_sprite_menu()
        self.draw_selected_preview()

        texto = self.font.render(str(self.layer), True, (255, 255, 255))
        self.screen.blit(texto, (10, 10))
        pygame.display.flip()
    
    def draw(self):
        if self.level_editor_state == "chose level":
            self.chose_create_level()
        if self.level_editor_state == "editing":
            self.editing()

    def mouse_whell_scroll(self, event, mouse_pos):
        if mouse_pos[0] >= self.sidebar_x:
            self.sidebar_scroll -= event.y * self.scroll_speed
            max_scroll = 0
            min_scroll = -max(0, self.get_sidebar_content_height() - self.height + 40)
            self.sidebar_scroll = max(min(self.sidebar_scroll, max_scroll), min_scroll)

    def handle_events(self, mouse_pos):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEWHEEL:
                self.mouse_whell_scroll(event, mouse_pos)

            if self.level_editor_state == "chose level":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.input_active = self.input_box.collidepoint(mouse_pos)

                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        filename = os.path.join("GameEngine/Levels", self.input_text + ".json")
                        print("Loading:", filename)
                        
                        if not os.path.exists(filename):
                            with open(filename, "w", encoding="utf8") as f:
                                f.write("[]")

                        self.load_map(filename)
                        self.level_editor_state = "editing"

                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]

                    else:
                        self.input_text += event.unicode
                return
            elif self.level_editor_state == "editing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.save_map()
                        self.level_editor_state = "chose level"
                        self.input_text = ""
                        self.input_active = False
                    elif event.key == pygame.K_UP:
                        self.layer +=1
                    elif event.key == pygame.K_DOWN:
                        self.layer -=1


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and mouse_pos[0] >= self.sidebar_x:
                    self.check_sprite_menu_click(mouse_pos)

                elif event.button == 1 and mouse_pos[0] < self.sidebar_x:
                    tile = self.get_tile_at_mouse(mouse_pos)
                    if tile:
                        tile.on_left_click()

                elif event.button == 2:
                    tile = self.get_tile_at_mouse(mouse_pos)
                    if tile:
                        sprite = tile.sprite
                        if sprite:
                            print("Selected sprite from tile ", sprite)
                            self.selected_sprite = tile.sprite_key

                if event.button == 3 and mouse_pos[0] < self.sidebar_x:
                    tile = self.get_tile_at_mouse(mouse_pos)
                    if tile:
                        tile.sprite = None
                        tile.sprite_key = None

            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()

                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    print("Map saved.")
                    self.save_map()

                if event.key == pygame.K_h:
                    self.show_grid = not self.show_grid
                    print("show_grid:", self.show_grid)

        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0] and mouse_pos[0] < self.sidebar_x:
            tile = self.get_tile_at_mouse(mouse_pos)
            if tile:
                tile.on_left_click()

        if mouse_buttons[2] and mouse_pos[0] < self.sidebar_x:
            tile = self.get_tile_at_mouse(mouse_pos)
            if tile:
                tile.sprite = None
                tile.sprite_key = None

    def get_tile_at_mouse(self, mouse_pos):
        x = mouse_pos[0] // self.tile_size
        y = mouse_pos[1] // self.tile_size
        return self.grid.get((x,y))

    def create_grid(self):
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid[(x,y)] = Tile(self, (x,y), layer=0)

    def load_sprites_from_folder(self, folder_path):
        sprites = {}
        if not os.path.isdir(folder_path):
            return sprites
        for filename in sorted(os.listdir(folder_path)):
            full = os.path.join(folder_path, filename)
            if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            try:
                image = pygame.image.load(full).convert_alpha()
                key = os.path.splitext(filename)[0]
                sprites[key] = image
            except Exception:
                pass
        return sprites

    def load_images(self, folder):
        folder_name = os.path.basename(folder.rstrip("/\\"))
        loaded = self.load_sprites_from_folder(folder)
        if loaded:
            if folder_name in self.sprites:
                for k,v in loaded.items():
                    self.sprites[folder_name][k] = v
            else:
                self.sprites[folder_name] = loaded

    def get_sidebar_content_height(self):
        h = 30
        for folder, imgs in self.sprites.items():
            h += 20
            h += len(imgs) * (self.ui_tile_size + self.sidebar_padding)
            h += 6
        return h + 40

    def draw_sprite_menu(self):
        pygame.draw.rect(self.screen, (30,30,30), (self.sidebar_x, 0, self.sidebar_width, self.height))
        x = self.sidebar_x + self.sidebar_padding
        y = 10 + self.sidebar_scroll
        font = pygame.font.SysFont(None, 20)
        title = font.render("Sprites", True, (220,220,220))
        self.screen.blit(title, (x, 6))
        y += 22
        for folder, sprites in self.sprites.items():
            label = font.render(folder, True, (200,200,200))
            self.screen.blit(label, (x, y))
            y += 20
            for name, surf in sprites.items():
                draw_rect = pygame.Rect(x, y, self.ui_tile_size, self.ui_tile_size)
                pygame.draw.rect(self.screen, (50,50,50), draw_rect)
                try:
                    icon = pygame.transform.scale(surf, (self.ui_tile_size, self.ui_tile_size))
                    self.screen.blit(icon, draw_rect.topleft)
                except Exception:
                    pass
                if self.selected_sprite == (folder, name):
                    pygame.draw.rect(self.screen, (255,215,0), draw_rect, 3)
                nm = name if len(name) <= 12 else name[:10] + "..."
                label2 = font.render(nm, True, (180,180,180))
                self.screen.blit(label2, (x + self.ui_tile_size + 6, y + self.ui_tile_size//2 - 8))
                y += self.ui_tile_size + self.sidebar_padding
            y += 6

    def check_sprite_menu_click(self, mouse_pos):
        mx, my = mouse_pos
        x = self.sidebar_x + self.sidebar_padding
        y = 10 + self.sidebar_scroll + 22
        for folder, sprites in self.sprites.items():
            y += 20
            for name, surf in sprites.items():
                r = pygame.Rect(x, y, self.ui_tile_size, self.ui_tile_size)
                if r.collidepoint(mx, my):
                    self.selected_sprite = (folder, name)
                    return
                y += self.ui_tile_size + self.sidebar_padding
            y += 6

    def draw_selected_preview(self):
        font = pygame.font.SysFont(None, 20)
        px = self.sidebar_x + self.sidebar_padding
        py = self.height - 80
        pygame.draw.rect(self.screen, (40,40,40), (px, py, self.sidebar_width - self.sidebar_padding*2, 70))
        label = font.render("Selected:", True, (200,200,200))
        self.screen.blit(label, (px + 4, py + 4))
        if self.selected_sprite:
            folder, name = self.selected_sprite
            surf = self.sprites.get(folder, {}).get(name)
            if surf:
                scaled = pygame.transform.scale(surf, (48,48))
                self.screen.blit(scaled, (px + 6, py + 20))
            name_label = font.render(name, True, (200,200,200))
            self.screen.blit(name_label, (px + 60, py + 30))
        else:
            none = font.render("None", True, (150,150,150))
            self.screen.blit(none, (px + 6, py + 30))
    
    def save_map(self):
        levels_folder = "GameEngine/Levels"
        os.makedirs(levels_folder, exist_ok=True)

        filename = os.path.join(levels_folder, self.input_text + ".json")

        data = []
        for (x, y), tile in sorted(self.grid.items()):
            if tile.sprite_key and tile.sprite:
                folder, name = tile.sprite_key
                data.append({
                    "x": x,
                    "y": y,
                    "folder": folder,
                    "name": name,
                    "layer": tile.layer
                })

        with open(filename, "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("Mapa salvo:", filename)

    def load_map(self, filename):
        for tile in self.grid.values():
            tile.sprite = None
            tile.sprite_key = None
            tile.layer = 0

        with open(filename, "r", encoding="utf8") as f:
            data = json.load(f)

        for cell in data:
            x = cell["x"]
            y = cell["y"]
            folder = cell["folder"]
            name = cell["name"]
            layer = cell.get("layer", 0)

            if (x, y) in self.grid:
                tile = self.grid[(x, y)]
                tile.sprite_key = (folder, name)
                tile.layer = layer

        for tile in self.grid.values():
            if tile.sprite_key:
                folder, name = tile.sprite_key
                tile.sprite = self.sprites.get(folder, {}).get(name)

        print("Mapa carregado:", filename)
        self.level_editor_state = "editing"

    def draw_level(self):
        for tile in self.grid.values():
            if tile.layer == self.layer:
                tile.draw()

if __name__ == "__main__":
    LevelEditor().start()