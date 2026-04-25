from app.models.enemy_model import EnemyModel


def test_enemy_initialization():
    enemy = EnemyModel(
        name="Slime", max_hp=10, hp=10, attack=3, defense=0, exp_reward=5, is_boss=False
    )
    assert enemy.name == "Slime"
    assert enemy.exp_reward == 5
    assert enemy.is_boss is False
    assert enemy.alive is True


def test_boss_enemy():
    boss = EnemyModel(
        name="Dragon", max_hp=100, hp=100, attack=15, defense=5, exp_reward=100, is_boss=True
    )
    assert boss.is_boss is True
    assert boss.exp_reward == 100
