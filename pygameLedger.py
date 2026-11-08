import pygame
import sys

# Initialize Pygame
pygame.init()

# Display settings
WIDTH, HEIGHT = 820, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Filter & Sortable Dictionary Viewer")

# Colors
BG_COLOR = (35, 38, 46)
HEADER_BG = (55, 60, 75)
ROW_EVEN = (45, 49, 60)
ROW_ODD = (40, 44, 54)
WHITE = (240, 240, 240)
ACCENT = (100, 180, 255)
DROPDOWN_BG = (65, 70, 85)
DROPDOWN_HOVER = (85, 95, 115)
BORDER = (110, 115, 130)

# Fonts
font = pygame.font.SysFont("Arial", 19)
bold_font = pygame.font.SysFont("Arial", 19, bold=True)
title_font = pygame.font.SysFont("Arial", 26, bold=True)


class Dropdown:
    """A reusable UI dropdown widget built with pygame.Rect."""
    def __init__(self, x, y, w, h, options, default_index=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected_index = default_index
        self.is_open = False
        self.option_rects = [
            pygame.Rect(x, y + (i + 1) * h, w, h) for i in range(len(options))
        ]

    @property
    def selected_value(self):
        return self.options[self.selected_index]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return True
            elif self.is_open:
                for i, opt_rect in enumerate(self.option_rects):
                    if opt_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.is_open = False
                        return True
                self.is_open = False
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, DROPDOWN_BG, self.rect, border_radius=4)
        pygame.draw.rect(surface, BORDER, self.rect, 2, border_radius=4)

        arrow = "▲" if self.is_open else "▼"
        label = font.render(f"{self.selected_value}  {arrow}", True, WHITE)
        surface.blit(label, (self.rect.x + 10, self.rect.y + 8))

        if self.is_open:
            mouse_pos = pygame.mouse.get_pos()
            for i, opt_rect in enumerate(self.option_rects):
                color = DROPDOWN_HOVER if opt_rect.collidepoint(mouse_pos) else DROPDOWN_BG
                pygame.draw.rect(surface, color, opt_rect)
                pygame.draw.rect(surface, BORDER, opt_rect, 1)
                opt_text = font.render(self.options[i], True, WHITE)
                surface.blit(opt_text, (opt_rect.x + 10, opt_rect.y + 8))


# Sample Data with two categorical fields ("type" and "rarity")
raw_data = [
    {"id": 1, "name": "Iron Sword", "type": "Weapon", "rarity": "Common", "value": 150},
    {"id": 2, "name": "Oak Shield", "type": "Armor", "rarity": "Common", "value": 90},
    {"id": 3, "name": "Health Potion", "type": "Consumable", "rarity": "Common", "value": 50},
    {"id": 4, "name": "Fire Staff", "type": "Weapon", "rarity": "Rare", "value": 320},
    {"id": 5, "name": "Steel Plate", "type": "Armor", "rarity": "Rare", "value": 450},
    {"id": 6, "name": "Mana Elixir", "type": "Consumable", "rarity": "Uncommon", "value": 75},
    {"id": 7, "name": "Shadow Dagger", "type": "Weapon", "rarity": "Epic", "value": 610},
    {"id": 8, "name": "Dragon Scale", "type": "Armor", "rarity": "Epic", "value": 850},
]

# Extract unique options dynamically for both fields
unique_types = ["All"] + sorted(list(set(item["type"] for item in raw_data)))
unique_rarities = ["All"] + sorted(list(set(item["rarity"] for item in raw_data)))

# Initialize two Dropdown widgets
type_dropdown = Dropdown(390, 25, 165, 36, unique_types)
rarity_dropdown = Dropdown(615, 25, 165, 36, unique_rarities)
dropdowns = [type_dropdown, rarity_dropdown]

# Table Column Configuration
columns = [
    {"key": "id", "label": "ID", "x": 40, "w": 70},
    {"key": "name", "label": "Name", "x": 110, "w": 220},
    {"key": "type", "label": "Type", "x": 330, "w": 150},
    {"key": "rarity", "label": "Rarity", "x": 480, "w": 150},
    {"key": "value", "label": "Value", "x": 630, "w": 150},
]

header_y = 90
header_height = 40
for col in columns:
    col["rect"] = pygame.Rect(col["x"], header_y, col["w"], header_height)

sort_key = "id"
sort_reverse = False

clock = pygame.time.Clock()
running = True

while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle dropdown events first; close other dropdowns if one is clicked
        event_consumed = False
        for dd in dropdowns:
            if dd.handle_event(event):
                event_consumed = True
                if dd.is_open:
                    for other_dd in dropdowns:
                        if other_dd is not dd:
                            other_dd.is_open = False
                break

        if event_consumed:
            continue

        # Header clicks for sorting
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for col in columns:
                if col["rect"].collidepoint(event.pos):
                    if sort_key == col["key"]:
                        sort_reverse = not sort_reverse
                    else:
                        sort_key = col["key"]
                        sort_reverse = False

    # 2. Multi-Field Filter & Sort
    sel_type = type_dropdown.selected_value
    sel_rarity = rarity_dropdown.selected_value

    filtered_data = [
        item for item in raw_data
        if (sel_type == "All" or item["type"] == sel_type)
        and (sel_rarity == "All" or item["rarity"] == sel_rarity)
    ]

    sorted_data = sorted(filtered_data, key=lambda x: x[sort_key], reverse=sort_reverse)

    # 3. Drawing
    screen.fill(BG_COLOR)

    title_surf = title_font.render("Inventory Data", True, ACCENT)
    screen.blit(title_surf, (40, 28))

    # Filter Labels
    screen.blit(font.render("Type:", True, WHITE), (340, 33))
    screen.blit(font.render("Rarity:", True, WHITE), (562, 33))

    # Draw Table Headers
    pygame.draw.rect(screen, HEADER_BG, (40, header_y, 740, header_height), border_radius=4)
    for col in columns:
        indicator = ""
        if sort_key == col["key"]:
            indicator = " ▼" if sort_reverse else " ▲"
        col_text = bold_font.render(col["label"] + indicator, True, ACCENT if sort_key == col["key"] else WHITE)
        screen.blit(col_text, (col["x"] + 10, header_y + 10))

    # Draw Data Rows (or empty state message)
    row_start_y = header_y + header_height + 5
    row_height = 42

    if not sorted_data:
        empty_surf = font.render("No items match both selected filters.", True, (180, 180, 180))
        screen.blit(empty_surf, (50, row_start_y + 12))
    else:
        for i, item in enumerate(sorted_data):
            y = row_start_y + (i * row_height)
            row_bg = ROW_EVEN if i % 2 == 0 else ROW_ODD
            pygame.draw.rect(screen, row_bg, (40, y, 740, row_height - 2))

            for col in columns:
                val_str = str(item[col["key"]])
                val_surf = font.render(val_str, True, WHITE)
                screen.blit(val_surf, (col["x"] + 10, y + 10))

    # Draw Dropdowns LAST (draw open dropdown on top of closed ones)
    for dd in sorted(dropdowns, key=lambda d: d.is_open):
        dd.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
