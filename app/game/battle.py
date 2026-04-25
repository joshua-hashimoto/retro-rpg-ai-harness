from app.models.character_model import CharacterModel


def calculate_damage(attacker: CharacterModel, defender: CharacterModel) -> int:
    return max(1, attacker.attack - defender.defense)


def execute_attack(
    attacker: CharacterModel, defender: CharacterModel
) -> tuple[CharacterModel, int]:
    damage = calculate_damage(attacker, defender)
    new_defender = defender.take_damage(damage)
    return (new_defender, damage)
