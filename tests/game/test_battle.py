from unittest.mock import patch

from app.game.battle import (
    battle,
    calculate_damage,
    enemy_turn,
    execute_attack,
    player_turn,
)
from app.models.enemy_model import EnemyModel
from app.models.player_model import PlayerModel


def test_calculate_damage_simple():
    attacker = PlayerModel(name="Hero", attack=5)
    defender = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    damage = calculate_damage(attacker, defender)
    assert damage == 5


def test_calculate_damage_with_defense():
    attacker = PlayerModel(name="Hero", attack=5)
    defender = EnemyModel(
        name="Knight",
        max_hp=20,
        hp=20,
        attack=3,
        defense=3,
        exp_reward=10,
        gold_reward=10,
        is_boss=False,
    )
    damage = calculate_damage(attacker, defender)
    assert damage == 2


def test_calculate_damage_minimum_1():
    attacker = PlayerModel(name="Hero", attack=5)
    defender = EnemyModel(
        name="Tank",
        max_hp=50,
        hp=50,
        attack=10,
        defense=10,
        exp_reward=20,
        gold_reward=25,
        is_boss=False,
    )
    damage = calculate_damage(attacker, defender)
    assert damage == 1


def test_execute_attack():
    attacker = PlayerModel(name="Hero", attack=5)
    defender = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    new_defender, damage = execute_attack(attacker, defender)
    assert new_defender.hp == 5
    assert damage == 5


def test_player_turn_attack():
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30)
    enemy = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    new_player, new_enemy, log = player_turn(player, enemy, "attack")
    assert new_player == player
    assert new_enemy.hp == 5
    assert "attacked" in log.lower()


def test_player_turn_potion():
    player = PlayerModel(name="Hero", attack=5, hp=10, max_hp=30, potions=3)
    enemy = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    new_player, new_enemy, log = player_turn(player, enemy, "potion")
    assert new_player.hp == 30
    assert new_player.potions == 2
    assert new_enemy == enemy
    assert "potion" in log.lower()


def test_player_turn_potion_no_potions():
    player = PlayerModel(name="Hero", attack=5, hp=10, max_hp=30, potions=0)
    enemy = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    new_player, new_enemy, log = player_turn(player, enemy, "potion")
    assert new_player.hp == 10
    assert new_player.potions == 0
    assert "no potions" in log.lower()


def test_enemy_turn():
    enemy = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30, defense=1)

    with patch("random.random", return_value=0.3):
        new_player, log, action = enemy_turn(enemy, player)

    assert new_player.hp == 28
    assert "attacked" in log.lower()
    assert action == "attack"


def test_enemy_wait_action():
    enemy = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30, defense=1)

    with patch("random.random", return_value=0.7):
        new_player, log, action = enemy_turn(enemy, player)

    assert action == "wait"
    assert new_player == player
    assert "resting" in log.lower()


def test_enemy_flee_action():
    enemy = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30, defense=1)

    with patch("random.random", return_value=0.95):
        new_player, log, action = enemy_turn(enemy, player)

    assert action == "flee"
    assert new_player == player
    assert "fled" in log.lower()


def test_battle_player_wins():
    player = PlayerModel(name="Hero", attack=20, hp=30, max_hp=30)
    enemy = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )
    new_player, victory, msg, exp, gold = battle(
        player, enemy, player_action_provider=lambda p, e: "attack",
    )
    assert victory is True
    assert new_player.alive is True
    assert exp == 5
    assert gold == 5


def test_battle_enemy_wins():
    player = PlayerModel(name="Weak", attack=1, hp=10, max_hp=10, defense=0)
    enemy = EnemyModel(
        name="Strong",
        max_hp=100,
        hp=100,
        attack=10,
        defense=0,
        exp_reward=50,
        gold_reward=50,
        is_boss=False,
    )
    new_player, victory, msg, exp, gold = battle(
        player, enemy, player_action_provider=lambda p, e: "attack",
    )
    assert victory is False
    assert not new_player.alive
    assert exp == 0
    assert gold == 0


def test_battle_with_flee():
    player = PlayerModel(name="Hero", attack=5, hp=30, max_hp=30)
    enemy = EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
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
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    )

    def action_provider(p, e):
        return "attack"

    new_player, victory, msg, exp, gold = battle(player, enemy, action_provider)

    assert victory is True
    assert exp == 5
    assert gold == 5
