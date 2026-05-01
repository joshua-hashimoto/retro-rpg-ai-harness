"""Entry point for the Simple RPG game."""

from app.game.battle import battle
from app.game.exp import gain_exp_and_check_level_up
from app.game.tui import (
    BOSS_UNLOCK_DEFEATS,
    BOSS_UNLOCK_LEVEL,
    get_battle_action,
    get_user_choice,
    show_battle_turn,
    show_boss_appears,
    show_boss_not_ready,
    show_complete_battle_result,
    show_enemy_appears,
    show_game_over,
    show_inn_rest,
    show_main_menu,
    show_thanks,
    show_title,
    show_welcome,
)
from app.models.enemy_data import BOSS_ENEMY, get_random_enemy
from app.models.player_model import PlayerModel


def fight_enemy(player: PlayerModel, defeated_count: int) -> tuple[PlayerModel, int, bool]:
    """Fight a random enemy.

    Args:
        player: The current player state.
        defeated_count: Number of enemies defeated so far.

    Returns:
        A tuple of (updated_player, updated_defeated_count, game_over).

    """
    enemy = get_random_enemy()
    show_enemy_appears(enemy)

    player, victory, msg, exp, gold = battle(
        player,
        enemy,
        player_action_provider=get_battle_action,
        on_log=show_battle_turn,
    )
    if not victory:
        show_complete_battle_result(msg, victory)
        return player, defeated_count, True
    level_up_message = None
    if exp > 0:
        defeated_count += 1
        player, leveled_up = gain_exp_and_check_level_up(player, exp)
        player = player.gain_gold(gold)
        if leveled_up:
            level_up_message = f"[bold green]*** LEVEL UP! You are now level {player.level}. ***"
    show_complete_battle_result(msg, victory, exp, gold, level_up_message)
    return player, defeated_count, False


def challenge_boss(player: PlayerModel, defeated_count: int) -> tuple[PlayerModel, bool]:
    """Challenge the boss.

    Args:
        player: The current player state.
        defeated_count: Number of enemies defeated so far.

    Returns:
        A tuple of (updated_player, game_over).

    """
    if not (defeated_count >= BOSS_UNLOCK_DEFEATS or player.level >= BOSS_UNLOCK_LEVEL):
        show_boss_not_ready()
        return player, False

    boss = BOSS_ENEMY.model_copy()
    show_boss_appears(boss)

    player, victory, msg, exp, gold = battle(
        player,
        boss,
        player_action_provider=get_battle_action,
        on_log=show_battle_turn,
    )
    if not victory:
        show_complete_battle_result(msg, victory)
        return player, True
    if victory and exp > 0:
        victory_message = (
            "[bold green]*** CONGRATULATIONS! You defeated the boss "
            "and saved the world! ***[/bold green]"
        )
        show_complete_battle_result(msg, victory, exp, gold, victory_message)
        return player, True
    return player, False


def rest_at_inn(player: PlayerModel) -> PlayerModel:
    """Rest at the inn to restore HP.

    Args:
        player: The current player state.

        The updated player with full HP.

    """
    player = player.heal_full()
    show_inn_rest()
    return player


def main() -> None:
    """Run the main game loop."""
    show_title()
    name = input("Enter your name: ").strip() or "Hero"
    player = PlayerModel(name=name)
    defeated_count = 0
    game_over = False

    show_welcome(player.name)
    print("🎮 Random debug print: Game initialized!")

    while not game_over:
        show_main_menu(player, defeated_count)
        choice = get_user_choice()

        if choice == "1":
            player, defeated_count, game_over = fight_enemy(player, defeated_count)
        elif choice == "2":
            player = rest_at_inn(player)
        elif choice == "3":
            player, game_over = challenge_boss(player, defeated_count)
        elif choice == "0":
            show_thanks()
            game_over = True

    if not player.alive:
        show_game_over()


if __name__ == "__main__":
    main()
