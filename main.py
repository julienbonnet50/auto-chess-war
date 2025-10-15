# Create characters
from model.battle.battle import Battle, BattleState
from model.characters.character import Element
from model.characters.knight.knight import Knight

# Create knights
knight1 = Knight("Knight Fire", 5, Element.FIRE, health=500, armor=100, damage=80, speed=90)
knight2 = Knight("Knight Water", 5, Element.WATER, health=500, armor=100, damage=80, speed=80)
knight3 = Knight("Knight Wind", 5, Element.WIND, health=500, armor=100, damage=80, speed=43)

# Create teams
team_a = [knight1, knight2]
team_b = [knight3]

# Start battle
battle = Battle(team_a, team_b)
print(battle.get_battle_summary())

# Auto-play the battle until it ends
while battle.state == BattleState.ONGOING:
    battle.auto_play_round()
    print(battle.get_battle_summary())

