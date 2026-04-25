from pydantic import Field
from app.models.character_model import CharacterModel


class EnemyModel(CharacterModel):
    exp_reward: int = Field(ge=0)
    gold_reward: int = Field(ge=0)
    is_boss: bool = False
