"""Player model with level, experience, potions, and gold."""

from pydantic import Field, model_validator

from app.models.character_model import CharacterModel


class PlayerModel(CharacterModel):
    """Pydantic model representing the player character."""

    max_hp: int = Field(default=30, gt=0)
    hp: int = Field(default=30, ge=0)
    attack: int = Field(default=5, ge=0)
    defense: int = Field(default=1, ge=0)
    level: int = 1
    exp: int = 0
    next_exp: int = 10
    potions: int = 3
    gold: int = 10

    @model_validator(mode="before")
    @classmethod
    def set_default_stats(cls, data: dict[str, object]) -> dict[str, object]:
        """Set hp to max_hp when hp is not explicitly provided."""
        if "hp" not in data:
            data["hp"] = data.get("max_hp", 30)
        return data

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
