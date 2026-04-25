from app.models.player_model import PlayerModel
from app.models.enemy_data import get_random_enemy, BOSS_ENEMY
from app.game.battle import battle
from app.game.exp import gain_exp_and_check_level_up


def show_main_menu(player: PlayerModel, defeated_count: int):
    print("\n==== MAIN MENU ====")
    print(f"Defeated: {defeated_count} | Level: {player.level} | Potions: {player.potions}")
    print(f"HP: {player.hp}/{player.max_hp} | EXP: {player.exp}/{player.next_exp}")
    print("1) Fight Enemy")
    print("2) Rest at Inn (Full HP)")
    if defeated_count >= 5 or player.level >= 3:
        print("3) Challenge Boss")
    print("q) Quit")


def get_user_choice():
    while True:
        choice = input("> ").strip().lower()
        if choice in ["1", "2", "3", "q"]:
            return choice
        print("Invalid choice. Please try again.")


def choose_action_in_battle(player: PlayerModel):
    while True:
        print("\n1) Attack")
        if player.potions > 0:
            print("2) Use Potion")
        choice = input("Action: ").strip()
        if choice == "1":
            return "attack"
        elif choice == "2" and player.potions > 0:
            return "potion"
        print("Invalid action.")


def main():
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
            enemy = get_random_enemy()
            print(f"\nA wild {enemy.name} appears!")
            print(f"Enemy Stats: HP {enemy.hp}, ATK {enemy.attack}, DEF {enemy.defense}")

            def action_provider(p, e):
                return choose_action_in_battle(p)

            player, victory, msg = battle(player, enemy, action_provider)
            print(msg)

            if victory:
                defeated_count += 1
                player, leveled_up = gain_exp_and_check_level_up(player, enemy.exp_reward)
                if leveled_up:
                    print(f"\n*** LEVEL UP! You are now level {player.level}. ***")
            else:
                game_over = True

        elif choice == "2":
            player = player.heal_full()
            print("\nYou rested at the inn. HP fully restored!\n")

        elif choice == "3":
            if defeated_count >= 5 or player.level >= 3:
                print("\n=== BOSS BATTLE ===")
                boss = BOSS_ENEMY.model_copy()
                print(f"The mighty {boss.name} appears!")
                print(f"Boss Stats: HP {boss.hp}, ATK {boss.attack}, DEF {boss.defense}")

                def action_provider(p, e):
                    return choose_action_in_battle(p)

                player, victory, msg = battle(player, boss, action_provider)
                print(msg)

                if victory:
                    print("\n*** CONGRATULATIONS! You defeated the boss and saved the world! ***")
                    game_over = True
                else:
                    game_over = True
            else:
                print("\nYou are not ready yet. Defeat 5 enemies or reach level 3.")

        elif choice == "q":
            print("\nThanks for playing!")
            game_over = True

    if not player.alive:
        print("\nGAME OVER")


if __name__ == "__main__":
    main()
