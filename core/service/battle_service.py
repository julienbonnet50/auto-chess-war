import uuid
from core.model.battle.battle import Battle, BattleState
from core.model.characters.element import CharacterElement
from core.model.characters.knight.knight import Knight

class BattleService:
    def __init__(self):
        self._battles = {}

    def create_battle(self, team_a_names, team_b_names, level=5):
        team_a = [Knight(name, level, CharacterElement.FIRE) for name in team_a_names]
        team_b = [Knight(name, level, CharacterElement.WATER) for name in team_b_names]
        battle = Battle(team_a, team_b)
        battle_id = str(uuid.uuid4())
        self._battles[battle_id] = battle
        return battle_id, battle

    def get_battle(self, battle_id):
        return self._battles.get(battle_id)

    def next_turn(self, battle_id):
        battle = self.get_battle(battle_id)
        if not battle:
            raise ValueError("Battle not found")
        return battle.next_turn()

    def autoplay(self, battle_id, max_turns=50):
        battle = self.get_battle(battle_id)
        if not battle:
            raise ValueError("Battle not found")
        results = []
        turns = 0
        while battle.state == BattleState.ONGOING and turns < max_turns:
            results.append(battle.next_turn())
            turns += 1
        return results, battle