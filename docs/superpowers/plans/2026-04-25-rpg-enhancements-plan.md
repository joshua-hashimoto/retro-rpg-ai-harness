# RPG Enhancements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add gold system, enemy AI with multiple actions, status display, and inn cost to the existing RPG.

**Architecture:** Model-centered approach extending existing immutable Pydantic models, updating battle logic with enemy AI, and enhancing main game loop for gold and inn features.

**Tech Stack:** Python 3.13, Pydantic 2.13.3, pytest, ruff.

---

## File Structure

**Files to Modify:**
- `app/models/player_model.py` - Add gold field and spend/gain methods
- `app/models/enemy_model.py` - Add gold_reward field
- `app/models/enemy_data.py` - Add gold_reward to enemy definitions
- `app/game/battle.py` - Update enemy_turn, battle loop, add status display
- `main.py` - Add gold display, inn cost logic, battle result handling

**New Test Files:**
- `tests/models/test_player_gold.py` - Player gold system tests
- `tests/models/test_enemy_gold.py` - Enemy gold reward tests
- `tests/game/test_enemy_ai.py` - Enemy AI action tests
- `tests/game/test_battle_enhancements.py` - Battle enhancements tests

**Existing Test Files to Update:**
- `tests/models/test_player_model.py` - Add gold-related tests
- `tests/models/test_enemy_model.py` - Add gold_reward tests
- `tests/game/test_battle.py` - Update for new battle signature

---

## Task 1: PlayerModel Gold System

**Files:**
- Modify: `app/models/player_model.py`
- Test: `tests/models/test_player_model.py`

- [ ] **Step 1: Write failing tests for gold system**

Add to `tests/models/test_player_model.py`:

```python
def test_player_initial_gold():
    player = PlayerModel(name="Hero")
    assert player.gold == 10

def test_spend_gold_success():
    player = PlayerModel(name="Hero", gold=20)
    new_player = player.spend_gold(10)
    assert new_player.gold == 10
    assert player.gold == 20  # Original unchanged

def test_spend_gold_insufficient():
    player = PlayerModel(name="Hero", gold=5)
    new_player = player.spend_gold(10)
    assert new_player.gold == 5  # Unchanged
    assert new_player == player

def test_gain_gold():
    player = PlayerModel(name="Hero", gold=10)
    new_player = player.gain_gold(15)
    assert new_player.gold == 25
    assert player.gold == 10  # Original unchanged
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/models/test_player_model.py -v`
Expected: FAIL (AttributeError: 'PlayerModel' object has no attribute 'gold')

- [ ] **Step 3: Implement gold system in PlayerModel**

Modify `app/models/player_model.py`:

```python
from app.models.character_model import CharacterModel


class PlayerModel(CharacterModel):
    level: int = 1
    exp: int = 0
    next_exp: int = 10
    potions: int = 3
    gold: int = 10  # NEW: Starting gold

    def __init__(self, **data):
        if "max_hp" not in data:
            data["max_hp"] = 30
        if "hp" not in data:
            data["hp"] = data["max_hp"]
        if "attack" not in data:
            data["attack"] = 5
        if "defense" not in data:
            data["defense"] = 1
        if "gold" not in data:
            data["gold"] = 10
        super().__init__(**data)

    def use_potion(self) -> "PlayerModel":
        if self.potions > 0:
            return self.model_copy(update={"potions": self.potions - 1, "hp": self.max_hp})
        return self

    def add_potion(self, amount: int) -> "PlayerModel":
        return self.model_copy(update={"potions": self.potions + amount})

    def gain_exp(self, amount: int) -> tuple["PlayerModel", bool]:
        current_exp = self.exp + amount
        current_level = self.level
        current_next_exp = self.next_exp
        current_max_hp = self.max_hp
        current_attack = self.attack
        current_defense = self.defense

        leveled_up = False
        while current_exp >= current_next_exp:
            leveled_up = True
            current_exp -= current_next_exp
            current_level += 1
            current_next_exp = int(current_next_exp * 1.5)
            current_max_hp += 5
            current_attack += 2
            current_defense += 1

        updates = {
            "exp": current_exp,
            "next_exp": current_next_exp,
            "level": current_level,
            "max_hp": current_max_hp,
            "attack": current_attack,
            "defense": current_defense,
        }

        if leveled_up:
            updates["hp"] = current_max_hp

        return self.model_copy(update=updates), leveled_up

    # NEW METHODS
    def spend_gold(self, amount: int) -> "PlayerModel":
        if self.gold >= amount:
            return self.model_copy(update={"gold": self.gold - amount})
        return self

    def gain_gold(self, amount: int) -> "PlayerModel":
        return self.model_copy(update={"gold": self.gold + amount})
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/models/test_player_model.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/models/player_model.py tests/models/test_player_model.py
git commit -m "feat: add gold system to PlayerModel"
```

