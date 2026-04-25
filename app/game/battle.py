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


def enemy_turn(enemy: EnemyModel, player: PlayerModel) -> tuple[PlayerModel, str]:
    new_player, damage = execute_attack(enemy, player)
    log = f"{enemy.name} attacked {player.name} for {damage} damage!"
    return (new_player, log)
