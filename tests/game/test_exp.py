from app.models.player_model import PlayerModel
from app.game.exp import gain_exp_and_check_level_up


def test_gain_exp_no_level_up():
    player = PlayerModel(name="Hero", exp=0, next_exp=10)
    new_player, leveled_up = gain_exp_and_check_level_up(player, 5)
    assert new_player.exp == 5
    assert leveled_up is False


def test_gain_exp_level_up():
    player = PlayerModel(name="Hero", exp=5, next_exp=10)
    new_player, leveled_up = gain_exp_and_check_level_up(player, 5)
    assert new_player.level == 2
    assert new_player.exp == 0
    assert leveled_up is True


def test_gain_exp_multiple_level_ups():
    player = PlayerModel(name="Hero", exp=9, next_exp=10)
    new_player, leveled_up = gain_exp_and_check_level_up(player, 20)
    assert new_player.level >= 3
    assert leveled_up is True
