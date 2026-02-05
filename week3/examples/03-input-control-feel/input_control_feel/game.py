from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pygame


class BoundaryMode(str, Enum):
    CLAMP = "clamp"
    WRAP = "wrap"
    BOUNCE = "bounce"

class ControlScheme(str, Enum):
    WASD = "WASD"
    ARROWS = "ARROWS"
    IJKL = "IJKL"

class Action(str, Enum):
    START = "START"
    MOVE_LEFT = "MOVE_LEFT"
    MOVE_RIGHT = "MOVE_RIGHT"
    MOVE_UP = "MOVE_UP"
    MOVE_DOWN = "MOVE_DOWN"
    JUMP = "JUMP"
    DASH = "DASH"

@dataclass(frozen=True)
class FeelPreset:
    name: str

    # Top-down feel
    accel: float
    max_speed: float
    friction: float

    # Platformer feel
    gravity: float
    jump_speed: float

class Game:
    fps = 60

    SCREEN_W, SCREEN_H = 960, 540
    HUD_H = 54
    PLAYFIELD_PADDING = 10

    PLAYER_SIZE = 32

    DASH_IMPULSE = 760.0
    DASH_COOLDOWN = 0.65
    DASH_DIR_BUFFER = 0.12  # seconds
    DASH_BOOST_TIME = 0.12  # seconds you’re allowed to exceed max_speed
    DASH_SPEED_MULT = 1.8  # max_speed multiplier during that window

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.font = pygame.font.SysFont(None, 22)
        self.big_font = pygame.font.SysFont(None, 48)

        self.screen_rect = pygame.Rect(0, 0, self.SCREEN_W, self.SCREEN_H)
        self.playfield = pygame.Rect(
            self.PLAYFIELD_PADDING,
            self.HUD_H + self.PLAYFIELD_PADDING,
            self.SCREEN_W - 2 * self.PLAYFIELD_PADDING,
            self.SCREEN_H - self.HUD_H - 2 * self.PLAYFIELD_PADDING,
        )

        self.boundary_mode = BoundaryMode.CLAMP
        self.platformer_mode = False
        self.state = "title"  # title | play

        self.player_rect = pygame.Rect(0, 0, self.PLAYER_SIZE, self.PLAYER_SIZE)
        self.player_pos = pygame.Vector2(self.playfield.center)
        self.player_vel = pygame.Vector2(0, 0)
        self.player_rect.center = self.player_pos

        self.on_ground = True
        self.jump_requested = False

        self.control_scheme = ControlScheme.WASD
        self.debug = False

        self.presets = [
            FeelPreset(
                name="tight",
                accel=3200.0,
                max_speed=520.0,
                friction=14.0,
                gravity=2600.0,
                jump_speed=860.0,
            ),
            FeelPreset(
                name="floaty",
                accel=1900.0,
                max_speed=560.0,
                friction=6.0,
                gravity=1700.0,
                jump_speed=760.0,
            ),
            FeelPreset(
                name="heavy",
                accel=1400.0,
                max_speed=440.0,
                friction=4.2,
                gravity=3200.0,
                jump_speed=820.0,
            ),
            FeelPreset(
                name="icy",
                accel=1600.0,
                max_speed=680.0,
                friction=1.4,
                gravity=2600.0,
                jump_speed=860.0,
            ),
        ]
        self.preset_idx = 0

        self.dash_cooldown_left = 0.0
        self.dash_dir_buffer_left = 0.0
        self.dash_boost_left = 0.0
        self.last_move_dir = pygame.Vector2(1, 0)


    @property
    def preset(self) -> FeelPreset:
        return self.presets[self.preset_idx]

    def _cycle_boundary_mode(self) -> None:
        modes = list(BoundaryMode)
        idx = modes.index(self.boundary_mode)
        self.boundary_mode = modes[(idx + 1) % len(modes)]

    def _cycle_control_scheme(self) -> None:
        schemes = list(ControlScheme)
        idx = schemes.index(self.control_scheme)
        self.control_scheme = schemes[(idx + 1) % len(schemes)]

    def _reset(self, keep_state: bool = False) -> None:
        self.player_pos = pygame.Vector2(self.playfield.center)
        self.player_vel = pygame.Vector2(0, 0)
        self.player_rect.center = self.player_pos
        self.on_ground = True
        self.jump_requested = False
        self.dash_cooldown_left = 0.0
        self.dash_boost_left = 0.0
        self.last_move_dir = pygame.Vector2(1, 0)

        if not keep_state:
            self.state = "play"

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if event.key == pygame.K_F1:
            self.debug = not self.debug
            return

        if event.key == pygame.K_TAB:
            self._cycle_boundary_mode()
            return

        if event.key == pygame.K_c:
            self._cycle_control_scheme()
            return

        if event.key == pygame.K_p:
            self.platformer_mode = not self.platformer_mode
            if self.state != "title":
                self._reset(keep_state=True)
            return

        if event.key == pygame.K_r:
            self._reset(keep_state=(self.state == "title"))
            return

        if self.state == "title" and self._key_triggers(Action.START, event.key):
            self.state = "play"
            self._reset(keep_state=True)
            return

        if event.key == pygame.K_1:
            self.preset_idx = 0
            return
        if event.key == pygame.K_2:
            self.preset_idx = 1
            return
        if event.key == pygame.K_3:
            self.preset_idx = 2
            return
        if event.key == pygame.K_4:
            self.preset_idx = 3
            return

        if self.state != "play":
            return

        # Discrete actions (now via mapping)
        if self._key_triggers(Action.DASH, event.key):
            self._try_dash()
            return

        if self.platformer_mode and self._key_triggers(Action.JUMP, event.key):
            self.jump_requested = True

    def _scheme_bindings(self) -> dict[Action, set[int]]:
        # per-scheme movement bindings
        if self.control_scheme == ControlScheme.WASD:
            return {
                Action.MOVE_LEFT: {pygame.K_a},
                Action.MOVE_RIGHT: {pygame.K_d},
                Action.MOVE_UP: {pygame.K_w},
                Action.MOVE_DOWN: {pygame.K_s},
            }
        if self.control_scheme == ControlScheme.IJKL:
            return {
                Action.MOVE_LEFT: {pygame.K_j},
                Action.MOVE_RIGHT: {pygame.K_l},
                Action.MOVE_UP: {pygame.K_i},
                Action.MOVE_DOWN: {pygame.K_k},
            }
        # ARROWS
        return {
            Action.MOVE_LEFT: {pygame.K_LEFT},
            Action.MOVE_RIGHT: {pygame.K_RIGHT},
            Action.MOVE_UP: {pygame.K_UP},
            Action.MOVE_DOWN: {pygame.K_DOWN},
        }

    def _action_keys(self, action: Action) -> set[int]:
        # global bindings for actions (keeps your "always allow arrows" idea but via mapping)
        always: dict[Action, set[int]] = {
            Action.MOVE_LEFT: {pygame.K_LEFT},
            Action.MOVE_RIGHT: {pygame.K_RIGHT},
            Action.MOVE_UP: {pygame.K_UP},
            Action.MOVE_DOWN: {pygame.K_DOWN},
            Action.START: {pygame.K_SPACE},
            Action.DASH: {pygame.K_LSHIFT, pygame.K_RSHIFT},
            Action.JUMP: {pygame.K_SPACE, pygame.K_UP},  # platformer jump
        }
        scheme = self._scheme_bindings()
        return set(scheme.get(action, set())) | set(always.get(action, set()))

    def _key_triggers(self, action: Action, key: int) -> bool:
        return key in self._action_keys(action)

    def _is_action_down(self, keys: pygame.key.ScancodeWrapper, action: Action) -> bool:
        return any(keys[k] for k in self._action_keys(action))

    def _read_direction(self) -> pygame.Vector2:
        keys = pygame.key.get_pressed()

        x = 0
        y = 0
        if self._is_action_down(keys, Action.MOVE_LEFT):
            x -= 1
        if self._is_action_down(keys, Action.MOVE_RIGHT):
            x += 1
        if self._is_action_down(keys, Action.MOVE_UP):
            y -= 1
        if self._is_action_down(keys, Action.MOVE_DOWN):
            y += 1

        direction = pygame.Vector2(x, y)
        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.last_move_dir.update(direction)
            self.dash_dir_buffer_left = self.DASH_DIR_BUFFER

        return direction

    def _read_horizontal(self) -> float:
        keys = pygame.key.get_pressed()

        x = 0
        if self._is_action_down(keys, Action.MOVE_LEFT):
            x -= 1
        if self._is_action_down(keys, Action.MOVE_RIGHT):
            x += 1
        if x != 0:
            self.last_move_dir.update(pygame.Vector2(x, 0).normalize())
            self.dash_dir_buffer_left = self.DASH_DIR_BUFFER

        return float(x)

    def _apply_platformer_vertical_bounds(self) -> None:
        # Treat the bottom of the playfield as "ground".
        if self.player_rect.bottom >= self.playfield.bottom:
            self.player_rect.bottom = self.playfield.bottom
            self.player_vel.y = 0
            self.on_ground = True

        # Prevent leaving the top of the playfield.
        if self.player_rect.top < self.playfield.top:
            self.player_rect.top = self.playfield.top
            if self.player_vel.y < 0:
                self.player_vel.y = 0

        self.player_pos.update(self.player_rect.center)

    def _apply_bounds_player(self) -> None:
        if self.boundary_mode == BoundaryMode.CLAMP:
            self.player_rect.clamp_ip(self.playfield)
            self.player_pos.update(self.player_rect.center)
            return

        if self.boundary_mode == BoundaryMode.WRAP:
            if self.player_rect.right < self.playfield.left:
                self.player_rect.left = self.playfield.right
            elif self.player_rect.left > self.playfield.right:
                self.player_rect.right = self.playfield.left

            if self.player_rect.bottom < self.playfield.top:
                self.player_rect.top = self.playfield.bottom
            elif self.player_rect.top > self.playfield.bottom:
                self.player_rect.bottom = self.playfield.top

            self.player_pos.update(self.player_rect.center)
            return

        # BOUNCE
        bounced = False
        if self.player_rect.left < self.playfield.left:
            self.player_rect.left = self.playfield.left
            self.player_vel.x *= -1
            bounced = True
        elif self.player_rect.right > self.playfield.right:
            self.player_rect.right = self.playfield.right
            self.player_vel.x *= -1
            bounced = True

        if self.player_rect.top < self.playfield.top:
            self.player_rect.top = self.playfield.top
            self.player_vel.y *= -1
            bounced = True
        elif self.player_rect.bottom > self.playfield.bottom:
            self.player_rect.bottom = self.playfield.bottom
            self.player_vel.y *= -1
            bounced = True

        if bounced:
            self.player_pos.update(self.player_rect.center)

    def _try_dash(self) -> None:
        if self.dash_cooldown_left > 0:
            return

        # 1) Prefer currently held direction
        if self.platformer_mode:
            held = pygame.Vector2(self._read_horizontal(), 0)
        else:
            held = self._read_direction()  # already normalized in your version

        if held.length_squared() > 0:
            dash_dir = held.normalize()
        # 2) Otherwise allow a short buffer of last direction
        elif self.dash_dir_buffer_left > 0 and self.last_move_dir.length_squared() > 0:
            dash_dir = pygame.Vector2(self.last_move_dir).normalize()
        # 3) Otherwise no dash (traditional + avoids “random” feeling)
        else:
            return

        self.player_vel += dash_dir * self.DASH_IMPULSE
        self.dash_cooldown_left = self.DASH_COOLDOWN
        self.dash_boost_left = self.DASH_BOOST_TIME

    def update(self, dt: float) -> None:
        if self.state != "play":
            return

        if self.dash_cooldown_left > 0:
            self.dash_cooldown_left = max(0.0, self.dash_cooldown_left - dt)

        if self.dash_boost_left > 0:
            self.dash_boost_left = max(0.0, self.dash_boost_left - dt)

        self.dash_dir_buffer_left = max(0.0, self.dash_dir_buffer_left - dt)

        p = self.preset

        if self.platformer_mode:
            x = self._read_horizontal()

            # Horizontal accel; no vertical input (gravity handles Y).
            self.player_vel.x += x * p.accel * dt
            if x == 0:
                self.player_vel.x -= self.player_vel.x * min(1.0, p.friction * dt)
            cap = p.max_speed * (self.DASH_SPEED_MULT if self.dash_boost_left > 0 else 1.0)
            self.player_vel.x = max(-cap, min(cap, self.player_vel.x))

            # Jump is a discrete action.
            if self.jump_requested and self.on_ground:
                self.player_vel.y = -p.jump_speed
                self.on_ground = False
            self.jump_requested = False

            # Gravity.
            self.player_vel.y += p.gravity * dt

            self.player_pos += self.player_vel * dt
            self.player_rect.center = (round(self.player_pos.x), round(self.player_pos.y))

            # Use the existing boundary mode for horizontal bounds.
            prev_y = self.player_rect.centery
            self._apply_bounds_player()
            self.player_rect.centery = prev_y
            self.player_pos.y = prev_y

            # Then apply platformer-specific vertical bounds.
            self._apply_platformer_vertical_bounds()
        else:
            direction = self._read_direction()

            # Accelerate toward direction.
            self.player_vel += direction * p.accel * dt

            # Friction: nudge velocity toward zero when no input.
            if direction.length_squared() == 0:
                self.player_vel -= self.player_vel * min(1.0, p.friction * dt)

            cap = p.max_speed * (self.DASH_SPEED_MULT if self.dash_boost_left > 0 else 1.0)
            if self.player_vel.length() > cap:
                self.player_vel.scale_to_length(cap)

            self.player_pos += self.player_vel * dt
            self.player_rect.center = (round(self.player_pos.x), round(self.player_pos.y))

            self._apply_bounds_player()

    def _draw_hud(self) -> None:
        pygame.draw.rect(self.screen, (46, 52, 64), pygame.Rect(0, 0, self.SCREEN_W, self.HUD_H))

        control = "PLATFORMER" if self.platformer_mode else "TOPDOWN"
        left = (
            f"Bounds: {self.boundary_mode.value.upper()}   Control: {control}   "
            f"Scheme: {self.control_scheme.value}   Feel: {self.preset.name}"
        )

        dash = "READY" if self.dash_cooldown_left <= 0 else f"CD {self.dash_cooldown_left:0.2f}s"
        right = f"Dash: {dash}"

        left_surf = self.font.render(left, True, (216, 222, 233))
        right_surf = self.font.render(right, True, (216, 222, 233))

        self.screen.blit(left_surf, (14, 16))
        self.screen.blit(right_surf, (self.SCREEN_W - right_surf.get_width() - 14, 16))

    def _draw_debug(self) -> None:
        p = self.preset
        lines = [
            f"vel=({self.player_vel.x:0.1f}, {self.player_vel.y:0.1f})",
            f"accel={p.accel:0.1f}  friction={p.friction:0.1f}  max={p.max_speed:0.1f}",
            f"gravity={p.gravity:0.1f}  jump={p.jump_speed:0.1f}",
            f"last_dir=({self.last_move_dir.x:0.2f},{self.last_move_dir.y:0.2f})",
        ]

        x = 14
        y = self.HUD_H + 10
        for line in lines:
            surf = self.font.render(line, True, (229, 233, 240))
            self.screen.blit(surf, (x, y))
            y += 18

    def _draw_center_message(self, title: str, subtitle: str) -> None:
        title_surf = self.big_font.render(title, True, (236, 239, 244))
        sub_surf = self.font.render(subtitle, True, (216, 222, 233))

        self.screen.blit(
            title_surf,
            (
                self.SCREEN_W // 2 - title_surf.get_width() // 2,
                self.SCREEN_H // 2 - 60,
            ),
        )
        self.screen.blit(
            sub_surf,
            (
                self.SCREEN_W // 2 - sub_surf.get_width() // 2,
                self.SCREEN_H // 2,
            ),
        )

    def draw(self) -> None:
        self.screen.fill((20, 24, 30))

        # Playfield
        pygame.draw.rect(self.screen, (10, 12, 16), self.playfield)
        pygame.draw.rect(self.screen, (76, 86, 106), self.playfield, width=2)

        # Player
        pygame.draw.rect(self.screen, (136, 192, 208), self.player_rect, border_radius=6)

        self._draw_hud()

        if self.debug:
            self._draw_debug()

        if self.state == "title":
            self._draw_center_message(
                "Week 3",
                "Space: start   Shift: dash   1/2/3: feel   C: scheme   P: mode   F1: debug",
            )
