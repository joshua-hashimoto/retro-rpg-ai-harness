from app.models.player_model import PlayerModel
from app.models.enemy_model import EnemyModel
from app.game.battle import calculate_damage, execute_attack


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
