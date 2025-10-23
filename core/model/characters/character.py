from enum import Enum

from core.model.characters.element import CharacterElement

class Character:
    def __init__(self, 
            name: str,
            level: int,
            char_element: CharacterElement,
            health: int,
            speed: int,
            damage: int,
            ability_power: int,
            armor: int,
            magic_resist: int
        ):
        # Initialize character attributes
        self.name: str = name
        self.level: int = level
        self.char_element: CharacterElement = char_element
        self.health: int = health
        self.speed: int = speed
        self.damage: int = damage
        self.ability_power: int = ability_power
        self.armor: int = armor
        self.magic_resist: int = magic_resist
        
    def __repr__(self) -> str:
        return f"Character(name={self.name}, level={self.level}, char_element={self.char_element.value}, health={self.health}, speed={self.speed}, damage={self.damage}, ability_power={self.ability_power}, armor={self.armor}, magic_resist={self.magic_resist})"