---

## Task 2: EnemyModel Gold Reward

**Files:**
- Modify: `app/models/enemy_model.py`
- Test: `tests/models/test_enemy_model.py`

- [ ] **Step 1: Write failing tests for gold reward**

Add to `tests/models/test_enemy_model.py`:

```python
def test_enemy_gold_reward():
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False
    )
    assert enemy.gold_reward == 5

def test_boss_gold_reward():
    boss = EnemyModel(
        name="Dragon", max_hp=100, hp=100, attack=15, defense=5, exp_reward=100, gold_reward=250, is_boss=True
    )
    assert boss.gold_reward == 250
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/models/test_enemy_model.py -v`
Expected: FAIL (unexpected keyword argument 'gold_reward')

- [ ] **Step 3: Implement gold_reward in EnemyModel**

Modify `app/models/enemy_model.py`:

```python
from pydantic import Field
from app.models.character_model import CharacterModel


class EnemyModel(CharacterModel):
    exp_reward: int = Field(ge=0)
    gold_reward: int = Field(ge=0)  # NEW
    is_boss: bool = False
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/models/test_enemy_model.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/models/enemy_model.py tests/models/test_enemy_model.py
git commit -m "feat: add gold_reward to EnemyModel"
```

---

## Task 3: Update EnemyData with Gold Rewards

**Files:**
- Modify: `app/models/enemy_data.py`

- [ ] **Step 1: Calculate gold rewards for each enemy**

Formula: `int(max_hp * 0.5)` for regular enemies, `int(max_hp * 2.5)` for boss.

- [ ] **Step 2: Update EnemyData**

Modify `app/models/enemy_data.py`:

```python
import random
from app.models.enemy_model import EnemyModel

# Define 5-10 regular enemies with gold rewards
REGULAR_ENEMIES = [
    EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False
    ),  # 10 * 0.5 = 5
    EnemyModel(
        name="Goblin", max_hp=15, hp=15, attack=4, defense=1, exp_reward=8, gold_reward=7, is_boss=False
    ),  # 15 * 0.5 = 7.5 -> 7
    EnemyModel(
        name="Rat", max_hp=8, hp=8, attack=2, defense=0, exp_reward=3, gold_reward=4, is_boss=False
    ),  # 8 * 0.5 = 4
    EnemyModel(
        name="Skeleton", max_hp=12, hp=12, attack=5, defense=1, exp_reward=10, gold_reward=6, is_boss=False
    ),  # 12 * 0.5 = 6
    EnemyModel(
        name="Bat", max_hp=6, hp=6, attack=3, defense=0, exp_reward=4, gold_reward=3, is_boss=False
    ),  # 6 * 0.5 = 3
    EnemyModel(
        name="Wolf", max_hp=18, hp=18, attack=6, defense=2, exp_reward=12, gold_reward=9, is_boss=False
    ),  # 18 * 0.5 = 9
    EnemyModel(
        name="Orc", max_hp=25, hp=25, attack=7, defense=2, exp_reward=15, gold_reward=12, is_boss=False
    ),  # 25 * 0.5 = 12.5 -> 12
    EnemyModel(
        name="Ghost", max_hp=14, hp=14, attack=8, defense=0, exp_reward=14, gold_reward=7, is_boss=False
    ),  # 14 * 0.5 = 7
]

# Define Boss with 5x gold reward
BOSS_ENEMY = EnemyModel(
    name="Dragon",
    max_hp=100,
    hp=100,
    attack=15,
    defense=5,
    exp_reward=100,
    gold_reward=250,
    is_boss=True,
)  # 100 * 2.5 = 250


def get_random_enemy() -> EnemyModel:
    return random.choice(REGULAR_ENEMIES).model_copy()
```

