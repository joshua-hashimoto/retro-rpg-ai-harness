"""Player model with level, experience, potions, and gold."""
from app.models.character_model import CharacterModel


class PlayerModel(CharacterModel):
    """Pydantic model representing the player character."""

    level: int = 1
    exp: int = 0
    next_exp: int = 10
    potions: int = 3
    gold: int = 10

    def __init__(self, **data: object) -> None:
        """Initialize the player with sensible defaults when stats are omitted."""
        if "max_hp" not in data:
            data["max_hp"] = 30
        if "hp" not in data:
            data["hp"] = data["max_hp"]
        if "attack" not in data:
            data["attack"] = 5
        if "defense" not in data:
            data["defense"] = 1
        if "gold" not in data:
            data["gold"] = 10
        super().__init__(**data)

    def use_potion(self) -> "PlayerModel":
        """Consume one potion and restore HP to max; return self if no potions remain."""
        if self.potions > 0:
            return self.model_copy(update={"potions": self.potions - 1, "hp": self.max_hp})
        return self

    def add_potion(self, amount: int) -> "PlayerModel":
        """Return a copy with potions increased by amount."""
        return self.model_copy(update={"potions": self.potions + amount})

    def gain_exp(self, amount: int) -> tuple["PlayerModel", bool]:
        """Apply exp gain, handle level-ups, and return updated player with level-up flag."""
        current_exp = self.exp + amount
        current_level = self.level
        current_next_exp = self.next_exp
        current_max_hp = self.max_hp
        current_attack = self.attack
        current_defense = self.defense

        leveled_up = False
        while current_exp >= current_next_exp:
            leveled_up = True
            current_exp -= current_next_exp
            current_level += 1
            current_next_exp = int(current_next_exp * 1.5)
            current_max_hp += 5
            current_attack += 2
            current_defense += 1

        updates = {
            "exp": current_exp,
            "next_exp": current_next_exp,
            "level": current_level,
            "max_hp": current_max_hp,
            "attack": current_attack,
            "defense": current_defense,
        }

        if leveled_up:
            updates["hp"] = current_max_hp

        return self.model_copy(update=updates), leveled_up

    def spend_gold(self, amount: int) -> "PlayerModel":
        """Spend gold if funds are sufficient; return self otherwise."""
        if self.gold >= amount:
            return self.model_copy(update={"gold": self.gold - amount})
        return self

    def gain_gold(self, amount: int) -> "PlayerModel":
        """Return a copy with gold increased by amount."""
        return self.model_copy(update={"gold": self.gold + amount})
