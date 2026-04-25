# Simple RPG Design Spec

**Date:** 2026-04-25
**Author:** OpenCode
**Status:** Approved

## Overview

A simple turn-based text RPG built with Python and Pydantic. Players battle random enemies, level up, and eventually defeat a boss.

## Requirements

- Text-based input/output
- 5-10 regular enemies + 1 boss
- Random enemy encounters
- Level up system
- Turn-based combat with attack and potion actions
- Boss unlocks after defeating 5 enemies OR reaching level 3

## Architecture

```
app/
├── models/
│   ├── character_model.py      # Base class (existing)
│   ├── player_model.py         # Player model
│   ├── enemy_model.py          # Enemy model
│   └── enemy_data.py           # Enemy definitions
├── game/
│   ├── battle.py               # Battle logic
│   └── exp.py                  # Experience and level-up logic
└── main.py                     # Game loop and UI
```

**Design Principles:**
- Immutable data models using Pydantic
- Pure functions for game logic
- Side effects only in main.py (UI and user input)
- Clear separation between logic and presentation

## Data Models

### CharacterModel (Existing)
```python
class CharacterModel(BaseModel):
    name: str
    max_hp: int  # gt=0
    hp: int  # ge=0, cannot exceed max_hp
    attack: int  # ge=0
    defense: int  # ge=0

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> CharacterModel:
        return self.model_copy(update={"hp": max(0, self.hp - amount)})

    def heal_full(self) -> CharacterModel:
        return self.model_copy(update={"hp": self.max_hp})
```

### PlayerModel
```python
class PlayerModel(CharacterModel):
    level: int = 1
    exp: int = 0
    next_exp: int = 10
    potions: int = 3

    def gain_exp(self, amount: int) -> PlayerModel:
        # Returns new player with added exp, potentially leveled up

    def use_potion(self) -> PlayerModel:
        # Returns new player with potions-1 and hp healed

    def add_potion(self, amount: int) -> PlayerModel:
        # Returns new player with potions+amount
```

**Initial Stats:**
- max_hp: 30
- attack: 5
- defense: 1
- level: 1
- exp: 0
- next_exp: 10
- potions: 3

**Level Up Bonuses:**
- max_hp += 5
- attack += 2
- defense += 1
- next_exp = int(next_exp * 1.5)
- HP fully healed

### EnemyModel
```python
class EnemyModel(CharacterModel):
    exp_reward: int  # EXP given when defeated
    is_boss: bool  # True for boss enemy
```

### EnemyData
Defines 5-10 regular enemies and 1 boss with varying stats.

Examples:
- Slime: HP 10, attack 3, defense 0, exp 5
- Goblin: HP 15, attack 4, defense 1, exp 8
- Dragon (Boss): HP 100, attack 15, defense 5, exp 100

## Game Logic

### Combat System

**Damage Calculation:**
```python
def calculate_damage(attacker: CharacterModel, defender: CharacterModel) -> int:
    return max(1, attacker.attack - defender.defense)
```

**Attack Execution:**
```python
def execute_attack(attacker: CharacterModel, defender: CharacterModel) -> tuple[CharacterModel, int]:
    damage = calculate_damage(attacker, defender)
    new_defender = defender.take_damage(damage)
    return (new_defender, damage)
```

**Player Turn:**
```python
def player_turn(player: PlayerModel, enemy: EnemyModel, action: str) -> tuple[PlayerModel, EnemyModel, str]:
    # Action: "attack" or "potion"
    # Returns (new_player, new_enemy, log_message)
```

**Enemy Turn:**
```python
def enemy_turn(enemy: EnemyModel, player: PlayerModel) -> tuple[PlayerModel, str]:
    # Enemy attacks player
    # Returns (new_player, log_message)
```

**Battle Loop:**
```python
def battle(player: PlayerModel, enemy: EnemyModel) -> tuple[PlayerModel, bool, str]:
    # Main battle loop
    # Returns (updated_player, victory, result_message)
```

**Battle Flow:**
1. Show player and enemy status
2. Player chooses action (attack or potion)
3. Execute player action
4. Check if enemy defeated
5. If enemy alive, enemy attacks
6. Check if player defeated
7. Repeat until one side is defeated

### Experience and Level Up

```python
def gain_exp_and_check_level_up(player: PlayerModel, exp: int) -> tuple[PlayerModel, bool]:
    # Add exp, check for level up(s)
    # Returns (updated_player, leveled_up)
```

When player gains enough exp:
- Increment level
- Subtract used exp from next_exp
- Update stats (HP+5, attack+2, defense+1)
- Calculate new next_exp (multiply by 1.5)
- Fully heal HP

## Main Game Loop

### Flow
```
Start Game
  ↓
Input Player Name
  ↓
Initialize Player
  ↓
[Main Loop]
  Show Menu:
  1) Fight Enemy
  2) Rest at Inn (full HP heal)
  3) Challenge Boss (unlocks after 5 defeats OR level 3)
  q) Quit
  ↓
  - Fight Enemy:
    - Choose random enemy
    - Run battle
    - If player wins: gain exp, increment defeat count
    - If player loses: GAME OVER
  - Rest: fully heal HP
  - Challenge Boss:
    - Run boss battle
    - If player wins: VICTORY
    - If player loses: GAME OVER
  - Quit: End game
```

### UI Functions

- `show_main_menu(defeated_count: int, player_level: int)` - Display menu options
- `get_user_choice() -> str` - Get and validate user input
- `choose_random_enemy() -> EnemyModel` - Select random enemy from enemy data
- `show_status(player: PlayerModel, defeated_count: int)` - Display player stats
- `show_battle_log(logs: list[str])` - Display battle messages

### Main Loop State

Maintain:
- `player: PlayerModel` - Current player state
- `defeated_count: int` - Number of enemies defeated
- `game_over: bool` - Whether game has ended

## Testing

### Unit Tests
- Model validation (negative HP, etc.)
- Damage calculation edge cases
- Level up calculation
- Experience accumulation

### Integration Tests
- Complete battle scenario (player wins)
- Complete battle scenario (player loses)
- Level up during battle
- Potion usage
- Multiple level ups from single battle

## Error Handling

- Invalid user input: Re-prompt with message
- Model validation errors: Should not occur in gameplay due to input validation, but will be visible during development

## Future Enhancements (Out of Scope)

- Multiple weapon types
- Skill system
- Equipment
- Multiple dungeons
- Save/load game
