"""Presentation helpers for the field Bag and shop economy screens."""

import pygame

from .config import SCREEN_HEIGHT, SCREEN_WIDTH
from .items import ITEM_CATEGORIES, ITEM_DATABASE
from .ui import wrap_text


def draw_inventory_screen(surface, inventory, party, fonts, pocket_index, selection, target_index, targeting, message):
    title_font, body_font, small_font = fonts
    surface.fill((15, 29, 57))
    panel = pygame.Rect(45, 34, SCREEN_WIDTH - 90, SCREEN_HEIGHT - 68)
    pygame.draw.rect(surface, (243, 248, 253), panel, border_radius=18)
    pygame.draw.rect(surface, (44, 77, 128), panel, 5, border_radius=18)
    surface.blit(body_font.render("Trainer Bag", True, (34, 69, 128)), (panel.x + 22, panel.y + 16))
    for index, category in enumerate(ITEM_CATEGORIES):
        rect = pygame.Rect(panel.x + 20 + index * 158, panel.y + 58, 148, 36)
        selected = index == pocket_index
        pygame.draw.rect(surface, (58, 105, 178) if selected else (215, 226, 239), rect, border_radius=8)
        color = (255, 255, 255) if selected else (40, 55, 78)
        surface.blit(small_font.render(category.title(), True, color), (rect.x + 10, rect.y + 7))
    category = ITEM_CATEGORIES[pocket_index]
    item_ids = inventory.pocket(category)
    for index, item_id in enumerate(item_ids[:8]):
        item = ITEM_DATABASE[item_id]
        row = pygame.Rect(panel.x + 22, panel.y + 112 + index * 43, 270, 36)
        active = index == selection
        pygame.draw.rect(surface, (65, 110, 180) if active else (223, 232, 242), row, border_radius=7)
        color = (255, 255, 255) if active else (35, 49, 70)
        surface.blit(small_font.render(item.name, True, color), (row.x + 10, row.y + 7))
        qty = small_font.render(f"x{inventory.count(item_id)}", True, color)
        surface.blit(qty, (row.right - qty.get_width() - 9, row.y + 7))
    detail_x = panel.x + 330
    if item_ids:
        item = ITEM_DATABASE[item_ids[min(selection, len(item_ids) - 1)]]
        surface.blit(body_font.render(item.name, True, (34, 69, 128)), (detail_x, panel.y + 120))
        y = panel.y + 160
        for line in wrap_text(item.description, small_font, panel.right - detail_x - 22):
            surface.blit(small_font.render(line, True, (48, 62, 83)), (detail_x, y))
            y += 24
        use_text = "Usable on a party Pokemon" if item.usable else "Cannot be used from the Bag yet"
        surface.blit(small_font.render(use_text, True, (50, 126, 76) if item.usable else (126, 91, 50)), (detail_x, y + 10))
    if targeting:
        overlay = pygame.Rect(detail_x, panel.y + 255, panel.right - detail_x - 22, 170)
        pygame.draw.rect(surface, (220, 231, 243), overlay, border_radius=10)
        surface.blit(small_font.render("Choose a Pokemon:", True, (35, 58, 91)), (overlay.x + 12, overlay.y + 10))
        for index, pokemon in enumerate(party.party):
            color = (39, 100, 174) if index == target_index else (45, 59, 79)
            label = f"{pokemon.display_name}  HP {pokemon.current_hp}/{pokemon.max_hp}  {pokemon.status}"
            surface.blit(small_font.render(label, True, color), (overlay.x + 14, overlay.y + 40 + index * 22))
    surface.blit(small_font.render(message, True, (151, 72, 45)), (panel.x + 24, panel.bottom - 58))
    hint = "UP/DOWN: choose Pokemon  ENTER: use  ESC: cancel" if targeting else "LEFT/RIGHT: pocket  UP/DOWN: item  ENTER: use  I/ESC: close"
    surface.blit(small_font.render(hint, True, (82, 96, 116)), (panel.x + 24, panel.bottom - 30))


def draw_shop_screen(surface, npc, inventory, money, fonts, mode, selection, message):
    _title_font, body_font, small_font = fonts
    panel = pygame.Rect(135, 55, 530, 490)
    pygame.draw.rect(surface, (247, 250, 255), panel, border_radius=16)
    pygame.draw.rect(surface, (35, 57, 91), panel, 4, border_radius=16)
    surface.blit(body_font.render(f"{npc.name}'s Shop", True, (34, 72, 137)), (panel.x + 24, panel.y + 18))
    for index, label in enumerate(("BUY", "SELL")):
        tab = pygame.Rect(panel.right - 180 + index * 78, panel.y + 18, 70, 30)
        pygame.draw.rect(surface, (63, 107, 177) if mode == label.lower() else (217, 226, 238), tab, border_radius=7)
        surface.blit(small_font.render(label, True, (255, 255, 255) if mode == label.lower() else (38, 52, 73)), (tab.x + 10, tab.y + 4))
    entries = npc.shop if mode == "buy" else inventory.pocket_items_for_sale()
    page_start = (selection // 7) * 7
    for row_index, entry in enumerate(entries[page_start:page_start + 7]):
        index = page_start + row_index
        item_id = entry["item"] if mode == "buy" else entry
        item = ITEM_DATABASE[item_id]
        price = entry["price"] if mode == "buy" else item.sell_price
        row = pygame.Rect(panel.x + 25, panel.y + 68 + row_index * 49, panel.width - 50, 41)
        active = index == selection
        pygame.draw.rect(surface, (67, 112, 183) if active else (224, 232, 241), row, border_radius=9)
        color = (255, 255, 255) if active else (31, 45, 66)
        surface.blit(small_font.render(item.name, True, color), (row.x + 12, row.y + 9))
        detail = f"${price:,}" if mode == "buy" else f"x{inventory.count(item_id)}   ${price:,}"
        rendered = small_font.render(detail, True, color)
        surface.blit(rendered, (row.right - rendered.get_width() - 12, row.y + 9))
    surface.blit(small_font.render(f"Money: ${money:,}", True, (38, 58, 84)), (panel.x + 25, panel.bottom - 72))
    surface.blit(small_font.render(message, True, (126, 73, 46)), (panel.x + 25, panel.bottom - 46))
    surface.blit(small_font.render("LEFT/RIGHT: Buy/Sell  ENTER: transact  ESC: leave", True, (82, 96, 116)), (panel.x + 25, panel.bottom - 24))
