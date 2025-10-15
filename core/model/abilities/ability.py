from __future__ import annotations
from typing import List, Optional, Tuple, Union
from enum import Enum
import random

from core.model.characters.character import Character
from core.model.battle.battle_character import BattleCharacter

class TargetType(Enum):
    SELF = "self"
    SINGLE_ENEMY = "single_enemy"
    SINGLE_ALLY = "single_ally"
    ALL_ENEMIES = "all_enemies"
    ALL_ALLIES = "all_allies"
    ADJACENT_ENEMIES = "adjacent_enemies"
    ADJACENT_ALLIES = "adjacent_allies"

class Ability:
    def __init__(self, 
                 name: str, 
                 description: str,
                 cooldown: int = 0,
                 current_cooldown: int = 0,
                 target_type: TargetType = TargetType.SINGLE_ENEMY):
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.current_cooldown = current_cooldown
        self.target_type = target_type
    
    def execute(self, caster: Union[Character, BattleCharacter], target: Optional[Union[Character, BattleCharacter]] = None,
                allies: List[Union[Character, BattleCharacter]] = None, enemies: List[Union[Character, BattleCharacter]] = None) -> str:
        """Execute the ability"""
        if self.current_cooldown > 0:
            return f"{self.name} is on cooldown! ({self.current_cooldown} turns remaining)"

        # Set cooldown
        self.current_cooldown = self.cooldown

        # Default behaviour: call _apply_effect which subclasses should override.
        return self._apply_effect(caster, target, allies, enemies)
    
    def _apply_effect(self, caster: Union[Character, BattleCharacter], target: Optional[Union[Character, BattleCharacter]],
                     allies: List[Union[Character, BattleCharacter]], enemies: List[Union[Character, BattleCharacter]]) -> str:
        """Override this method with specific ability logic. Default message works with either
        Character or BattleCharacter caster types."""
        caster_name = caster.character.name if isinstance(caster, BattleCharacter) else getattr(caster, 'name', 'Unknown')
        return f"{caster_name} uses {self.name}!"
    
    def reduce_cooldown(self):
        """Reduce cooldown by 1 at the start of each turn"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def __repr__(self):
        return f"Ability(name={self.name}, cooldown={self.current_cooldown}/{self.cooldown})"