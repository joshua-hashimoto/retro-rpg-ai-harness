from app.models.player_model import PlayerModel


def test_player_initialization():
    player = PlayerModel(name="Hero")
    assert player.name == "Hero"
    assert player.max_hp == 30
    assert player.hp == 30
    assert player.attack == 5
    assert player.defense == 1
    assert player.level == 1
    assert player.exp == 0
    assert player.next_exp == 10
    assert player.potions == 3
    assert player.alive is True


def test_use_potion_reduces_count():
    player = PlayerModel(name="Hero", potions=3, hp=10, max_hp=30)
    new_player = player.use_potion()
    assert new_player.potions == 2
    assert new_player.hp == 30  # Healed to full


def test_use_potion_no_potions():
    player = PlayerModel(name="Hero", potions=0, hp=10, max_hp=30)
    new_player = player.use_potion()
    assert new_player.potions == 0
    assert new_player.hp == 10  # No change


def test_add_potion():
    player = PlayerModel(name="Hero", potions=1)
    new_player = player.add_potion(2)
    assert new_player.potions == 3


def test_gain_exp_basic():
    player = PlayerModel(name="Hero", level=1, exp=0, next_exp=10)
    new_player, leveled_up = player.gain_exp(5)
    assert new_player.exp == 5
    assert leveled_up is False


def test_gain_exp_levels_up():
    player = PlayerModel(name="Hero", level=1, exp=0, next_exp=10)
    new_player, leveled_up = player.gain_exp(10)
    assert new_player.level == 2
    assert new_player.exp == 0
    assert new_player.max_hp == 35
    assert new_player.attack == 7
    assert new_player.defense == 2
    assert new_player.next_exp == 15
    assert new_player.hp == 35  # Full heal
    assert leveled_up is True


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

