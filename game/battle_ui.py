"""Rendering helpers for the turn-based battle scene."""

import pygame

from .config import SCREEN_HEIGHT, SCREEN_WIDTH
from .items import ITEM_DATABASE
from .ui import draw_health_bar, draw_panel


TYPE_COLORS = {
    "Normal": (150, 150, 135), "Fire": (230, 92, 52), "Water": (67, 126, 220),
    "Grass": (80, 169, 77), "Ground": (191, 154, 78), "Flying": (126, 150, 219),
    "Bug": (145, 160, 45), "Dark": (89, 76, 71), "Fighting": (180, 62, 54),
    "Poison": (152, 76, 160), "Psychic": (221, 84, 130), "Steel": (130, 147, 160),
}


def draw_battle_screen(
    surface, battle, assets, title_font, body_font, small_font, menu_mode, selected,
    inventory=None, capture_animation=None,
):
    surface.fill((124, 204, 224))
    pygame.draw.ellipse(surface, (105, 180, 105), (420, 185, 330, 105))
    pygame.draw.ellipse(surface, (93, 162, 91), (40, 345, 370, 120))

    player = battle.player_pokemon
    enemy = battle.enemy_pokemon
    enemy_sprite = assets.image(enemy.species.sprite_path, size=(180, 180))
    player_sprite = pygame.transform.flip(assets.image(player.species.sprite_path, size=(210, 210)), True, False)
    surface.blit(enemy_sprite, enemy_sprite.get_rect(center=(585, 165)))
    surface.blit(player_sprite, player_sprite.get_rect(center=(235, 345)))

    _draw_status_panel(surface, enemy, pygame.Rect(35, 45, 330, 105), body_font, small_font)
    _draw_status_panel(surface, player, pygame.Rect(430, 300, 335, 115), body_font, small_font, show_hp=True)

    menu_rect = pygame.Rect(20, 430, SCREEN_WIDTH - 40, 150)
    draw_panel(surface, menu_rect, (246, 249, 252), (38, 57, 88), 4)
    if battle.result is not None:
        _draw_result(surface, battle, menu_rect, body_font, small_font)
    elif menu_mode == "moves":
        _draw_moves(surface, battle, menu_rect, body_font, small_font, selected)
    elif menu_mode == "bag":
        _draw_bag(surface, inventory, menu_rect, body_font, small_font, selected)
    else:
        _draw_main_menu(surface, battle, menu_rect, body_font, small_font, selected)
    if capture_animation is not None:
        _draw_capture_animation(surface, capture_animation, small_font)


def _draw_status_panel(surface, pokemon, rect, body_font, small_font, show_hp=False):
    draw_panel(surface, rect, (248, 250, 241), (44, 65, 68), 3)
    name = body_font.render(pokemon.display_name, True, (28, 42, 53))
    level = small_font.render(f"Lv. {pokemon.level}", True, (45, 55, 64))
    surface.blit(name, (rect.x + 14, rect.y + 10))
    surface.blit(level, (rect.right - level.get_width() - 14, rect.y + 15))
    hp_color = (68, 185, 92) if pokemon.current_hp / pokemon.max_hp > 0.5 else (225, 181, 49) if pokemon.current_hp / pokemon.max_hp > 0.2 else (215, 67, 59)
    draw_health_bar(surface, rect.x + 55, rect.y + 57, rect.width - 75, 18, pokemon.current_hp, pokemon.max_hp, hp_color)
    surface.blit(small_font.render("HP", True, (45, 58, 66)), (rect.x + 15, rect.y + 55))
    if show_hp:
        hp = small_font.render(f"{pokemon.current_hp} / {pokemon.max_hp}", True, (45, 55, 64))
        surface.blit(hp, (rect.right - hp.get_width() - 18, rect.y + 80))
    if pokemon.status != "healthy":
        status = small_font.render(pokemon.status.upper(), True, (190, 55, 45))
        surface.blit(status, (rect.x + 15, rect.y + 82))


def _draw_main_menu(surface, battle, rect, body_font, small_font, selected):
    for line_index, line in enumerate(battle.log[-4:]):
        prompt = small_font.render(line, True, (36, 48, 65))
        surface.blit(prompt, (rect.x + 18, rect.y + 12 + line_index * 27))
    options = ("FIGHT", "BAG", "RUN")
    for index, label in enumerate(options):
        option = pygame.Rect(rect.x + 405 + index * 115, rect.y + 70, 105, 52)
        fill = (55, 104, 180) if selected == index else (216, 226, 238)
        color = (255, 255, 255) if selected == index else (35, 49, 70)
        pygame.draw.rect(surface, fill, option, border_radius=8)
        text = body_font.render(label, True, color)
        surface.blit(text, text.get_rect(center=option.center))


