"""Application lifecycle and main loop for Pokemon Beta Blue."""

from dataclasses import replace
import pygame

from .config import (
    GAME_VERSION, PROJECT_ROOT, USER_DATA_ROOT, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, STATE_GENDER_SELECT, STATE_NAME_ENTRY, STATE_SKIN_SELECT, STATE_TITLE,
    STATE_BATTLE, STATE_DIALOGUE, STATE_INVENTORY, STATE_MULTIPLAYER, STATE_NURSERY, STATE_QUEST_LOG, STATE_REGION_MAP, STATE_SHOP, STATE_STARTER_SELECT, STATE_TOWN,
    STATE_WILD_ENCOUNTER, load_settings, save_settings,
)
from .window import GameWindow
from .player import Player
from .camera import Camera
from .world import WorldManager
from .npc import NPCManager
from .trainer_ai import TrainerAI
from .encounters import EncounterContext, EncounterManager
from .battle import Battle, BattleAction, BattleKind
from .battle_ui import draw_battle_screen
from .capture import CaptureAnimation, CaptureCalculator, CaptureContext
from .items import ITEM_CATEGORIES, ITEM_DATABASE, Inventory
from .economy import ShopService
from .inventory_ui import draw_inventory_screen, draw_shop_screen
from .party import PartyManager
from .pokemon_data import create_pokemon
from .input import InputManager, handle_name_input
from .assets import AssetManager, ensure_asset_folders
from .ui import wrap_text
from .quests import QuestManager
from .story import StoryProgress
from .evolution import EvolutionService
from .breeding import Nursery
from .breeding_ui import draw_nursery_screen
from .save_system import SaveError, SaveManager
from .weather import WorldSimulation
from .world_events import WorldEventManager
from .world_effects import draw_world_effects
from .accounts import OfflineAccountProvider
from .multiplayer import ConnectionState, MultiplayerGateway
from .trading import TradeService
from .online_battle import OnlineBattleCoordinator
from .multiplayer_ui import draw_multiplayer_screen
from .audio import AudioManager
from .performance import PerformanceMonitor
from .region_map import RegionMap


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