- [ ] **Step 3: Commit**

```bash
git add app/models/enemy_data.py
git commit -m "feat: add gold rewards to EnemyData"
```

---

## Task 4: Enemy AI with Multiple Actions

**Files:**
- Modify: `app/game/battle.py`
- Test: `tests/game/test_battle.py`

- [ ] **Step 1: Write failing tests for enemy AI actions**

Add to `tests/game/test_battle.py`:

```python
import random
from unittest.mock import patch

def test_enemy_wait_action():
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False
    )
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30, defense=1)

    with patch("random.random", return_value=0.7):  # 0.6-0.9 = wait
        new_player, log, action = enemy_turn(enemy, player)

    assert action == "wait"
    assert new_player == player  # Player unchanged
    assert "resting" in log.lower()

def test_enemy_flee_action():
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False
    )
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30, defense=1)

    with patch("random.random", return_value=0.95):  # 0.9+ = flee
        new_player, log, action = enemy_turn(enemy, player)

    assert action == "flee"
    assert new_player == player  # Player unchanged
    assert "fled" in log.lower()
```

- [ ] **Step 2: Update existing enemy_turn test for new signature**

Modify existing `test_enemy_turn` in `tests/game/test_battle.py`:

```python
def test_enemy_turn():
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False
    )
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30, defense=1)

    with patch("random.random", return_value=0.3):  # 0-0.6 = attack
        new_player, log, action = enemy_turn(enemy, player)

    assert new_player.hp == 28
    assert "attacked" in log.lower()
    assert action == "attack"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/game/test_battle.py::test_enemy_wait_action -v`
Expected: FAIL (wrong number of values to unpack)

- [ ] **Step 4: Implement enemy AI in enemy_turn**

Modify `enemy_turn` in `app/game/battle.py`:

```python
def enemy_turn(enemy: EnemyModel, player: PlayerModel) -> tuple[PlayerModel, str, str]:
    """
    Returns: (updated_player, log_message, enemy_action)
    enemy_action: "attack", "wait", or "flee"
    """
    roll = random.random()

    if roll < 0.6:
        # Attack (60%)
        new_player, damage = execute_attack(enemy, player)
        log = f"{enemy.name} attacked {player.name} for {damage} damage!"
        return (new_player, log, "attack")
    elif roll < 0.9:
        # Wait (30%)
        log = f"{enemy.name} is resting..."
        return (player, log, "wait")
    else:
        # Flee (10%)
        log = f"{enemy.name} fled from battle!"
        return (player, log, "flee")
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/game/test_battle.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add app/game/battle.py tests/game/test_battle.py
git commit -m "feat: add enemy AI with attack, wait, flee actions"
```

---

## Task 5: Enemy Status Display

**Files:**
- Modify: `app/game/battle.py`

- [ ] **Step 1: Add status display function**

Add to `app/game/battle.py`:

```python
def show_enemy_status(enemy: EnemyModel) -> str:
    return f"""{enemy.name}
HP: {enemy.hp}/{enemy.max_hp}
Attack: {enemy.attack}
Defense: {enemy.defense}"""
```

- [ ] **Step 2: Commit**

```bash
git add app/game/battle.py
git commit -m "feat: add enemy status display function"
```

---

## Task 6: Battle Loop Enhancements

**Files:**
- Modify: `app/game/battle.py`
- Test: `tests/game/test_battle.py`

- [ ] **Step 1: Write failing tests for enhanced battle**

Add to `tests/game/test_battle.py`:

