from enum import Enum

class Element(Enum):
    FIRE = "Fire"
    WATER = "Water"
    WIND = "Wind"
    GOLD = "Gold"
    SILVER = "Silver"

class Character:
    def __init__(self, 
            name: str,
            level: int,
            element: Element,
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
        self.element: Element = element
        self.health: int = health
        self.speed: int = speed
        self.damage: int = damage
        self.ability_power: int = ability_power
        self.armor: int = armor
        self.magic_resist: int = magic_resist
        
    def __repr__(self) -> str:
        return f"Character(name={self.name}, level={self.level}, element={self.element.value}, health={self.health}, speed={self.speed}, damage={self.damage}, ability_power={self.ability_power}, armor={self.armor}, magic_resist={self.magic_resist})"