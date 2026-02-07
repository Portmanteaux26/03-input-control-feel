# A3 — Input Mapping + Control Feel Tuning (Week 3)
Small Pygame prototype demonstrating an input mapping layer, discrete actions with constraints, and multiple control-feel presets.

## How to run
1) (Optional) Create/activate a virtual environment.
2) Install dependencies:
   
    pip install -r requirements.txt
4) Run:
   
    python main.py

## Controls
### Core
- **Start (title):** Space
- **Move:** depends on scheme (see below)
- **Dash:** Shift (Left or Right Shift)
- **Jump (Platformer mode):** Space or Up (double-jump enabled)
- **Reset:** R
- **Quit:** Esc
### Toggles
- **Toggle mode (Top-down / Platformer):** P
- **Cycle control scheme (WASD / IJKL / Arrows):** C
- **Cycle boundary mode (Clamp / Wrap / Bounce):** Tab
- **Debug overlay:** F1
### Feel presets
- **1:** tight
- **2:** floaty
- **3:** heavy
- **4:** icy
- **5:** underwater
  
Notes:
- Arrow keys are always supported for movement (even if another scheme is selected).

## This week
- **Input mapping layer:** Added an `Action` enum and an action→keys mapping so gameplay uses actions (MOVE/JUMP/DASH/START) rather than hard-coded keys throughout the logic.
- **Dash improvement:** Dash now prefers the **currently held direction**, with a short **direction buffer** (so you can tap a direction and dash immediately after).
- **Dash “burst” feel:** Added a brief **overspeed window** after dashing (temporary higher speed cap), making dash noticeable even when already near max speed.
- **Basic dash anim:** Added simple pulse animation when dashing to increase visual feedback that a dash was used.
- **New feel presets:** Added **icy** and **underwater** presets in addition to the starter presets.
- **Platformer upgrade:** Added **double-jump** (2 jumps before landing; second jump is slightly weaker).

## Preset tuning notes + playtest observations
- **tight (baseline):** High accel + high friction, medium max speed, medium gravity/jump → snappy, precise control.
  - Observation: easy to stop exactly on a point; short taps move predictably.
- **floaty:** Lower gravity + lower jump speed, reduced accel/friction → more airtime and softer movement.
  - Observation: platformer jumps hang longer and land gently; top-down starts/turns feel less sharp.
- **heavy:** Higher gravity, lower accel/max speed, low friction → weighty movement and faster drops.
  - Observation: you must plan turns early; platformer falls feel noticeably faster.
- **icy:** Very low friction, higher max speed, medium accel → low traction, long slides, wide turns.
  - Observation: releasing input still glides a long distance; reversing direction takes time to “catch.”
- **underwater:** Very low gravity, low max speed, moderate friction (drag), low accel/jump → buoyant but sluggish, like pushing through water.
  - Observation: movement feels slow and controlled; platformer rises/falls slowly but doesn’t “pop” very high.
