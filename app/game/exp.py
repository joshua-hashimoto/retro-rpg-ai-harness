"""Experience and level-up utility functions."""
from app.models.player_model import PlayerModel


def gain_exp_and_check_level_up(player: PlayerModel, exp: int) -> tuple[PlayerModel, bool]:
    """Apply exp to the player and return the updated player with a level-up flag."""
    return player.gain_exp(exp)
