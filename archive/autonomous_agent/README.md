# Frogger Game

A classic Frogger arcade game implementation using Pygame.

## Installation

```bash
pip install pygame
```

## How to Play

```bash
python frogger_game.py
```

## Controls

- **Arrow Keys**: Move the frog
  - UP: Move forward
  - DOWN: Move backward
  - LEFT: Move left
  - RIGHT: Move right

## Objective

- Guide your frog from the bottom of the screen to the goal at the top
- Avoid vehicles on the road (gray area)
- Jump on logs to cross the water (blue area)
- Don't fall in the water!
- You have 3 lives
- Earn points for moving forward and reaching the goal

## Game Elements

- **Green Frog**: Your character
- **Red/Yellow Vehicles**: Obstacles on the road - avoid them!
- **Brown Logs**: Platforms in the water - jump on them!
- **Blue Water**: Dangerous - stay on logs!
- **Green Goal Zone**: Reach here to score big points!

## Scoring

- Move forward: +10 points
- Reach the goal: +100 points

## Game Over

- You lose a life when:
  - Hit by a vehicle
  - Fall in the water (not on a log)
- Game ends when all lives are lost

Good luck!
