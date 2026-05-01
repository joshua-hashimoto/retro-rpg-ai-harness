"""Base character model shared by player and enemies."""

from typing import Self

from pydantic import BaseModel, Field, field_validator


class CharacterModel(BaseModel):
    """Base Pydantic model for all characters in the game."""

    name: str
    max_hp: int = Field(gt=0)
    hp: int = Field(ge=0)
    attack: int = Field(ge=0)
    defense: int = Field(ge=0)

    @field_validator("hp")
    @classmethod
    def hp_cannot_exceed_max_hp(cls, v: int, info) -> int:  # noqa: ANN001
        """Clamp hp to max_hp if it would exceed it."""
        if "max_hp" in info.data and v > info.data["max_hp"]:
            return info.data["max_hp"]
        return v

    @property
    def alive(self) -> bool:
        """Return True if hp is greater than zero."""
        return self.hp > 0

    def take_damage(self, amount: int) -> Self:
        """Return a copy with hp reduced by amount (minimum 0)."""
        return self.model_copy(update={"hp": max(0, self.hp - amount)})

    def heal_full(self) -> Self:
        """Return a copy with hp restored to max_hp."""
        return self.model_copy(update={"hp": self.max_hp})
