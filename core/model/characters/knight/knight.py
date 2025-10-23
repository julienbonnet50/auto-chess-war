from core.model.abilities.damage.basic import BasicAttack
from core.model.characters.character import Character, CharacterElement
class Knight(Character):
    def __init__(self, name: str, level: int, char_element: CharacterElement, **kwargs):
        base_stats = {
            'health': 120 + (level * 10),
            'speed': 80,
            'damage': 90 + (level * 5),
            'ability_power': 20,
            'armor': 100 + (level * 8),
            'magic_resist': 60 + (level * 4),
            **kwargs
        }
        super().__init__(name, level, char_element, **base_stats)
        self.abilities = [
            BasicAttack()
        ]