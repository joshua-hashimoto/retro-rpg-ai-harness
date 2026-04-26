"""Entry point for the Simple RPG game."""
from app.game.battle import battle
from app.game.exp import gain_exp_and_check_level_up
from app.models.enemy_data import BOSS_ENEMY, get_random_enemy
from app.models.player_model import PlayerModel

BOSS_UNLOCK_DEFEATS = 5
BOSS_UNLOCK_LEVEL = 3


def show_main_menu(player: PlayerModel, defeated_count: int) -> None:
    """Display the main action menu.

    Args:
        player: The current player state.
        defeated_count: Number of enemies defeated so far.

    """
    print("\n==== MAIN MENU ====")
    print(
        f"Defeated: {defeated_count} | Level: {player.level} | "
        f"Gold: {player.gold}G | Potions: {player.potions}",
    )
    print(f"HP: {player.hp}/{player.max_hp} | EXP: {player.exp}/{player.next_exp}")
    print("1) Fight Enemy")
    print("2) Rest at Inn (Full HP) - 10G")
    if defeated_count >= BOSS_UNLOCK_DEFEATS or player.level >= BOSS_UNLOCK_LEVEL:
        print("3) Challenge Boss")
    print("q) Quit")


def get_user_choice() -> str:
    """Prompt the user and return a valid menu choice."""
    while True:
        choice = input("> ").strip().lower()
        if choice in ["1", "2", "3", "q"]:
            return choice
        print("Invalid choice. Please try again.")


def choose_action_in_battle(player: PlayerModel) -> str:
    """Prompt the player to choose a battle action and return it."""
    while True:
        print("\n1) Attack")
        if player.potions > 0:
            print("2) Use Potion")
        choice = input("Action: ").strip()
        if choice == "1":
            return "attack"
        if choice == "2" and player.potions > 0:
            return "potion"
        print("Invalid action.")


def _fight_enemy(
    player: PlayerModel, defeated_count: int
) -> tuple[PlayerModel, int, bool]:
    enemy = get_random_enemy()
    print(f"\nA wild {enemy.name} appears!")
    print(f"Enemy Stats: HP {enemy.hp}, ATK {enemy.attack}, DEF {enemy.defense}")
    player, victory, msg, exp, gold = battle(
        player, enemy, lambda p, _e: choose_action_in_battle(p)
    )
    print(msg)
    if not victory:
        return player, defeated_count, True
    defeated_count += 1
    player, leveled_up = gain_exp_and_check_level_up(player, exp)
    player = player.gain_gold(gold)
    if leveled_up:
        print(f"\n*** LEVEL UP! You are now level {player.level}. ***")
    return player, defeated_count, False


def _challenge_boss(
    player: PlayerModel, defeated_count: int
) -> tuple[PlayerModel, bool]:
    if not (defeated_count >= BOSS_UNLOCK_DEFEATS or player.level >= BOSS_UNLOCK_LEVEL):
        print("\nYou are not ready yet. Defeat 5 enemies or reach level 3.")
        return player, False
    print("\n=== BOSS BATTLE ===")
    boss = BOSS_ENEMY.model_copy()
    print(f"The mighty {boss.name} appears!")
    print(f"Boss Stats: HP {boss.hp}, ATK {boss.attack}, DEF {boss.defense}")
    player, victory, msg, _, _ = battle(
        player, boss, lambda p, _e: choose_action_in_battle(p)
    )
    print(msg)
    if victory:
        print("\n*** CONGRATULATIONS! You defeated the boss and saved the world! ***")
    return player, True


def main() -> None:
    """Run the main game loop."""
    print("==== SIMPLE RPG ====")
    name = input("Enter your name: ").strip() or "Hero"
    player = PlayerModel(name=name)
    defeated_count = 0
    game_over = False

    print(f"\nWelcome, {player.name}! Defeat enemies to level up, then challenge the boss.\n")

    while not game_over:
        show_main_menu(player, defeated_count)
        choice = get_user_choice()

        if choice == "1":
            player, defeated_count, game_over = _fight_enemy(player, defeated_count)
        elif choice == "2":
            player = player.heal_full()
            print("\nYou rested at the inn. HP fully restored!\n")
        elif choice == "3":
            player, game_over = _challenge_boss(player, defeated_count)
        elif choice == "q":
            print("\nThanks for playing!")
            game_over = True

    if not player.alive:
        print("\nGAME OVER")


if __name__ == "__main__":
    main()
