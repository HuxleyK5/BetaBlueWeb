"""Nursery presentation kept separate from breeding rules."""

import pygame

from .config import SCREEN_HEIGHT, SCREEN_WIDTH
from .pokemon_data import DATABASE


def draw_nursery_screen(surface, party, nursery, fonts, parent_a, parent_b, message):
    _title_font, body_font, small_font = fonts
    surface.fill((31, 67, 62))
    panel = pygame.Rect(55, 38, SCREEN_WIDTH - 110, SCREEN_HEIGHT - 76)
    pygame.draw.rect(surface, (246, 249, 239), panel, border_radius=18)
    pygame.draw.rect(surface, (64, 116, 91), panel, 5, border_radius=18)
    surface.blit(body_font.render("Bluebell Pokemon Nursery", True, (39, 91, 68)), (panel.x + 22, panel.y + 18))
    surface.blit(small_font.render("LEFT/RIGHT: first parent   UP/DOWN: second parent", True, (65, 81, 72)), (panel.x + 22, panel.y + 60))
    if len(party.party) < 2:
        surface.blit(body_font.render("Bring at least two Pokemon to breed.", True, (115, 73, 55)), (panel.x + 45, panel.y + 130))
    else:
        first, second = party.party[parent_a], party.party[parent_b]
        labels = (("Parent A", first), ("Parent B", second))
        for index, (label, pokemon) in enumerate(labels):
            card = pygame.Rect(panel.x + 35 + index * 330, panel.y + 105, 290, 105)
            pygame.draw.rect(surface, (220, 234, 219), card, border_radius=12)
            surface.blit(small_font.render(label, True, (63, 92, 75)), (card.x + 12, card.y + 10))
            surface.blit(body_font.render(pokemon.display_name, True, (36, 75, 57)), (card.x + 12, card.y + 36))
            detail = f"Lv.{pokemon.level}  {pokemon.gender.title()}  Friendship {pokemon.friendship}"
            surface.blit(small_font.render(detail, True, (66, 82, 72)), (card.x + 12, card.y + 75))
    surface.blit(body_font.render(f"Eggs: {len(nursery.eggs)} / {nursery.max_eggs}", True, (39, 91, 68)), (panel.x + 28, panel.y + 245))
    for index, egg in enumerate(nursery.eggs[:6]):
        species = DATABASE.get_species(egg.species_key)
        status = "Ready to hatch" if egg.ready else f"{egg.remaining_steps} steps remaining"
        surface.blit(small_font.render(f"Egg {index + 1}: {species.name} - {status}", True, (53, 70, 60)), (panel.x + 38, panel.y + 285 + index * 27))
    surface.blit(small_font.render(message, True, (139, 80, 45)), (panel.x + 25, panel.bottom - 58))
    surface.blit(small_font.render("ENTER: breed selected parents   N/ESC: leave", True, (75, 91, 80)), (panel.x + 25, panel.bottom - 29))
