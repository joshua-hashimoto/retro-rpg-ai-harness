import random
from typing import Callable, Optional

from app.models.character_model import CharacterModel
from app.models.player_model import PlayerModel
from app.models.enemy_model import EnemyModel


def calculate_damage(attacker: CharacterModel, defender: CharacterModel) -> int:
    return max(1, attacker.attack - defender.defense)


def execute_attack(
    attacker: CharacterModel, defender: CharacterModel
) -> tuple[CharacterModel, int]:
    damage = calculate_damage(attacker, defender)
    new_defender = defender.take_damage(damage)
    return (new_defender, damage)


def player_turn(
    player: PlayerModel, enemy: EnemyModel, action: str
) -> tuple[PlayerModel, EnemyModel, str]:
    if action == "attack":
        new_enemy, damage = execute_attack(player, enemy)
        log = f"{player.name} attacked {enemy.name} for {damage} damage!"
        return (player, new_enemy, log)
    elif action == "potion":
        if player.potions > 0:
            new_player = player.use_potion()
            log = f"{player.name} used a potion and recovered HP!"
            return (new_player, enemy, log)
        else:
            log = "You have no potions left!"
            return (player, enemy, log)
    else:
        return (player, enemy, "Invalid action")


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


def show_enemy_status(enemy: EnemyModel) -> str:
    return f"""{enemy.name}
HP: {enemy.hp}/{enemy.max_hp}
Attack: {enemy.attack}
Defense: {enemy.defense}"""


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

        current_player, current_enemy, log = player_turn(current_player, current_enemy, action)
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
        result_msg = f"Victory! {current_player.name} defeated {enemy.name}!\n" + "\n".join(
            logs[-3:]
        )
        return (current_player, True, result_msg, enemy.exp_reward, enemy.gold_reward)
    else:
        result_msg = f"Defeat! {current_player.name} was defeated by {enemy.name}.\n" + "\n".join(
            logs[-3:]
        )
        return (current_player, False, result_msg, 0, 0)
