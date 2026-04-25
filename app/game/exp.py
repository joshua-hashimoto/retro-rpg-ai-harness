from app.models.player_model import PlayerModel


def gain_exp_and_check_level_up(player: PlayerModel, exp: int) -> tuple[PlayerModel, bool]:
    return player.gain_exp(exp)