class Game:
    def __init__(self, root_path=PROJECT_ROOT):
        pygame.init()
        self.root_path = root_path
        self.settings = load_settings()
        self.save_manager = SaveManager(USER_DATA_ROOT / "saves")
        self.account_provider = OfflineAccountProvider()
        self.player_identity = self.account_provider.create_guest()
        self.multiplayer = MultiplayerGateway(self.player_identity)
        self.trade_service = TradeService()
        self.online_battles = OnlineBattleCoordinator()
        ensure_asset_folders(root_path)
        self.window = GameWindow(self.settings)
        self.assets = AssetManager(self.root_path)
        self.audio = AudioManager(self.settings.master_volume, self.settings.sfx_volume)
        self.performance = PerformanceMonitor()
        self.input = InputManager()
        self.player = Player()
        self.party = PartyManager()
        self.inventory = Inventory()
        self.shop_service = ShopService()
        self.evolution_service = EvolutionService()
        self.nursery = Nursery()
        self.capture_calculator = CaptureCalculator()
        self.capture_animation = None
        self.world = WorldManager(self.root_path / "maps")
        self.region_map = RegionMap(self.root_path / "maps" / "overviews" / "beta_region.json", self.world.areas)
        self.world_simulation = WorldSimulation()
        self.world_events = WorldEventManager(self.root_path / "maps" / "events" / "world_events.json", self.world)
        self.npcs = NPCManager(self.world, self.root_path / "characters" / "npcs.json")
        self.story = StoryProgress()
        self.quests = QuestManager(
            self.root_path / "quests" / "quests.json",
            known_npcs=self.npcs.npcs,
            known_areas=self.world.areas,
        )
        self.encounters = EncounterManager(self.root_path / "Pokemon" / "data" / "encounters.json")
        self.encounters.validate_areas(self.world.areas)
        self.encounter_context = self.world_events.context_for(self.world.current_area_id, self.world_simulation, self.story.flags)
        self.active_encounter = None
        self.active_battle = None
        self.active_npc = None
        self.dialogue_lines = ()
        self.dialogue_index = 0
        self.shop_selection = 0
        self.shop_mode = "buy"
        self.shop_message = ""
        self.inventory_pocket = 0
        self.inventory_selection = 0
        self.inventory_target = 0
        self.inventory_targeting = False
        self.inventory_message = ""
        self.nursery_parent_a = 0
        self.nursery_parent_b = 1
        self.nursery_message = "Select two compatible partners."
        self.badge_names = self.story.badges
        self.quest_selection = 0
        self.quest_notice = ""
        self.quest_notice_timer = 0.0
        self.starter_options = ("treecko", "torchic", "mudkip")
        self.starter_selection = 0
        self.gender_options = ("male", "female")
        self.gender_selection = 0
        self.skin_selection = 0
        self.battle_menu = "main"
        self.battle_selection = 0
        self.game_map = self.world.current_area.game_map
        self.player.teleport(*self.world.current_area.spawn)
        self.camera = Camera(self.game_map.pixel_width, self.game_map.pixel_height)
        self.camera.update(*self.player.center, snap=True)
        self.location_banner_timer = 2.5
        self.state = STATE_TITLE
        self.clock = pygame.time.Clock()
        self.title_font = self.assets.font(72, bold=True)
        self.body_font = self.assets.font(28)
        self.small_font = self.assets.font(20)
        self.assets.preload_images(
            [create_pokemon(key, 5).species.sprite_path for key in self.starter_options], size=(155, 155)
        )
        self.assets.preload_images(("assets/characters/male_trainers_supplied.png", "assets/characters/female_trainers_supplied.png"))
        self.player_name = ""
        self.save_message = ""

    def handle_events(self):
        self.input.begin_frame()
        for event in pygame.event.get():
            self.input.process_event(event)
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.window.toggle_fullscreen()
                    self.persist_settings()
                elif event.key == pygame.K_F3:
                    self.performance.toggle()
                elif event.key == pygame.K_F5:
                    self.save_game(manual=True)
                elif event.key == pygame.K_F9:
                    self.load_game()
                elif event.key == pygame.K_F6 and self.state == STATE_TOWN:
                    self.world_simulation.advance_hours(6)
                    self.refresh_world_context()
                    self.quest_notice = "You wait for six hours."
                    self.quest_notice_timer = 3.0
                elif self.state == STATE_TITLE:
                    self.handle_title_input(event)
                elif self.state == STATE_NAME_ENTRY:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_SKIN_SELECT
                    else:
                        self.player_name = handle_name_input(event, self.player_name)
                    if event.key == pygame.K_RETURN and self.player_name.strip():
                        self.player.name = self.player_name.strip()
                        self.player_identity = self.account_provider.rename_guest(self.player.name)
                        self.multiplayer.session.identity = self.player_identity
                        self.state = STATE_STARTER_SELECT
                elif self.state == STATE_GENDER_SELECT:
                    self.handle_gender_input(event)
                elif self.state == STATE_SKIN_SELECT:
                    self.handle_skin_input(event)
                elif self.state == STATE_STARTER_SELECT:
                    self.handle_starter_input(event)
                elif self.state == STATE_TOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.try_npc_interaction()
                elif self.state == STATE_TOWN and event.key == pygame.K_q:
                    self.quest_selection = 0
                    self.state = STATE_QUEST_LOG
                elif self.state == STATE_TOWN and event.key == pygame.K_i:
                    self.open_inventory()
                elif self.state == STATE_TOWN and event.key == pygame.K_n:
                    self.open_nursery()
                elif self.state == STATE_TOWN and event.key == pygame.K_m:
                    self.state = STATE_MULTIPLAYER
                elif self.state == STATE_TOWN and event.key == pygame.K_r:
                    self.state = STATE_REGION_MAP
                elif self.state == STATE_QUEST_LOG:
                    self.handle_quest_log_input(event)
                elif self.state == STATE_INVENTORY:
                    self.handle_inventory_input(event)
                elif self.state == STATE_NURSERY:
                    self.handle_nursery_input(event)
                elif self.state == STATE_MULTIPLAYER:
                    self.handle_multiplayer_input(event)
                elif self.state == STATE_REGION_MAP and event.key in (pygame.K_ESCAPE, pygame.K_r):
                    self.state = STATE_TOWN
                elif self.state == STATE_DIALOGUE:
                    self.handle_dialogue_input(event)
                elif self.state == STATE_SHOP:
                    self.handle_shop_input(event)
                elif self.state == STATE_WILD_ENCOUNTER:
                    if event.key == pygame.K_RETURN:
                        self.start_wild_battle()
                    elif event.key == pygame.K_ESCAPE:
                        self.dismiss_wild_encounter()
                elif self.state == STATE_BATTLE:
                    self.handle_battle_input(event)
        return True

    def handle_title_input(self, event):
        if event.key == pygame.K_c and self.save_manager.has_save:
            self.load_game()
        elif event.key == pygame.K_RETURN:
            self.player_name = ""
            self.player.name = ""
            self.gender_selection = 0
            self.skin_selection = 0
            self.player.set_appearance("male", 0)
            self.state = STATE_GENDER_SELECT

    def persist_settings(self):
        width, height = self.window.windowed_size if self.window.fullscreen else self.window.window.get_size()
        self.window.windowed_size = (width, height)
        self.settings = replace(self.settings, window_width=width, window_height=height, fullscreen=self.window.fullscreen)
        try:
            save_settings(self.settings)
        except OSError as error:
            self.save_message = f"Settings could not be saved: {error}"

    def save_game(self, manual=False):
        stable_states = {STATE_TOWN, STATE_QUEST_LOG, STATE_INVENTORY, STATE_NURSERY, STATE_MULTIPLAYER, STATE_REGION_MAP}
        if self.state not in stable_states or not self.player.name or not self.party.party:
            if manual:
                self.save_message = "Saving is available during normal exploration."
                self.quest_notice = self.save_message
                self.quest_notice_timer = 3.0
                self.audio.play("error")
            return False
        self.persist_settings()
        try:
            self.save_manager.save(self)
        except SaveError as error:
            self.save_message = str(error)
            self.quest_notice = self.save_message
            self.quest_notice_timer = 4.0
            self.audio.play("error")
            return False
        self.save_message = "Game saved."
        if manual:
            self.quest_notice = self.save_message
            self.quest_notice_timer = 3.0
            self.audio.play("confirm")
        return True

    def load_game(self):
        try:
            self.save_manager.load(self)
        except SaveError as error:
            self.save_message = str(error)
            if self.state != STATE_TITLE:
                self.quest_notice = self.save_message
                self.quest_notice_timer = 4.0
            self.audio.play("error")
            return False
        self.active_battle = None
        self.active_encounter = None
        self.active_npc = None
        self.capture_animation = None
        self.encounters.reset_grace()
        self.state = STATE_TOWN
        self.location_banner_timer = 2.5
        self.window.fullscreen = self.settings.fullscreen
        self.window.windowed_size = (self.settings.window_width, self.settings.window_height)
        self.window.vsync = self.settings.vsync
        self.window.window = self.window._create_window()
        self.audio.master_volume = self.settings.master_volume
        self.audio.sfx_volume = self.settings.sfx_volume
        self.save_message = "Save loaded."
        self.quest_notice = self.save_message
        self.quest_notice_timer = 3.0
        self.audio.play("confirm")
        return True

    def handle_starter_input(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.starter_selection = (self.starter_selection - 1) % len(self.starter_options)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.starter_selection = (self.starter_selection + 1) % len(self.starter_options)
        elif event.key == pygame.K_RETURN:
            starter_key = self.starter_options[self.starter_selection]
            self.party.add_pokemon(create_pokemon(starter_key, 5))
            self.publish_quest_event("starter_chosen", starter_key)
            self.state = STATE_TOWN
            self.audio.play("confirm")

    def handle_gender_input(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
            self.gender_selection = 1 - self.gender_selection
        elif event.key == pygame.K_ESCAPE:
            self.state = STATE_TITLE
        elif event.key == pygame.K_RETURN:
            gender = self.gender_options[self.gender_selection]
            self.skin_selection = 0
            self.player.set_appearance(gender, self.skin_selection)
            self.state = STATE_SKIN_SELECT
            self.audio.play("confirm")

    def handle_skin_input(self, event):
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.skin_selection = (self.skin_selection - 1) % 3
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.skin_selection = (self.skin_selection + 1) % 3
        elif event.key == pygame.K_ESCAPE:
            self.state = STATE_GENDER_SELECT
        elif event.key == pygame.K_RETURN:
            gender = self.gender_options[self.gender_selection]
            self.player.set_appearance(gender, self.skin_selection)
            self.state = STATE_NAME_ENTRY
            self.audio.play("confirm")

    def update(self, dt):
        if self.player.name and self.state != STATE_TOWN:
            self.player.stats.play_time_seconds += dt
        if self.state == STATE_BATTLE and self.capture_animation is not None:
            self.capture_animation.update(dt)
            if self.capture_animation.complete:
                self.finish_capture_animation()
            return
        if self.state != STATE_TOWN:
            return
        self.location_banner_timer = max(0.0, self.location_banner_timer - dt)
        self.quest_notice_timer = max(0.0, self.quest_notice_timer - dt)
        self.world_simulation.update(dt)
        self.refresh_world_context()
        world_hour = self.world_simulation.hour
        self.npcs.update(dt, self.world.current_area_id, world_hour, (self.player.tile_x, self.player.tile_y))
        if not self.player.moving:
            dx, dy = self.input.movement_vector()
            if dx or dy:
                self.player.start_move(dx, dy, self.is_world_solid)
        was_moving = self.player.moving
        self.player.update(dt)
        if was_moving and not self.player.moving:
            self.advance_pokemon_lifecycle()
            transition = self.world.transition_at(self.player.tile_x, self.player.tile_y)
            if transition is None:
                transition = self.world_events.transition_at(
                    self.world.current_area_id, self.player.tile_x, self.player.tile_y,
                    self.world_simulation, self.story.flags,
                )
            if transition is not None:
                self.change_area(transition)
            else:
                self.try_wild_encounter()
        self.camera.update(*self.player.center, dt=dt)

    def is_world_solid(self, tile_x, tile_y):
        return self.game_map.is_solid(tile_x, tile_y) or self.npcs.is_occupied(self.world.current_area_id, tile_x, tile_y)

    def try_npc_interaction(self):
        if self.player.moving:
            return
        direction = {
            "up": (0, -1), "up_left": (-1, -1), "up_right": (1, -1),
            "down": (0, 1), "down_left": (-1, 1), "down_right": (1, 1),
            "left": (-1, 0), "right": (1, 0),
        }[self.player.direction]
        npc = self.npcs.at(self.world.current_area_id, self.player.tile_x + direction[0], self.player.tile_y + direction[1])
        if npc is not None:
            self.begin_dialogue(npc)

    def begin_dialogue(self, npc):
        self.active_npc = npc
        self.dialogue_lines = npc.dialogue_for_state()
        self.dialogue_index = 0
        npc.direction = _opposite_direction(self.player.direction)
        self.state = STATE_DIALOGUE

    def handle_dialogue_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.close_npc_interaction()
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.dialogue_index += 1
            if self.dialogue_index >= len(self.dialogue_lines):
                self.complete_dialogue()

    def complete_dialogue(self):
        npc = self.active_npc
        npc.interacted = True
        self.publish_quest_event("talk_to_npc", npc.npc_id)
        if npc.can_battle():
            self.start_trainer_battle(npc)
        elif npc.role == "shopkeeper":
            self.shop_selection = 0
            self.shop_mode = "buy"
            self.shop_message = "Choose an item."
            self.state = STATE_SHOP
        else:
            self.grant_npc_reward(npc)
            self.close_npc_interaction()

    def close_npc_interaction(self):
        self.active_npc = None
        self.dialogue_lines = ()
        self.dialogue_index = 0
        self.state = STATE_TOWN
        self.save_game()

    def start_trainer_battle(self, npc):
        kind = BattleKind.GYM if npc.role == "gym_leader" else BattleKind.TRAINER
        ai = TrainerAI(npc.ai)
        self.active_battle = Battle(self.party.party, npc.create_party(), kind, enemy_ai=ai)
        self.active_battle.log[0] = f"{npc.name} challenges you!"
        self.battle_menu = "main"
        self.battle_selection = 0
        self.capture_animation = None
        self.state = STATE_BATTLE
        self.audio.play("battle")

    def grant_npc_reward(self, npc):
        if npc.reward_claimed or not npc.reward:
            return
        money = npc.reward.get("money", 0)
        self.player.stats.money += money
        for item_id, count in npc.reward.get("items", {}).items():
            self.inventory.add(item_id, count)
        badge = npc.reward.get("badge")
        if badge and self.story.earn_badge(badge):
            self.player.stats.badges = len(self.badge_names)
            self.publish_quest_event("earn_badge", badge)
        npc.reward_claimed = True

    def publish_quest_event(self, event, target=None, amount=1):
        """Bridge gameplay events into quests and award each completion once."""
        updates, rewards = self.quests.emit(event, target, amount)
        for quest_id, reward in rewards:
            self.player.stats.money += reward.get("money", 0)
            for item_id, count in reward.get("items", {}).items():
                self.inventory.add(item_id, count)
            self.story.apply_quest_rewards(reward)
            self.quest_notice = f"Quest complete: {self.quests.definitions[quest_id].title}"
            self.quest_notice_timer = 4.0
            self.audio.play("quest")
        if updates and not rewards:
            update = updates[-1]
            quest = self.quests.definitions[update.quest_id]
            self.quest_notice = f"New quest: {quest.title}" if update.activated else f"Quest updated: {quest.title}"
            self.quest_notice_timer = 3.0
        self.refresh_world_context()

    def refresh_world_context(self):
        self.encounter_context = self.world_events.context_for(
            self.world.current_area_id, self.world_simulation, self.story.flags
        )

    def handle_shop_input(self, event):
        entries = self.shop_entries()
        if event.key == pygame.K_ESCAPE:
            self.close_npc_interaction()
        elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d, pygame.K_TAB):
            self.shop_mode = "sell" if self.shop_mode == "buy" else "buy"
            self.shop_selection = 0
            self.shop_message = "Choose an item."
        elif event.key in (pygame.K_UP, pygame.K_w) and entries:
            self.shop_selection = (self.shop_selection - 1) % len(entries)
        elif event.key in (pygame.K_DOWN, pygame.K_s) and entries:
            self.shop_selection = (self.shop_selection + 1) % len(entries)
        elif event.key == pygame.K_RETURN and entries:
            if self.shop_mode == "buy":
                result = self.shop_service.buy(self.player.stats, self.inventory, entries[self.shop_selection])
            else:
                result = self.shop_service.sell(self.player.stats, self.inventory, entries[self.shop_selection])
            self.shop_message = result.message
            remaining = self.shop_entries()
            self.shop_selection = min(self.shop_selection, max(0, len(remaining) - 1))

    def shop_entries(self):
        if self.shop_mode == "buy":
            return self.active_npc.shop
        return self.inventory.pocket_items_for_sale()

    def open_inventory(self):
        self.inventory_pocket = 0
        self.inventory_selection = 0
        self.inventory_target = 0
        self.inventory_targeting = False
        self.inventory_message = "Choose an item."
        self.state = STATE_INVENTORY

    def inventory_entries(self):
        return self.inventory.pocket(ITEM_CATEGORIES[self.inventory_pocket])

    def handle_inventory_input(self, event):
        if self.inventory_targeting:
            if event.key == pygame.K_ESCAPE:
                self.inventory_targeting = False
            elif event.key in (pygame.K_UP, pygame.K_w) and self.party.party:
                self.inventory_target = (self.inventory_target - 1) % len(self.party.party)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and self.party.party:
                self.inventory_target = (self.inventory_target + 1) % len(self.party.party)
            elif event.key == pygame.K_RETURN and self.party.party:
                entries = self.inventory_entries()
                if entries:
                    item_id = entries[self.inventory_selection]
                    item = ITEM_DATABASE[item_id]
                    pokemon = self.party.party[self.inventory_target]
                    if item.effect == "evolution":
                        trigger = "trade" if item_id == "link_cable" else "item"
                        result = self.evolution_service.evolve(pokemon, trigger, item_id)
                        if result.success:
                            self.inventory.remove(item_id)
                    else:
                        result = self.inventory.use(item_id, pokemon)
                    self.inventory_message = result.message
                    if result.success:
                        self.inventory_targeting = False
                        self.inventory_selection = min(self.inventory_selection, max(0, len(self.inventory_entries()) - 1))
            return
        entries = self.inventory_entries()
        if event.key in (pygame.K_ESCAPE, pygame.K_i):
            self.state = STATE_TOWN
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.inventory_pocket = (self.inventory_pocket - 1) % len(ITEM_CATEGORIES)
            self.inventory_selection = 0
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.inventory_pocket = (self.inventory_pocket + 1) % len(ITEM_CATEGORIES)
            self.inventory_selection = 0
        elif event.key in (pygame.K_UP, pygame.K_w) and entries:
            self.inventory_selection = (self.inventory_selection - 1) % len(entries)
        elif event.key in (pygame.K_DOWN, pygame.K_s) and entries:
            self.inventory_selection = (self.inventory_selection + 1) % len(entries)
        elif event.key == pygame.K_RETURN and entries:
            item = ITEM_DATABASE[entries[self.inventory_selection]]
            if item.usable and self.party.party:
                self.inventory_target = min(self.inventory_target, len(self.party.party) - 1)
                self.inventory_targeting = True
                self.inventory_message = f"Use {item.name} on which Pokemon?"
            else:
                self.inventory_message = f"{item.name} cannot be used right now."

    def open_nursery(self):
        self.nursery_parent_a = 0
        self.nursery_parent_b = min(1, max(0, len(self.party.party) - 1))
        self.nursery_message = "Select two compatible partners."
        self.state = STATE_NURSERY

    def handle_multiplayer_input(self, event):
        if event.key in (pygame.K_ESCAPE, pygame.K_m):
            self.state = STATE_TOWN
        elif event.key == pygame.K_RETURN:
            if self.multiplayer.session.state == ConnectionState.CONNECTED:
                self.multiplayer.disconnect()
            else:
                self.multiplayer.connect_loopback()

    def handle_nursery_input(self, event):
        count = len(self.party.party)
        if event.key in (pygame.K_ESCAPE, pygame.K_n):
            self.state = STATE_TOWN
        elif event.key in (pygame.K_LEFT, pygame.K_a) and count:
            self.nursery_parent_a = (self.nursery_parent_a - 1) % count
        elif event.key in (pygame.K_RIGHT, pygame.K_d) and count:
            self.nursery_parent_a = (self.nursery_parent_a + 1) % count
        elif event.key in (pygame.K_UP, pygame.K_w) and count:
            self.nursery_parent_b = (self.nursery_parent_b - 1) % count
        elif event.key in (pygame.K_DOWN, pygame.K_s) and count:
            self.nursery_parent_b = (self.nursery_parent_b + 1) % count
        elif event.key == pygame.K_RETURN and count >= 2:
            _egg, self.nursery_message = self.nursery.breed(
                self.party.party[self.nursery_parent_a], self.party.party[self.nursery_parent_b]
            )

    def advance_pokemon_lifecycle(self):
        """Advance friendship and Eggs exactly once per completed world step."""
        self.nursery.advance_steps()
        if self.player.stats.steps_taken % 128 == 0:
            for pokemon in self.party.party:
                pokemon.gain_friendship(1)
            self.process_evolutions("friendship")
        hatched = self.nursery.hatch_ready(self.party)
        if hatched:
            names = ", ".join(pokemon.display_name for pokemon in hatched)
            self.quest_notice = f"The Egg hatched into {names}!"
            self.quest_notice_timer = 5.0

    def process_evolutions(self, trigger):
        for pokemon in self.party.party:
            result = self.evolution_service.evolve(pokemon, trigger)
            if result.success:
                self.quest_notice = result.message
                self.quest_notice_timer = 5.0

    def try_wild_encounter(self):
        tile_symbol = self.game_map.symbol_at(self.player.tile_x, self.player.tile_y)
        encounter = self.encounters.roll(self.world.current_area_id, tile_symbol, self.encounter_context)
        if encounter is not None:
            self.active_encounter = encounter
            self.player.stats.pokemon_seen += 1
            self.state = STATE_WILD_ENCOUNTER
            self.audio.play("encounter")

    def dismiss_wild_encounter(self):
        """Leave the pre-battle reveal without starting combat."""
        self.active_encounter = None
        self.encounters.reset_grace()
        self.state = STATE_TOWN
        self.save_game()

    def start_wild_battle(self):
        if self.active_encounter is None or self.party.active_pokemon is None:
            self.dismiss_wild_encounter()
            return
        self.active_battle = Battle(self.party.party, [self.active_encounter.pokemon], BattleKind.WILD)
        self.battle_menu = "main"
        self.battle_selection = 0
        self.capture_animation = None
        self.state = STATE_BATTLE
        self.audio.play("battle")

    def handle_battle_input(self, event):
        battle = self.active_battle
        if battle is None:
            self.state = STATE_TOWN
            return
        if self.capture_animation is not None:
            return
        if battle.result is not None:
            if event.key == pygame.K_RETURN:
                self.finish_battle()
            return
        if self.battle_menu == "main":
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.battle_selection = (self.battle_selection - 1) % 3
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.battle_selection = (self.battle_selection + 1) % 3
            elif event.key == pygame.K_RETURN:
                if self.battle_selection == 0:
                    self.battle_menu = "moves"
                    self.battle_selection = 0
                elif self.battle_selection == 1:
                    self.battle_menu = "bag"
                    self.battle_selection = 0
                else:
                    battle.attempt_escape()
        elif self.battle_menu == "moves":
            move_count = len(battle.player_pokemon.known_moves)
            if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.battle_menu = "main"
                self.battle_selection = 0
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.battle_selection = max(0, self.battle_selection - 1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.battle_selection = min(move_count - 1, self.battle_selection + 1)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.battle_selection = max(0, self.battle_selection - 2)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.battle_selection = min(move_count - 1, self.battle_selection + 2)
            elif event.key == pygame.K_RETURN and move_count:
                battle.execute_round([BattleAction("player", 0, self.battle_selection)])
                self.battle_menu = "main"
                self.battle_selection = 0
        elif self.battle_menu == "bag":
            ball_ids = self.available_ball_ids()
            if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.battle_menu = "main"
                self.battle_selection = 0
            elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_UP, pygame.K_w) and ball_ids:
                self.battle_selection = (self.battle_selection - 1) % len(ball_ids)
            elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN, pygame.K_s) and ball_ids:
                self.battle_selection = (self.battle_selection + 1) % len(ball_ids)
            elif event.key == pygame.K_RETURN and ball_ids:
                self.throw_ball(ball_ids[self.battle_selection])

    def available_ball_ids(self):
        return [
            item_id for item_id, count in self.inventory.items.items()
            if count > 0 and ITEM_DATABASE.get(item_id) and ITEM_DATABASE[item_id].category == "ball"
        ]

    def throw_ball(self, ball_id):
        battle = self.active_battle
        if battle is None or battle.result is not None:
            return
        if battle.kind != BattleKind.WILD:
            battle.log.append("You cannot capture another trainer's Pokémon!")
            self.battle_menu = "main"
            self.battle_selection = 0
            return
        if not self.party.has_capture_capacity():
            battle.log.append("Your party and all storage boxes are full!")
            self.battle_menu = "main"
            self.battle_selection = 0
            return
        ball = ITEM_DATABASE[ball_id]
        encounter = self.active_encounter
        context = CaptureContext(
            rarity=encounter.rarity,
            zone=encounter.zone,
            time_of_day=self.encounter_context.time_of_day,
            legendary_event=encounter.legendary_event,
        )
        result = self.capture_calculator.attempt(battle.enemy_pokemon, ball, context)
        if result.blocked_reason:
            battle.log.append(result.blocked_reason)
            self.battle_menu = "main"
            self.battle_selection = 0
            return
        if not self.inventory.remove(ball_id, 1):
            battle.log.append(f"No {ball.name}s remaining!")
            return
        battle.log.append(f"You threw a {ball.name}!")
        self.capture_animation = CaptureAnimation(result, ball_id)

    def finish_capture_animation(self):
        result = self.capture_animation.result
        battle = self.active_battle
        self.capture_animation = None
        battle.resolve_capture(result.success)
        if result.success:
            caught = battle.enemy_pokemon
            if self.party.add_pokemon(caught):
                self.player.stats.pokemon_caught += 1
                self.publish_quest_event("catch_species", caught.species.key)
                self.publish_quest_event("capture_count", amount=1)
                placement = self.party.last_placement
                self.audio.play("capture")
                if placement[0] == "party":
                    battle.log.append(f"{caught.display_name} joined your party!")
                else:
                    box = self.party.storage.boxes[placement[1]]
                    battle.log.append(f"{caught.display_name} was sent to {box.name}.")
            else:
                battle.log.append("All storage boxes are full; the capture could not be stored.")
        self.battle_menu = "main"
        self.battle_selection = 0

    def finish_battle(self):
        battle = self.active_battle
        if battle and battle.result and battle.result.winner == "enemy":
            self.party.heal_all()
        if battle and battle.result and battle.result.winner == "player" and self.active_npc is not None:
            self.active_npc.defeated = True
            self.grant_npc_reward(self.active_npc)
            self.publish_quest_event("defeat_trainer", self.active_npc.npc_id)
        if battle and battle.result and battle.result.winner == "player":
            for pokemon in self.party.party:
                if pokemon.current_hp > 0:
                    pokemon.gain_friendship(3)
            if battle.result.levels_gained:
                self.process_evolutions("level")
            self.process_evolutions("friendship")
        self.active_battle = None
        self.active_encounter = None
        self.active_npc = None
        self.capture_animation = None
        self.encounters.reset_grace()
        self.state = STATE_TOWN
        self.save_game()

    def change_area(self, transition):
        """Cross a connection while remaining in the same exploration state."""
        area, destination = self.world.travel(transition)
        self.game_map = area.game_map
        self.player.teleport(*destination)
        self.camera = Camera(self.game_map.pixel_width, self.game_map.pixel_height)
        self.camera.update(*self.player.center, snap=True)
        self.location_banner_timer = 2.5
        self.encounters.reset_grace()
        self.publish_quest_event("visit_area", area.area_id)
        self.save_game()

    def handle_quest_log_input(self, event):
        quests = self.quests.visible_quests()
        if event.key in (pygame.K_ESCAPE, pygame.K_q):
            self.state = STATE_TOWN
        elif event.key in (pygame.K_UP, pygame.K_w) and quests:
            self.quest_selection = (self.quest_selection - 1) % len(quests)
        elif event.key in (pygame.K_DOWN, pygame.K_s) and quests:
            self.quest_selection = (self.quest_selection + 1) % len(quests)

    def draw_title_screen(self):
        self.window.screen.fill((18, 30, 84))
        ticks = pygame.time.get_ticks() / 1000
        for index in range(18):
            x = int((index * 71 + ticks * (8 + index % 3)) % (SCREEN_WIDTH + 30)) - 15
            y = 55 + (index * 83) % (SCREEN_HEIGHT - 110)
            radius = 2 + index % 3
            pygame.draw.circle(self.window.screen, (55, 88, 152), (x, y), radius)
        title_surface = self.title_font.render("Pokemon Beta Blue", True, (255, 224, 108))
        prompt = "ENTER: New Game"
        if self.save_manager.has_save:
            prompt += "   C: Continue"
        prompt_surface = self.body_font.render(prompt, True, (255, 255, 255))
        self.window.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
        self.window.screen.blit(prompt_surface, prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))
        if self.save_message:
            error = self.small_font.render(self.save_message, True, (255, 170, 140))
            self.window.screen.blit(error, error.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 85)))
        version = self.small_font.render(f"Version {GAME_VERSION}", True, (145, 166, 205))
        self.window.screen.blit(version, (SCREEN_WIDTH - version.get_width() - 12, SCREEN_HEIGHT - 30))

    def draw_name_entry(self):
        self.window.screen.fill((12, 20, 48))
        prompt_surface = self.body_font.render("Enter Your Name:", True, (255, 255, 255))
        name_surface = self.body_font.render(self.player_name, True, (255, 255, 255))
        hint_surface = self.small_font.render("Press ENTER to confirm", True, (180, 180, 180))
        self.window.screen.blit(prompt_surface, prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
        self.window.screen.blit(name_surface, name_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        self.window.screen.blit(hint_surface, hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))

    def draw_gender_selection(self):
        self.window.screen.fill((22, 43, 77))
        heading = self.body_font.render("Choose your trainer", True, (255, 236, 126))
        self.window.screen.blit(heading, heading.get_rect(center=(SCREEN_WIDTH // 2, 52)))
        for index, gender in enumerate(self.gender_options):
            card = pygame.Rect(65 + index * 365, 100, 305, 385)
            selected = index == self.gender_selection
            pygame.draw.rect(self.window.screen, (247, 249, 245), card, border_radius=16)
            pygame.draw.rect(self.window.screen, (255, 207, 65) if selected else (90, 111, 137), card, 6, border_radius=16)
            lineup = self.assets.image(f"assets/characters/{gender}_trainers_supplied.png", size=(285, 102))
            self.window.screen.blit(lineup, lineup.get_rect(center=(card.centerx, card.y + 142)))
            label = self.title_font.render(gender.title(), True, (35, 57, 91))
            self.window.screen.blit(label, label.get_rect(center=(card.centerx, card.y + 280)))
            detail = self.small_font.render("Three available looks", True, (74, 89, 108))
            self.window.screen.blit(detail, detail.get_rect(center=(card.centerx, card.y + 330)))
        hint = self.small_font.render("LEFT / RIGHT to choose   •   ENTER to continue", True, (240, 246, 255))
        self.window.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 535)))

    def draw_skin_selection(self):
        self.window.screen.fill((22, 43, 77))
        gender = self.gender_options[self.gender_selection]
        heading = self.body_font.render(f"Choose your {gender} trainer look", True, (255, 236, 126))
        self.window.screen.blit(heading, heading.get_rect(center=(SCREEN_WIDTH // 2, 52)))
        lineup = self.assets.image(f"assets/characters/{gender}_trainers_supplied.png")
        source_width = lineup.get_width() // 3
        style_names = ("Skin 1", "Skin 2", "Skin 3")
        for index in range(3):
            card = pygame.Rect(47 + index * 245, 95, 216, 405)
            selected = index == self.skin_selection
            pygame.draw.rect(self.window.screen, (247, 249, 245), card, border_radius=15)
            pygame.draw.rect(self.window.screen, (255, 207, 65) if selected else (90, 111, 137), card, 6, border_radius=15)
            source = lineup.subsurface((index * source_width, 0, source_width, lineup.get_height()))
            preview = pygame.transform.smoothscale(source, (196, 210))
            self.window.screen.blit(preview, (card.x + 10, card.y + 65))
            label = self.body_font.render(style_names[index], True, (35, 57, 91))
            self.window.screen.blit(label, label.get_rect(center=(card.centerx, card.bottom - 52)))
        hint = self.small_font.render("LEFT / RIGHT to choose   •   ENTER to confirm   •   ESC to go back", True, (240, 246, 255))
        self.window.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 545)))

    def draw_starter_selection(self):
        self.window.screen.fill((29, 65, 104))
        heading = self.body_font.render("Choose your first partner", True, (255, 236, 126))
        self.window.screen.blit(heading, heading.get_rect(center=(SCREEN_WIDTH // 2, 70)))
        for index, key in enumerate(self.starter_options):
            pokemon = create_pokemon(key, 5)
            card = pygame.Rect(70 + index * 245, 145, 205, 310)
            selected = index == self.starter_selection
            pygame.draw.rect(self.window.screen, (248, 251, 255) if selected else (190, 207, 225), card, border_radius=15)
            pygame.draw.rect(self.window.screen, (255, 211, 77) if selected else (55, 77, 105), card, 5, border_radius=15)
            sprite = self.assets.image(pokemon.species.sprite_path, size=(155, 155))
            self.window.screen.blit(sprite, sprite.get_rect(center=(card.centerx, card.y + 105)))
            name = self.body_font.render(pokemon.species.name, True, (27, 45, 72))
            types = self.small_font.render(" / ".join(pokemon.species.types), True, (65, 82, 106))
            self.window.screen.blit(name, name.get_rect(center=(card.centerx, card.y + 220)))
            self.window.screen.blit(types, types.get_rect(center=(card.centerx, card.y + 255)))
        hint = self.small_font.render("LEFT / RIGHT to choose   •   ENTER to confirm", True, (245, 248, 255))
        self.window.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 520)))

    def draw_town(self):
        self.window.screen.fill((0, 0, 0))
        offset_x, offset_y = self.camera.offset
        self.game_map.draw(self.window.screen, offset_x, offset_y)
        for hidden in self.world_events.active_hidden_transitions(
            self.world.current_area_id, self.world_simulation, self.story.flags
        ):
            center = (offset_x + hidden.position[0] * TILE_SIZE + TILE_SIZE // 2, offset_y + hidden.position[1] * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.circle(self.window.screen, (245, 230, 135), center, 12, 2)
            pygame.draw.circle(self.window.screen, (255, 255, 220), center, 3)
        for npc in self.npcs.in_area(self.world.current_area_id):
            npc.draw(self.window.screen, offset_x, offset_y, self.small_font)
        self.player.draw(self.window.screen, offset_x, offset_y)
        draw_world_effects(self.window.screen, self.world_simulation, self.encounter_context)
        if self.location_banner_timer > 0:
            self.draw_location_banner()
        status_bar = pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        pygame.draw.rect(self.window.screen, (10, 10, 30), status_bar)
        stats = self.player.stats
        status_text = self.small_font.render(
            f"{stats.name or 'Unknown'} | Day {self.world_simulation.day} {self.world_simulation.clock_text} | {self.world_simulation.season.title()} | {self.encounter_context.weather.title()} | ${stats.money:,}",
            True,
            (255, 255, 255),
        )
        self.window.screen.blit(status_text, (10, SCREEN_HEIGHT - 32))
        self.draw_quest_tracker()

    def draw_quest_tracker(self):
        active = self.quests.active_quests()
        if active:
            quest, state = active[0]
            objective = next((obj for obj in quest.objectives if state.objectives[obj.objective_id] < obj.required), None)
            if objective:
                panel = pygame.Surface((330, 58), pygame.SRCALPHA)
                panel.fill((12, 26, 56, 215))
                panel.blit(self.small_font.render(quest.title, True, (255, 224, 108)), (10, 7))
                text = self.quests.objective_text(objective, state)
                panel.blit(self.small_font.render(text[:43], True, (235, 242, 255)), (10, 31))
                self.window.screen.blit(panel, (12, 12))
        hint = self.small_font.render("Q: Quests  I: Bag  N: Nursery  M: Link  F6: Wait", True, (235, 242, 255))
        self.window.screen.blit(hint, (SCREEN_WIDTH - hint.get_width() - 12, 12))
        if self.quest_notice_timer > 0 and self.quest_notice:
            notice = self.body_font.render(self.quest_notice, True, (255, 234, 126))
            backing = notice.get_rect(center=(SCREEN_WIDTH // 2, 365)).inflate(28, 18)
            pygame.draw.rect(self.window.screen, (15, 31, 65), backing, border_radius=10)
            self.window.screen.blit(notice, notice.get_rect(center=backing.center))
        events = self.world_events.active_events(self.world.current_area_id, self.world_simulation, self.story.flags)
        if events:
            event_text = self.small_font.render("Event: " + ", ".join(event.name for event in events), True, (255, 235, 135))
            self.window.screen.blit(event_text, (12, 76))

    def draw_quest_log(self):
        self.draw_town()
        veil = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        veil.fill((6, 14, 32, 225))
        self.window.screen.blit(veil, (0, 0))
        panel = pygame.Rect(55, 42, SCREEN_WIDTH - 110, SCREEN_HEIGHT - 84)
        pygame.draw.rect(self.window.screen, (244, 248, 253), panel, border_radius=16)
        pygame.draw.rect(self.window.screen, (42, 71, 118), panel, 4, border_radius=16)
        title = self.body_font.render(f"Quest Journal - {self.story.active_chapter}", True, (35, 70, 132))
        self.window.screen.blit(title, (panel.x + 22, panel.y + 18))
        visible = self.quests.visible_quests()
        if not visible:
            self.window.screen.blit(self.small_font.render("No quests discovered.", True, (52, 65, 84)), (panel.x + 24, panel.y + 80))
            return
        self.quest_selection %= len(visible)
        for index, (quest, state) in enumerate(visible):
            row = pygame.Rect(panel.x + 20, panel.y + 65 + index * 44, 260, 36)
            selected = index == self.quest_selection
            pygame.draw.rect(self.window.screen, (62, 103, 172) if selected else (220, 229, 240), row, border_radius=7)
            marker = "[Done]" if state.status == "completed" else f"[{quest.kind.title()}]"
            color = (255, 255, 255) if selected else (35, 49, 70)
            self.window.screen.blit(self.small_font.render(f"{marker} {quest.title}"[:31], True, color), (row.x + 9, row.y + 7))
        quest, state = visible[self.quest_selection]
        detail_x = panel.x + 310
        self.window.screen.blit(self.body_font.render(quest.title, True, (35, 70, 132)), (detail_x, panel.y + 72))
        y = panel.y + 112
        for line in wrap_text(quest.description, self.small_font, panel.right - detail_x - 22):
            self.window.screen.blit(self.small_font.render(line, True, (48, 61, 82)), (detail_x, y))
            y += 24
        y += 12
        for objective in quest.objectives:
            done = state.objectives[objective.objective_id] >= objective.required
            color = (45, 130, 76) if done else (48, 61, 82)
            self.window.screen.blit(self.small_font.render(self.quests.objective_text(objective, state), True, color), (detail_x, y))
            y += 29
        rewards = []
        if quest.rewards.get("money"):
            rewards.append(f"${quest.rewards['money']:,}")
        rewards.extend(f"{count}x {ITEM_DATABASE[item_id].name}" for item_id, count in quest.rewards.get("items", {}).items())
        reward_text = "Rewards: " + (", ".join(rewards) or "Story progress")
        self.window.screen.blit(self.small_font.render(reward_text, True, (151, 94, 25)), (detail_x, panel.bottom - 65))
        hint = self.small_font.render("UP/DOWN: select   Q or ESC: close", True, (85, 98, 116))
        self.window.screen.blit(hint, (panel.x + 22, panel.bottom - 32))

    def draw_location_banner(self):
        area = self.world.current_area
        panel = pygame.Surface((440, 70), pygame.SRCALPHA)
        panel.fill((12, 26, 56, 220))
        title = self.body_font.render(area.name, True, (255, 228, 105))
        description = self.small_font.render(area.description, True, (235, 242, 255))
        panel.blit(title, title.get_rect(center=(220, 24)))
        panel.blit(description, description.get_rect(center=(220, 52)))
        self.window.screen.blit(panel, panel.get_rect(midtop=(SCREEN_WIDTH // 2, 18)))

    def draw_dialogue(self):
        panel = pygame.Rect(35, 405, SCREEN_WIDTH - 70, 160)
        pygame.draw.rect(self.window.screen, (247, 250, 255), panel, border_radius=14)
        pygame.draw.rect(self.window.screen, (35, 57, 91), panel, 4, border_radius=14)
        name = self.body_font.render(self.active_npc.name, True, (37, 76, 145))
        self.window.screen.blit(name, (panel.x + 18, panel.y + 12))
        line = self.dialogue_lines[min(self.dialogue_index, len(self.dialogue_lines) - 1)]
        for index, wrapped in enumerate(wrap_text(line, self.small_font, panel.width - 40)):
            text = self.small_font.render(wrapped, True, (31, 43, 61))
            self.window.screen.blit(text, (panel.x + 20, panel.y + 55 + index * 25))
        hint = self.small_font.render("ENTER: continue   •   ESCAPE: close", True, (95, 107, 125))
        self.window.screen.blit(hint, (panel.right - hint.get_width() - 18, panel.bottom - 30))

    def draw_shop(self):
        self.draw_town()
        draw_shop_screen(
            self.window.screen, self.active_npc, self.inventory, self.player.stats.money,
            (self.title_font, self.body_font, self.small_font), self.shop_mode,
            self.shop_selection, self.shop_message,
        )

    def draw_wild_encounter(self):
        encounter = self.active_encounter
        if encounter is None:
            return
        veil = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        veil.fill((5, 12, 28, 210))
        self.window.screen.blit(veil, (0, 0))

        panel = pygame.Rect(145, 80, 510, 420)
        pygame.draw.rect(self.window.screen, (244, 249, 255), panel, border_radius=18)
        pygame.draw.rect(self.window.screen, (35, 56, 92), panel, 5, border_radius=18)
        pokemon = encounter.pokemon
        sprite = self.assets.image(pokemon.species.sprite_path, size=(180, 180))
        self.window.screen.blit(sprite, sprite.get_rect(center=(SCREEN_WIDTH // 2, 255)))

        rarity_colors = {
            "common": (80, 110, 130), "uncommon": (42, 145, 84),
            "rare": (61, 102, 205), "legendary": (190, 126, 20),
        }
        heading = self.body_font.render("A wild Pokémon appeared!", True, (30, 47, 75))
        name = self.title_font.render(pokemon.species.name, True, (25, 43, 74))
        details = self.small_font.render(
            f"Lv. {pokemon.level}  •  {encounter.rarity.title()}  •  {encounter.zone.title()}",
            True,
            rarity_colors[encounter.rarity],
        )
        hint = self.small_font.render("ENTER: battle   •   ESCAPE: retreat", True, (76, 88, 108))
        self.window.screen.blit(heading, heading.get_rect(center=(SCREEN_WIDTH // 2, 122)))
        self.window.screen.blit(name, name.get_rect(center=(SCREEN_WIDTH // 2, 382)))
        self.window.screen.blit(details, details.get_rect(center=(SCREEN_WIDTH // 2, 430)))
        self.window.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 474)))

    def run(self):
        running = True
        dt = 0.0
        while running:
            running = self.handle_events()
            self.update(dt)
            self.window.screen.fill((0, 0, 0))
            if self.state == STATE_TITLE:
                self.draw_title_screen()
            elif self.state == STATE_NAME_ENTRY:
                self.draw_name_entry()
            elif self.state == STATE_GENDER_SELECT:
                self.draw_gender_selection()
            elif self.state == STATE_SKIN_SELECT:
                self.draw_skin_selection()
            elif self.state == STATE_STARTER_SELECT:
                self.draw_starter_selection()
            elif self.state == STATE_TOWN:
                self.draw_town()
            elif self.state == STATE_QUEST_LOG:
                self.draw_quest_log()
            elif self.state == STATE_INVENTORY:
                draw_inventory_screen(
                    self.window.screen, self.inventory, self.party,
                    (self.title_font, self.body_font, self.small_font),
                    self.inventory_pocket, self.inventory_selection, self.inventory_target,
                    self.inventory_targeting, self.inventory_message,
                )
            elif self.state == STATE_NURSERY:
                draw_nursery_screen(
                    self.window.screen, self.party, self.nursery,
                    (self.title_font, self.body_font, self.small_font),
                    self.nursery_parent_a, self.nursery_parent_b, self.nursery_message,
                )
            elif self.state == STATE_MULTIPLAYER:
                draw_multiplayer_screen(
                    self.window.screen, self.player_identity, self.multiplayer,
                    (self.title_font, self.body_font, self.small_font),
                )
            elif self.state == STATE_REGION_MAP:
                self.region_map.draw(
                    self.window.screen, self.assets, self.world.current_area_id, self.story.flags,
                    (self.title_font, self.body_font, self.small_font),
                )
            elif self.state == STATE_DIALOGUE:
                self.draw_town()
                self.draw_dialogue()
            elif self.state == STATE_SHOP:
                self.draw_shop()
            elif self.state == STATE_WILD_ENCOUNTER:
                self.draw_town()
                self.draw_wild_encounter()
            elif self.state == STATE_BATTLE:
                draw_battle_screen(
                    self.window.screen, self.active_battle, self.assets,
                    self.title_font, self.body_font, self.small_font,
                    self.battle_menu, self.battle_selection,
                    self.inventory, self.capture_animation,
                )

            self.performance.draw(self.window.screen, self.small_font, self.assets)

            self.window.present()
            dt = min(self.clock.tick(self.settings.target_fps) / 1000.0, 0.05)
            self.performance.record(dt)

        self.save_game()
        self.audio.shutdown()
        pygame.quit()


def _opposite_direction(direction):
    vertical = "down" if "up" in direction else "up" if "down" in direction else ""
    horizontal = "right" if "left" in direction else "left" if "right" in direction else ""
    return "_".join(part for part in (vertical, horizontal) if part) or "down"


def main():
    """Run the game and return a process exit code."""
    Game().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