```python
def test_battle_with_flee():
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30)
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False
    )

    def action_provider(p, e):
        return "attack"

    # Mock enemy to always flee
    with patch("app.game.battle.enemy_turn") as mock_turn:
        mock_turn.return_value = (player, "Slime fled!", "flee")
        new_player, victory, msg, exp, gold = battle(player, enemy, action_provider)

    assert victory is True
    assert exp == 0
    assert gold == 0
    assert "fled" in msg.lower()

def test_battle_rewards_gold():
    player = PlayerModel(name="Hero", attack=20, hp=30, max_hp=30)
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False
    )

    def action_provider(p, e):
        return "attack"

    new_player, victory, msg, exp, gold = battle(player, enemy, action_provider)

    assert victory is True
    assert exp == 5
    assert gold == 5
```

- [ ] **Step 2: Update battle tests for new signature**

Modify `test_battle_player_wins` and `test_battle_enemy_wins` in `tests/game/test_battle.py`:

```python
def test_battle_player_wins():
    player = PlayerModel(name="Hero", attack=20, hp=30, max_hp=30)
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, gold_reward=5, is_boss=False
    )
    new_player, victory, msg, exp, gold = battle(
        player, enemy, player_action_provider=lambda p, e: "attack"
    )
    assert victory is True
    assert new_player.alive is True
    assert exp == 5
    assert gold == 5


def test_battle_enemy_wins():
    player = PlayerModel(name="Weak", attack=1, hp=10, max_hp=10, defense=0)
    enemy = EnemyModel(
        name="Strong", max_hp=100, hp=100, attack=10, defense=0, exp_reward=50, gold_reward=50, is_boss=False
    )
    new_player, victory, msg, exp, gold = battle(
        player, enemy, player_action_provider=lambda p, e: "attack"
    )
    assert victory is False
    assert not new_player.alive
    assert exp == 0
    assert gold == 0
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/game/test_battle.py::test_battle_player_wins -v`
Expected: FAIL (too many values to unpack)

- [ ] **Step 4: Update battle loop to handle flee and return rewards**

Modify `battle` function in `app/game/battle.py`:

```python
def battle(
    player: PlayerModel,
    enemy: EnemyModel,
    player_action_provider: Optional[Callable[[PlayerModel, EnemyModel], str]] = None,
) -> tuple[PlayerModel, bool, str, int, int]:
    """
    Main battle loop.
    Returns: (updated_player, victory, result_message, exp_gained, gold_gained)
    If enemy fled: exp_gained=0, gold_gained=0, victory=True (battle ended)
    """
    current_player = player
    current_enemy = enemy
    logs = []
    enemy_fled = False

    while current_player.alive and current_enemy.alive:
        if player_action_provider:
            action = player_action_provider(current_player, current_enemy)
        else:
            action = "attack"

        current_player, current_enemy, log = player_turn(
            current_player, current_enemy, action
        )
        logs.append(log)

        if not current_enemy.alive:
            break

        current_player, log, enemy_action = enemy_turn(current_enemy, current_player)
        logs.append(log)

        if enemy_action == "flee":
            enemy_fled = True
            break

    if enemy_fled:
        result_msg = f"{enemy.name} fled from battle!\n" + "\n".join(logs[-3:])
        return (current_player, True, result_msg, 0, 0)

    if current_player.alive:
        result_msg = (
            f"Victory! {current_player.name} defeated {enemy.name}!\n" + "\n".join(logs[-3:])
        )
        return (current_player, True, result_msg, enemy.exp_reward, enemy.gold_reward)
    else:
        result_msg = (
            f"Defeat! {current_player.name} was defeated by {enemy.name}.\n" + "\n".join(logs[-3:])
        )
        return (current_player, False, result_msg, 0, 0)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/game/test_battle.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add app/game/battle.py tests/game/test_battle.py
git commit -m "feat: update battle loop with flee handling and gold rewards"
```

---

## Task 7: Main Game Loop - Gold Display

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Update main menu to display gold**

Modify `show_main_menu` in `main.py`:

```python
def show_main_menu(player: PlayerModel, defeated_count: int):
    print("\n==== MAIN MENU ====")
    print(f"Defeated: {defeated_count} | Level: {player.level} | Gold: {player.gold}G | Potions: {player.potions}")
    print(f"HP: {player.hp}/{player.max_hp} | EXP: {player.exp}/{player.next_exp}")
    print("1) Fight Enemy")
    print("2) Rest at Inn (Full HP) - 10G")
    if defeated_count >= 5 or player.level >= 3:
        print("3) Challenge Boss")
    print("q) Quit")
```

