### Pygame - Game Notes - Game 1 - Shoot Em Up

A few notes on building a simple 'Shoot Em Up' type game with Pygame.

#### Contents
* Intro
* Different types
* Game versions
  * Sprites/Basic
* References

#### Intro
A **Shoot Em Up**, or **STG** in Japan, style game simply allows a player to fire bullets and other weapons at an enemy, whilst trying to avoid their attack.

The classic example, of course, is **Space Invaders**, which largely popularised this genre of game.

However, there are many different examples of this style of game.

#### Different types
Whilst the general gameplay is the same for each type of STG, there are a few notable variants. For example, we may consider viewpoint and movement as an easy way of differentiating various different examples. These may include,

  * fixed shooters
  * rail shooters
  * scrolling shooters
  * ...

#### Game versions
The following versions are available:

##### Sprites/Basic
  * v0.1 - shooter0.1.py
    * add a sprite for the ship, abstract the ship object to a parent class, and move the ship around the screen...
  * v0.2 - shooter0.2.py
    * player object with horizontal control - includes limits on both sides of x-axis for sprite movement
    * enemy objects moving down the screen
    * enemy objects have random path on x and y axis
    * enemy objects recreated as they leave the game bounding of the game window...

#### References
* [Shoot Em Up](https://en.wikipedia.org/wiki/Shoot_'em_up)
