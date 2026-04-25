# RPG Feature Enhancement Design Spec

**Date:** 2026-04-25
**Author:** OpenCode
**Status:** Approved

## Overview

Enhance the existing simple RPG with four new features:
1. Display enemy status after each action
2. Enemy AI with multiple action patterns (attack, wait, flee)
3. Gold system - earn gold from defeating enemies
4. Inn cost - pay gold to rest and heal

## Requirements

### 1. Enemy Status Display
- Show detailed enemy stats after each action
- Format:
  ```
  Slime
  HP: 5/10
  Attack: 3
  Defense: 0
  ```

### 2. Enemy AI Action Patterns
- Three actions: attack (60%), wait (30%), flee (10%)
- **Attack**: Deal damage to player (existing behavior)
- **Wait**: Do nothing, show message like "Slime is resting..."
- **Flee**: Enemy escapes from battle, player gets no EXP or gold

### 3. Gold System
- Player starts with 10 gold
- Earn gold by defeating enemies
- Gold reward is proportional to enemy strength
  - Formula: `int(max_hp * 0.5)` (simple and consistent)
  - Boss drops 5x normal gold
- Display gold in main menu

### 4. Inn Cost
- Rest at Inn costs 10 gold
- Requires 10+ gold to use
- Fully restores HP
- Show error message if insufficient gold

## Architecture

**Design Principles:**
- Maintain immutable Pydantic models
- Keep pure functions for game logic
- Minimal changes to existing structure
- Model-centered approach

## Data Model Changes

### PlayerModel
```python
class PlayerModel(CharacterModel):
    # ... existing fields ...
    gold: int = 10  # NEW: Starting gold

    # NEW METHODS
    def spend_gold(self, amount: int) -> PlayerModel:
        if self.gold >= amount:
            return self.model_copy(update={"gold": self.gold - amount})
        return self  # Or raise error

    def gain_gold(self, amount: int) -> PlayerModel:
        return self.model_copy(update={"gold": self.gold + amount})
```

### EnemyModel
```python
class EnemyModel(CharacterModel):
    # ... existing fields ...
    gold_reward: int = Field(ge=0)  # NEW: Gold dropped when defeated

    # NEW PROPERTY (optional, for display)
    @property
    def gold_reward_display(self) -> str:
        return f"{self.gold_reward}G"
```

### EnemyData Update
- Add `gold_reward` to each enemy definition
- Calculate: `int(max_hp * 0.5)` for regular enemies
- Boss gets 5x gold
- Example:
  ```python
  EnemyModel(name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False)
  EnemyModel(name="Dragon", max_hp=100, hp=100, attack=15, defense=5, exp_reward=100, gold_reward=250, is_boss=True)
  ```

## Game Logic Changes

### Enemy Turn Logic

**Action Types:**
- `"attack"`: Deal damage
- `"wait"`: Skip turn
- `"flee"`: End battle

**Probability Distribution:**
- Attack: 60%
- Wait: 30%
- Flee: 10%

**Updated `enemy_turn` Function:**
```python
def enemy_turn(enemy: EnemyModel, player: PlayerModel) -> tuple[PlayerModel, str, str]:
    """
    Returns: (updated_player, log_message, enemy_action)
    enemy_action: "attack", "wait", or "flee"
    """
    # Determine action based on probabilities
    roll = random.random()
    if roll < 0.6:
        # Attack
        new_player, damage = execute_attack(enemy, player)
        log = f"{enemy.name} attacked {player.name} for {damage} damage!"
        return (new_player, log, "attack")
    elif roll < 0.9:
        # Wait
        log = f"{enemy.name} is resting..."
        return (player, log, "wait")
    else:
        # Flee
        log = f"{enemy.name} fled from battle!"
        return (player, log, "flee")
```

### Battle Loop Updates

**Handle Flee Action:**
- If enemy action is "flee", break battle loop
- No EXP or gold rewarded
- Return special result indicating enemy fled

**Status Display:**
- After each turn (player and enemy), display enemy status
- Use new function: `show_enemy_status(enemy: EnemyModel) -> str`

**Victory Rewards:**
- In addition to EXP, also award gold
- Return both EXP and gold from battle function

**Updated Battle Function Signature:**
```python
def battle(
    player: PlayerModel,
    enemy: EnemyModel,
    player_action_provider: Optional[Callable[[PlayerModel, EnemyModel], str]] = None,
) -> tuple[PlayerModel, bool, str, int, int]:
    """
    Returns: (updated_player, victory, result_message, exp_gained, gold_gained)
    If enemy fled: exp_gained=0, gold_gained=0, victory=True (battle ended)
    """
```

### Status Display Function

```python
def show_enemy_status(enemy: EnemyModel) -> str:
    return f"""{enemy.name}
HP: {enemy.hp}/{enemy.max_hp}
Attack: {enemy.attack}
Defense: {enemy.defense}"""
```

## Main Game Loop Updates

### Main Menu Display
- Add gold to status display:
  ```
  Defeated: 3 | Level: 2 | Gold: 25G | Potions: 2
  HP: 25/35 | EXP: 5/15
  ```

### Inn Rest Logic
```python
elif choice == "2":
    INN_COST = 10
    if player.gold >= INN_COST:
        player = player.spend_gold(INN_COST)
        player = player.heal_full()
        print(f"\nYou rested at the inn (paid {INN_COST}G). HP fully restored!\n")
    else:
        print("\nYou don't have enough gold! Need 10G.\n")
```

### Battle Result Handling
- After battle, show EXP and gold gained
- Update player with both EXP and gold
- Example:
  ```
  Victory! You defeated Slime!
  Gained 5 EXP and 5 gold.
  ```

## Testing

### PlayerModel Tests
- `test_player_initial_gold` - Verify initial gold is 10
- `test_spend_gold_success` - Spend gold successfully
- `test_spend_gold_insufficient` - Try to spend more than available
- `test_gain_gold` - Earn gold

### EnemyModel Tests
- `test_enemy_gold_reward` - Verify gold reward is set
- `test_boss_gold_reward` - Boss drops more gold

### Battle Logic Tests
- `test_enemy_wait_action` - Enemy waits
- `test_enemy_flee_action` - Enemy flees
- `test_enemy_action_attack` - Enemy attacks
- `test_battle_with_flee` - Complete battle where enemy flees
- `test_battle_rewards_gold` - Verify gold is rewarded on victory
- `test_battle_no_gold_on_flee` - No gold when enemy flees

### Inn Tests
- `test_inn_rest_success` - Rest with enough gold
- `test_inn_rest_insufficient_gold` - Try to rest without enough gold

## Error Handling

**Insufficient Gold:**
- Model's `spend_gold` method: Return unchanged instance or raise ValueError
- Main loop: Check gold before spending, show user-friendly message

**Enemy Flee:**
- Battle loop: Break immediately, return special result
- Main loop: Display "Enemy fled!" message, no rewards

## Implementation Order

1. Update PlayerModel (gold field, spend/gain methods)
2. Update EnemyModel (gold_reward field)
3. Update EnemyData (add gold rewards)
4. Update enemy_turn (add wait and flee actions)
5. Update battle loop (handle flee, add status display, return gold)
6. Update main.py (inn cost, gold display, battle result handling)
7. Add tests for all new functionality

## Future Enhancements (Out of Scope)

- Shop system to buy items
- Different inn prices based on location
- Enemy gold reward variance (random bonus)
- Steal action for player
- More enemy actions (heal, buff, etc.)
