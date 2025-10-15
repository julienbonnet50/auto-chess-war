from __future__ import annotations
from typing import List, Optional, Tuple
from enum import Enum
import random

from model.characters.character import Character

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
    
    def execute(self, caster: Character, target: Optional[Character] = None, 
                allies: List[Character] = None, enemies: List[Character] = None) -> str:
        """Execute the ability"""
        if self.current_cooldown > 0:
            return f"{self.name} is on cooldown! ({self.current_cooldown} turns remaining)"
        
        # Set cooldown
        self.current_cooldown = self.cooldown
        
        return self._apply_effect(caster, target, allies, enemies)
    
    def _apply_effect(self, caster: Character, target: Optional[Character], 
                     allies: List[Character], enemies: List[Character]) -> str:
        """Override this method with specific ability logic"""
        return f"{caster.name} uses {self.name}!"
    
    def reduce_cooldown(self):
        """Reduce cooldown by 1 at the start of each turn"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def __repr__(self):
        return f"Ability(name={self.name}, cooldown={self.current_cooldown}/{self.cooldown})"