def _draw_moves(surface, battle, rect, body_font, small_font, selected):
    pokemon = battle.player_pokemon
    for index, move in enumerate(pokemon.known_moves):
        column, row = index % 2, index // 2
        option = pygame.Rect(rect.x + 15 + column * 370, rect.y + 12 + row * 62, 355, 55)
        fill = TYPE_COLORS.get(move.type_name, (100, 110, 125)) if selected == index else (225, 232, 240)
        text_color = (255, 255, 255) if selected == index else (28, 40, 58)
        pygame.draw.rect(surface, fill, option, border_radius=8)
        surface.blit(body_font.render(move.name, True, text_color), (option.x + 12, option.y + 5))
        pp = battle.remaining_pp(pokemon, move)
        detail = small_font.render(f"{move.type_name}  {move.category.title()}  PP {pp}/{move.pp}", True, text_color)
        surface.blit(detail, (option.x + 12, option.y + 31))


def _draw_bag(surface, inventory, rect, body_font, small_font, selected):
    ball_ids = [item_id for item_id, count in inventory.items.items() if count > 0 and ITEM_DATABASE.get(item_id) and ITEM_DATABASE[item_id].category == "ball"]
    if not ball_ids:
        surface.blit(body_font.render("No Poké Balls remaining", True, (38, 52, 72)), (rect.x + 20, rect.y + 25))
    for index, item_id in enumerate(ball_ids[:6]):
        column, row = index % 3, index // 3
        option = pygame.Rect(rect.x + 12 + column * 250, rect.y + 12 + row * 62, 238, 55)
        active = index == selected
        pygame.draw.rect(surface, (69, 112, 183) if active else (225, 232, 240), option, border_radius=8)
        color = (255, 255, 255) if active else (28, 40, 58)
        item = ITEM_DATABASE[item_id]
        surface.blit(body_font.render(item.name, True, color), (option.x + 10, option.y + 5))
        surface.blit(small_font.render(f"Quantity: {inventory.count(item_id)}", True, color), (option.x + 10, option.y + 32))


def _draw_capture_animation(surface, animation, small_font):
    progress = animation.progress
    if progress < 0.42:
        travel = progress / 0.42
        x = 260 + (570 - 260) * travel
        y = 330 - 220 * (4 * travel * (1 - travel))
    else:
        shake_phase = animation.visible_shakes
        x = 570 + (7 if shake_phase % 2 else -7 if shake_phase else 0)
        y = 225
    center = (round(x), round(y))
    pygame.draw.circle(surface, (245, 247, 250), center, 20)
    pygame.draw.arc(surface, (220, 58, 58), (center[0] - 20, center[1] - 20, 40, 40), 0, 3.1416, 20)
    pygame.draw.line(surface, (32, 42, 55), (center[0] - 19, center[1]), (center[0] + 19, center[1]), 3)
    pygame.draw.circle(surface, (245, 247, 250), center, 6)
    pygame.draw.circle(surface, (32, 42, 55), center, 6, 2)
    label = "Throwing..." if progress < 0.42 else f"Shakes: {animation.visible_shakes} / 4"
    text = small_font.render(label, True, (25, 39, 60))
    surface.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 410)))


def _draw_result(surface, battle, rect, body_font, small_font):
    result = battle.result
    if result.escaped:
        heading = "Got away safely!"
    elif result.captured:
        heading = "Pokémon caught!"
    elif result.winner == "player":
        heading = "Battle won!"
    else:
        heading = "Your party was defeated."
    surface.blit(body_font.render(heading, True, (30, 48, 78)), (rect.x + 20, rect.y + 18))
    details = battle.log[-1]
    if result.xp_awarded:
        details = f"Gained {result.xp_awarded} XP. Levels gained: {result.levels_gained}."
    surface.blit(small_font.render(details, True, (48, 62, 82)), (rect.x + 20, rect.y + 62))
    surface.blit(small_font.render("Press ENTER to return to the world", True, (70, 84, 105)), (rect.x + 20, rect.y + 105))
