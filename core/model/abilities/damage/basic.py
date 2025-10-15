from core.model.abilities.ability import Ability, TargetType
from core.model.battle.battle_character import BattleCharacter

class BasicAttack(Ability):
    def __init__(self):
        super().__init__(
            name="Basic Attack",
            description="A basic physical attack",
            cooldown=0,
            target_type=TargetType.SINGLE_ENEMY
        )
    
    def _apply_effect(self, caster, target: BattleCharacter, allies, enemies):
        if not target:
            return "No target for Basic Attack!"
        # Determine caster name and attack value whether caster is a BattleCharacter or base Character
        caster_name = caster.character.name if isinstance(caster, BattleCharacter) else getattr(caster, 'name', 'Unknown')
        damage = None
        if isinstance(caster, BattleCharacter):
            damage = caster.character.damage
        else:
            damage = getattr(caster, 'damage', 0)

        # Apply damage using take_damage when possible
        actual_damage = damage
        if hasattr(target, 'take_damage'):
            actual_damage = target.take_damage(damage)
        else:
            # Fallback: try to decrement current_health if attribute exists
            if hasattr(target, 'current_health'):
                target.current_health = max(0, target.current_health - damage)

        target_name = target.character.name if isinstance(target, BattleCharacter) else getattr(target, 'name', 'Unknown')

        return f"⚔️ {caster_name} attacks {target_name} for {actual_damage} damage!"