- [ ] **Step 2: Commit**

```bash
git add main.py
git commit -m "feat: add gold display to main menu"
```

---

## Task 8: Main Game Loop - Inn Cost

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Update inn rest logic with cost**

Modify the `choice == "2"` section in `main.py`:

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

- [ ] **Step 2: Commit**

```bash
git add main.py
git commit -m "feat: add inn cost logic"
```

---

## Task 9: Main Game Loop - Battle Result Handling

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Update battle result handling to show gold**

Modify the `choice == "1"` section in `main.py`:

```python
        if choice == "1":
            enemy = get_random_enemy()
            print(f"\nA wild {enemy.name} appears!")
            print(f"Enemy Stats: HP {enemy.hp}, ATK {enemy.attack}, DEF {enemy.defense}")

            def action_provider(p, e):
                return choose_action_in_battle(p)

            player, victory, msg, exp_gained, gold_gained = battle(player, enemy, action_provider)
            print(msg)

            if victory:
                if exp_gained > 0 or gold_gained > 0:
                    defeated_count += 1
                    player, leveled_up = gain_exp_and_check_level_up(player, exp_gained)
                    player = player.gain_gold(gold_gained)
                    print(f"Gained {exp_gained} EXP and {gold_gained} gold!")
                    if leveled_up:
                        print(f"\n*** LEVEL UP! You are now level {player.level}. ***")
                else:
                    print("The enemy escaped! No rewards.")
            else:
                game_over = True
```

- [ ] **Step 2: Update boss battle result handling**

Modify the `choice == "3"` section in `main.py`:

```python
                player, victory, msg, exp_gained, gold_gained = battle(player, boss, action_provider)
                print(msg)

                if victory:
                    if exp_gained > 0 or gold_gained > 0:
                        player, leveled_up = gain_exp_and_check_level_up(player, exp_gained)
                        player = player.gain_gold(gold_gained)
                        print(f"Gained {exp_gained} EXP and {gold_gained} gold!")
                        if leveled_up:
                            print(f"\n*** LEVEL UP! You are now level {player.level}. ***")
                        print("\n*** CONGRATULATIONS! You defeated the boss and saved the world! ***")
                    game_over = True
                else:
                    game_over = True
```

- [ ] **Step 3: Commit**

```bash
git add main.py
git commit -m "feat: update battle result handling with gold rewards"
```

---

## Task 10: Add Status Display in Battle

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Add enemy status display in battle**

Update the action_provider function in `main.py` to show enemy status:

```python
            from app.game.battle import show_enemy_status

            def action_provider(p, e):
                print(f"\n--- {e.name}'s Turn ---")
                print(show_enemy_status(e))
                return choose_action_in_battle(p)
```

Also add after player action:
```python
            player, victory, msg, exp_gained, gold_gained = battle(player, enemy, action_provider)
            print(msg)

            # Show enemy status after player's action
            if enemy.alive:
                print(f"\n--- {enemy.name}'s Status ---")
                print(show_enemy_status(enemy))
```

- [ ] **Step 2: Commit**

```bash
git add main.py
git commit -m "feat: add enemy status display during battle"
```

---

## Final Verification

- [ ] **Step 1: Run full test suite**

Run: `pytest tests/ -v`

Expected: All tests pass.

- [ ] **Step 2: Run linting**

Run:
```bash
ruff check .
ruff format .
```

Fix any issues.

- [ ] **Step 3: Manual test**

Run: `uv run python main.py`

Test the following:
1. Verify gold is displayed in main menu
2. Fight enemy and check gold reward
3. Try to rest at inn without enough gold
4. Rest at inn with enough gold
5. Wait for enemy to rest
6. Wait for enemy to flee (may take several battles)
7. Defeat boss and get large gold reward

- [ ] **Step 4: Final commit if needed**

```bash
git add .
git commit -m "chore: final tweaks and verification"
```
