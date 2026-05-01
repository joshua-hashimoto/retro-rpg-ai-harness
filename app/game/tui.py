"""TUI display functions for the RPG game."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.models.character_model import CharacterModel
from app.models.enemy_model import EnemyModel
from app.models.player_model import PlayerModel

console = Console()
BOSS_UNLOCK_DEFEATS = 5
BOSS_UNLOCK_LEVEL = 3


def show_main_menu(player: PlayerModel, defeated_count: int) -> None:
    """Display the main action menu.

    Args:
        player: The current player state.
        defeated_count: Number of enemies defeated so far.

    """
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column()
    table.add_row(
        f"[bold blue]Defeated:[/bold blue] {defeated_count}  |  "
        f"[bold green]Level:[/bold green] {player.level}  |  "
        f"[bold yellow]Gold:[/bold yellow] {player.gold}G  |  "
        f"[bold magenta]Potions:[/bold magenta] {player.potions}",
    )
    table.add_row(
        f"[bold red]HP:[/bold red] {player.hp}/{player.max_hp}  |  "
        f"[bold cyan]EXP:[/bold cyan] {player.exp}/{player.next_exp}",
    )

    menu_table = Table(show_header=False, box=None)
    menu_table.add_column()
    menu_table.add_row("[1] Fight Enemy")
    menu_table.add_row("[2] Rest at Inn (Full HP) - 10G")
    if defeated_count >= BOSS_UNLOCK_DEFEATS or player.level >= BOSS_UNLOCK_LEVEL:
        menu_table.add_row("[3] Challenge Boss")
    menu_table.add_row("[0] Quit")

    console.print(Panel.fit(table, title="[bold]MAIN MENU[/bold]", border_style="bright_blue"))
    console.print(menu_table)


def get_user_choice() -> str:
    """Prompt the user and return a valid menu choice."""
    while True:
        choice = input("> ").strip().lower()
        if choice in ["0", "1", "2", "3"]:
            return choice
        console.print("[red]Invalid choice. Please try again.[/red]")


def show_battle_menu(player: PlayerModel) -> None:
    """Display battle action menu.

    Args:
        player: The current player state.

    """
    console.print()
    console.print("[1] Attack")
    if player.potions > 0:
        console.print(f"[2] Use Potion ({player.potions} left)")
    console.print("[3] Flee")


def get_battle_action(player: PlayerModel, enemy: EnemyModel) -> str:
    """Prompt the player to choose a battle action and return it.

    Args:
        player: The current player state.
        enemy: The current enemy state.

    Returns:
        The chosen action: "attack", "potion", or "flee".

    """
    while True:
        console.print()
        console.print(
            f"[bold red]{player.name}: {player.hp}/{player.max_hp} HP[/bold red]  |  "
            f"[bold yellow]{enemy.name}: {enemy.hp}/{enemy.max_hp} HP[/bold yellow]",
        )
        show_battle_menu(player)
        choice = input("Action: ").strip()
        if choice == "1":
            return "attack"
        if choice == "2" and player.potions > 0:
            return "potion"
        if choice == "3":
            return "flee"
        console.print("[red]Invalid action.[/red]")


def show_battle_turn(log: str) -> None:
    """Display a single battle turn result.

    Args:
        log: The log message to display.

    """
    console.print(f"  [italic]{log}[/italic]")


def show_battle_gains(exp: int, gold: int) -> None:
    """Display EXP and gold gained after a victory.

    Args:
        exp: EXP gained.
        gold: Gold gained.

    """
    console.print()
    console.print(
        Panel.fit(
            f"[green]Gained {exp} EXP and {gold} Gold![/green]",
            title="[bold]RESULT[/bold]",
            border_style="green",
        )
    )


def show_complete_battle_result(
    message: str,
    victory: bool,
    exp: int = 0,
    gold: int = 0,
    level_up_message: str | None = None,
) -> None:
    """Display complete battle result in a single panel.

    Args:
        message: The battle result message.
        victory: True if the player won, False otherwise.
        exp: EXP gained.
        gold: Gold gained.
        level_up_message: Optional level up message.

    """
    lines = [message]
    if exp > 0 or gold > 0:
        lines.append("")
        if exp > 0:
            lines.append(f"[green]GAINED: {exp} EXP[/green]")
        if gold > 0:
            lines.append(f"[yellow]GAINED: {gold} GOLD[/yellow]")
    if level_up_message:
        lines.append("")
        lines.append(level_up_message)

    console.print()
    console.print(
        Panel(
            "\n".join(lines),
            title="[bold]RESULT[/bold]",
            border_style="green" if victory else "red",
        )
    )


def show_character_stats(character: CharacterModel, title: str = "") -> None:
    """Display character stats in a formatted table.

    Args:
        character: The character to display stats for.
        title: Optional title for the stats panel.

    """
    table = Table(show_header=False, box=None)
    table.add_column()
    table.add_row(f"[bold]{title}:[/bold]")
    table.add_row(f"  [red]HP:[/red] {character.hp}")
    table.add_row(f"  [orange1]ATK:[/orange1] {character.attack}")
    table.add_row(f"  [blue]DEF:[/blue] {character.defense}")
    console.print(table)


def show_enemy_appears(enemy: EnemyModel) -> None:
    """Display enemy appearance message.

    Args:
        enemy: The enemy that appears.

    """
    console.print()
    console.print(
        Panel(f"[bold yellow]A wild {enemy.name} appears![/bold yellow]", border_style="yellow"),
    )
    show_character_stats(enemy, "Enemy Stats")


def show_boss_appears(boss: EnemyModel) -> None:
    """Display boss appearance message.

    Args:
        boss: The boss enemy that appears.

    """
    console.print()
    console.print(Panel("[bold red]=== BOSS BATTLE ===[/bold red]", border_style="red"))
    console.print(
        Panel(f"[bold red]The mighty {boss.name} appears![/bold red]", border_style="red"),
    )
    show_character_stats(boss, "Boss Stats")


def show_battle_result(message: str, victory: bool) -> None:
    """Display battle result.

    Args:
        message: The battle result message.
        victory: True if the player won, False otherwise.

    """
    console.print()
    console.print(Panel(message, border_style="green" if victory else "red"))


def show_level_up(level: int) -> None:
    """Display level up message.

    Args:
        level: The new level.

    """
    console.print()
    console.print(
        Panel(
            f"[bold green]*** LEVEL UP! You are now level {level}. ***",
            border_style="green",
        ),
    )


def show_inn_rest() -> None:
    """Display inn rest message."""
    console.print()
    console.print(
        Panel(
            "[green]You rested at the inn. HP fully restored![/green]",
            border_style="green",
        ),
    )


def show_title() -> None:
    """Display game title."""
    console.print(Panel("[bold]==== SIMPLE RPG ====[/bold]", border_style="bright_cyan"))


def show_welcome(player_name: str) -> None:
    """Display welcome message.

    Args:
        player_name: The player's name.

    """
    console.print()
    console.print(
        Panel(
            f"Welcome, [bold cyan]{player_name}[/bold cyan]! "
            f"Defeat enemies to level up, then challenge the boss.",
            border_style="cyan",
        ),
    )


def show_thanks() -> None:
    """Display thanks message."""
    console.print()
    console.print("[yellow]Thanks for playing![/yellow]")


def show_game_over() -> None:
    """Display game over message."""
    console.print()
    console.print(Panel("[bold red]GAME OVER[/bold red]", border_style="red"))


def show_boss_not_ready() -> None:
    """Display boss not ready message."""
    console.print()
    console.print("[yellow]You are not ready yet. Defeat 5 enemies or reach level 3.[/yellow]")


def show_victory() -> None:
    """Display victory message."""
    console.print()
    console.print(
        Panel(
            "[bold green]*** CONGRATULATIONS! You defeated the boss "
            "and saved the world! ***[/bold green]",
            border_style="green",
        ),
    )
