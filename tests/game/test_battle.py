from app.models.player_model import PlayerModel
from app.models.enemy_model import EnemyModel
from app.game.battle import calculate_damage, execute_attack, player_turn, enemy_turn


def test_calculate_damage_simple():
    attacker = PlayerModel(name="Hero", attack=5)
    defender = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, is_boss=False
    )
    damage = calculate_damage(attacker, defender)
    assert damage == 5


def test_calculate_damage_with_defense():
    attacker = PlayerModel(name="Hero", attack=5)
    defender = EnemyModel(
        name="Knight", max_hp=20, hp=20, attack=3, defense=3, exp_reward=10, is_boss=False
    )
    damage = calculate_damage(attacker, defender)
    assert damage == 2


def test_calculate_damage_minimum_1():
    attacker = PlayerModel(name="Hero", attack=5)
    defender = EnemyModel(
        name="Tank", max_hp=50, hp=50, attack=10, defense=10, exp_reward=20, is_boss=False
    )
    damage = calculate_damage(attacker, defender)
    assert damage == 1


def test_execute_attack():
    attacker = PlayerModel(name="Hero", attack=5)
    defender = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, is_boss=False
    )
    new_defender, damage = execute_attack(attacker, defender)
    assert new_defender.hp == 5
    assert damage == 5


def test_player_turn_attack():
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30)
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, is_boss=False
    )
    new_player, new_enemy, log = player_turn(player, enemy, "attack")
    assert new_player == player
    assert new_enemy.hp == 5
    assert "attacked" in log.lower()


def test_player_turn_potion():
    player = PlayerModel(name="Hero", attack=5, hp=10, max_hp=30, potions=3)
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, is_boss=False
    )
    new_player, new_enemy, log = player_turn(player, enemy, "potion")
    assert new_player.hp == 30
    assert new_player.potions == 2
    assert new_enemy == enemy
    assert "potion" in log.lower()


def test_player_turn_potion_no_potions():
    player = PlayerModel(name="Hero", attack=5, hp=10, max_hp=30, potions=0)
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, is_boss=False
    )
    new_player, new_enemy, log = player_turn(player, enemy, "potion")
    assert new_player.hp == 10
    assert new_player.potions == 0
    assert "no potions" in log.lower()


def test_enemy_turn():
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, is_boss=False
    )
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30, defense=1)
    new_player, log = enemy_turn(enemy, player)
    assert new_player.hp == 28
    assert "attacked" in log.lower()
