"""Predefined enemy instances and random enemy selection."""

import random

from app.models.enemy_model import EnemyModel

REGULAR_ENEMIES = [
    EnemyModel(
        name="Slime",
        max_hp=10,
        hp=10,
        attack=3,
        defense=0,
        exp_reward=5,
        gold_reward=5,
        is_boss=False,
    ),
    EnemyModel(
        name="Goblin",
        max_hp=15,
        hp=15,
        attack=4,
        defense=1,
        exp_reward=8,
        gold_reward=7,
        is_boss=False,
    ),
    EnemyModel(
        name="Rat",
        max_hp=8,
        hp=8,
        attack=2,
        defense=0,
        exp_reward=3,
        gold_reward=4,
        is_boss=False,
    ),
    EnemyModel(
        name="Skeleton",
        max_hp=12,
        hp=12,
        attack=5,
        defense=1,
        exp_reward=10,
        gold_reward=6,
        is_boss=False,
    ),
    EnemyModel(
        name="Bat",
        max_hp=6,
        hp=6,
        attack=3,
        defense=0,
        exp_reward=4,
        gold_reward=3,
        is_boss=False,
    ),
    EnemyModel(
        name="Wolf",
        max_hp=18,
        hp=18,
        attack=6,
        defense=2,
        exp_reward=12,
        gold_reward=9,
        is_boss=False,
    ),
    EnemyModel(
        name="Orc",
        max_hp=25,
        hp=25,
        attack=7,
        defense=2,
        exp_reward=15,
        gold_reward=12,
        is_boss=False,
    ),
    EnemyModel(
        name="Ghost",
        max_hp=14,
        hp=14,
        attack=8,
        defense=0,
        exp_reward=14,
        gold_reward=7,
        is_boss=False,
    ),
]

BOSS_ENEMY = EnemyModel(
    name="Dragon",
    max_hp=100,
    hp=100,
    attack=15,
    defense=5,
    exp_reward=100,
    gold_reward=250,
    is_boss=True,
)


def get_random_enemy() -> EnemyModel:
    """Return a random copy of a regular enemy."""
    return random.choice(REGULAR_ENEMIES).model_copy()
