from model.abilities.ability import Ability, TargetType

class BasicAttack(Ability):
    def __init__(self):
        super().__init__(
            name="Basic Attack",
            description="A basic physical attack",
            cooldown=0,
            target_type=TargetType.SINGLE_ENEMY
        )
    
    def _apply_effect(self, caster, target, allies, enemies):
        if not target:
            return "No target for Basic Attack!"
        
        damage = caster.damage
        target.health -= damage
        
        return f"⚔️ {caster.name} attacks {target.name} for {damage:.1f} damage!"