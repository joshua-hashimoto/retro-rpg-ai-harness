"""Battle system functions for the RPG game."""

import random
from collections.abc import Callable
from typing import TypeVar

from app.models.character_model import CharacterModel
from app.models.enemy_model import EnemyModel
from app.models.player_model import PlayerModel

ENEMY_ATTACK_THRESHOLD = 0.6
ENEMY_WAIT_THRESHOLD = 0.9

_D = TypeVar("_D", bound=CharacterModel)


def calculate_damage(attacker: CharacterModel, defender: CharacterModel) -> int:
    """Calculate damage dealt from attacker to defender (minimum 1)."""
    return max(1, attacker.attack - defender.defense)


def execute_attack(
    attacker: CharacterModel,
    defender: _D,
) -> tuple[_D, int]:
    """Execute an attack and return the updated defender with damage dealt."""
    damage = calculate_damage(attacker, defender)
    new_defender = defender.take_damage(damage)
    return (new_defender, damage)


def player_turn(
    player: PlayerModel,
    enemy: EnemyModel,
    action: str,
) -> tuple[PlayerModel, EnemyModel, str]:
    """Process the player's turn and return updated player, enemy, and log message."""
    if action == "attack":
        new_enemy, damage = execute_attack(player, enemy)
        if not new_enemy.alive:
            log = (
                f"{player.name} attacked {enemy.name} for {damage} damage! "
                f"{enemy.name} was defeated!"
            )
        else:
            log = (
                f"{player.name} attacked {enemy.name} for {damage} damage! "
                f"({enemy.name} HP: {new_enemy.hp}/{new_enemy.max_hp})"
            )
        return (player, new_enemy, log)
    if action == "flee":
        log = f"{player.name} fled from battle!"
        return (player, enemy, log)
    if action == "potion":
        if player.potions > 0:
            new_player = player.use_potion()
            log = (
                f"{player.name} used a potion and recovered HP! "
                f"({player.name} HP: {new_player.hp}/{new_player.max_hp})"
            )
            return (new_player, enemy, log)
        log = "You have no potions left!"
        return (player, enemy, log)
    return (player, enemy, "Invalid action")


def enemy_turn(enemy: EnemyModel, player: PlayerModel) -> tuple[PlayerModel, str, str]:
    """Process the enemy's turn.

    Return updated player, log message, and enemy action.
    Enemy action is one of: "attack", "wait", or "flee".
    """
    roll = random.random()

    if roll < ENEMY_ATTACK_THRESHOLD:
        new_player, damage = execute_attack(enemy, player)
        if not new_player.alive:
            log = (
                f"{enemy.name} attacked {player.name} for {damage} damage! "
                f"{player.name} was defeated!"
            )
        else:
            log = (
                f"{enemy.name} attacked {player.name} for {damage} damage! "
                f"({player.name} HP: {new_player.hp}/{new_player.max_hp})"
            )
        return (new_player, log, "attack")
    if roll < ENEMY_WAIT_THRESHOLD:
        log = f"{enemy.name} is resting..."
        return (player, log, "wait")
    log = f"{enemy.name} fled from battle!"
    return (player, log, "flee")


def show_enemy_status(enemy: EnemyModel) -> str:
    """Return a formatted string with the enemy's current status."""
    return f"""{enemy.name}
HP: {enemy.hp}/{enemy.max_hp}
Attack: {enemy.attack}
Defense: {enemy.defense}"""


def _execute_turn(
    player: PlayerModel,
    enemy: EnemyModel,
    action: str,
    on_log: Callable[[str], None] | None,
) -> tuple[PlayerModel, EnemyModel, str | None]:
    """Execute one full round (player then enemy); return a status string or None to continue."""
    player, enemy, log = player_turn(player, enemy, action)
    if on_log:
        on_log(log)
    if action == "flee":
        return player, enemy, "player_fled"
    if not enemy.alive:
        return player, enemy, "enemy_dead"
    player, log, enemy_action = enemy_turn(enemy, player)
    if on_log:
        on_log(log)
    if enemy_action == "flee":
        return player, enemy, "enemy_fled"
    return player, enemy, None


def battle(
    player: PlayerModel,
    enemy: EnemyModel,
    player_action_provider: Callable[[PlayerModel, EnemyModel], str] | None = None,
    on_log: Callable[[str], None] | None = None,
) -> tuple[PlayerModel, bool, str, int, int]:
    """Run the main battle loop.

    Return (updated_player, victory, result_message, exp_gained, gold_gained).
    If enemy or player fled: exp_gained=0, gold_gained=0, victory=True (battle ended safely).
    """
    current_player = player
    current_enemy = enemy
    status = None

    while current_player.alive and current_enemy.alive and status is None:
        action = (
            player_action_provider(current_player, current_enemy)
            if player_action_provider
            else "attack"
        )
        current_player, current_enemy, status = _execute_turn(
            current_player, current_enemy, action, on_log
        )

    if status == "player_fled":
        return (current_player, True, f"{player.name} fled from battle!", 0, 0)
    if status == "enemy_fled":
        return (current_player, True, f"{enemy.name} fled from battle!", 0, 0)
    if current_player.alive:
        return (
            current_player,
            True,
            f"Victory! {current_player.name} defeated {enemy.name}!",
            enemy.exp_reward,
            enemy.gold_reward,
        )
    return (
        current_player,
        False,
        f"Defeat! {current_player.name} was defeated by {enemy.name}.",
        0,
        0,
    )
