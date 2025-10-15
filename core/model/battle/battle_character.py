from typing import List, Optional, Any
from core.model.characters.character import Character

class BattleCharacter:
    def __init__(self, character: Character):
        self.character: Character = character
        self.current_health: int = character.health
        self.is_alive: bool = True
        self.status_effects = {}
        self.active_buffs = {}
        self.active_debuffs = {}
        self.next_turn_meter = 0

    def __repr__(self):
        status = "Alive" if self.is_alive else "Dead"
        return f"{self.character.name} (HP: {self.current_health}/{self.character.health}, {status})"

    def __str__(self):
        return self.__repr__()

    def take_damage(self, damage: int) -> int:
        actual_damage = max(0, damage)
        self.current_health -= actual_damage
        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False
        return actual_damage

    def heal(self, amount: int) -> int:
        if not self.is_alive:
            return 0
        actual_heal = min(amount, self.character.health - self.current_health)
        self.current_health += actual_heal
        return actual_heal

    def add_status_effect(self, effect: str, duration: int, value: Any = None):
        self.status_effects[effect] = {
            'duration': duration,
            'value': value
        }

    def has_status_effect(self, effect: str) -> bool:
        return effect in self.status_effects

    def process_start_of_turn(self):
        # Process damage over time effects
        if 'burn' in self.status_effects:
            burn_data = self.status_effects['burn']
            self.take_damage(burn_data['value'])
            burn_data['duration'] -= 1
            if burn_data['duration'] <= 0:
                del self.status_effects['burn']

        # Process stun
        if 'stun' in self.status_effects:
            self.status_effects['stun']['duration'] -= 1
            if self.status_effects['stun']['duration'] <= 0:
                del self.status_effects['stun']

    def can_take_action(self) -> bool:
        return self.is_alive and not self.has_status_effect('stun')

    def calculate_turn_meter_gain(self) -> int:
        base_gain = self.character.speed
        # Apply speed buffs/debuffs
        if 'speed_buff' in self.active_buffs:
            base_gain = int(base_gain * 1.3)  # 30% speed buff
        if 'speed_debuff' in self.active_debuffs:
            base_gain = int(base_gain * 0.7)  # 30% speed debuff
        return base_gain

    def use_ability(self, ability_index: int, target: Optional['BattleCharacter'] = None,
                    allies: List['BattleCharacter'] = None, enemies: List['BattleCharacter'] = None) -> str:
        """Use ability from the character's ability list.

        Abilities are executed with BattleCharacter instances so they can call
        methods like take_damage/heal/add_status_effect directly.
        """
        if not self.is_alive:
            return f"{self.character.name} is dead and cannot act!"

        if 0 <= ability_index < len(self.character.abilities):
            ability = self.character.abilities[ability_index]

            # Pass BattleCharacter objects directly so ability implementations
            # can operate on the battle state (take_damage/heal/etc.)
            allies_list = allies if allies else []
            enemies_list = enemies if enemies else []

            result = ability.execute(self, target, allies_list, enemies_list)

            # Optionally, if ability objects contain declarative fields (damage_amount, heal_amount, etc.)
            # apply them here to BattleCharacters. That logic can be kept in ability implementations,
            # but a small helper is provided below for shared behaviour.
            return result
        return "Invalid ability!"

    def _apply_ability_effects(self, ability, target: Optional['BattleCharacter'], allies: List['BattleCharacter'], enemies: List['BattleCharacter']):
        """Apply simple declarative ability effects to BattleCharacters.

        This helper is intended for ability implementations to call when they want
        a standardized effect application (damage/heal/status/aoe). It's not invoked
        automatically; specific Ability subclasses should call it when appropriate.
        """
        # Apply damage to primary target
        if target and hasattr(ability, 'damage_amount') and getattr(ability, 'damage_amount', 0) > 0:
            actual_damage = target.take_damage(ability.damage_amount)
            # use battle logging in higher-level code; print here for debug
            print(f"DEBUG: {self.character.name} dealt {actual_damage} damage to {target.character.name}, new HP: {target.current_health}")

        # Apply healing to target or self
        if hasattr(ability, 'heal_amount') and getattr(ability, 'heal_amount', 0) > 0:
            if target:
                target.heal(ability.heal_amount)
            else:
                self.heal(ability.heal_amount)

        # Apply status effects
        if hasattr(ability, 'status_effects') and getattr(ability, 'status_effects'):
            for effect, duration in ability.status_effects.items():
                if target:
                    target.add_status_effect(effect, duration)

        # Apply AoE damage/heal if applicable
        if hasattr(ability, 'aoe_damage') and getattr(ability, 'aoe_damage', 0) > 0:
            if hasattr(ability, 'aoe_target') and ability.aoe_target == 'enemies':
                for enemy in enemies:
                    if enemy != target:  # Don't double-damage primary target
                        enemy.take_damage(ability.aoe_damage)
            elif hasattr(ability, 'aoe_target') and ability.aoe_target == 'allies':
                for ally in allies:
                    if ally != self:  # Don't double-heal/buff self
                        ally.heal(ability.aoe_damage)  # Assuming aoe_damage is healing in this context