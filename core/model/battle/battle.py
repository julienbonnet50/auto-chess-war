from __future__ import annotations
from typing import List, Dict, Optional
from enum import Enum
from core.model.battle.battle_character import BattleCharacter
from core.model.characters.character import Character


class BattleState(Enum):
    SETUP = "setup"
    ONGOING = "ongoing"
    VICTORY = "victory"
    DEFEAT = "defeat"
    DRAW = "draw"


class Battle:
    TURN_METER_THRESHOLD = 1000  # Full meter

    def __init__(self, team_a: List[Character], team_b: List[Character]):
        self.team_a = [BattleCharacter(char) for char in team_a]
        self.team_b = [BattleCharacter(char) for char in team_b]
        self.state = BattleState.SETUP
        self.current_turn = 0
        self.active_character: Optional[BattleCharacter] = None
        self.turn_meters: Dict[BattleCharacter, float] = {}
        self.battle_log: List[str] = []
        self.start_battle()

    def start_battle(self):
        """Start the battle with all turn meters at 0 and determine first active character."""
        self.state = BattleState.ONGOING

        # Initialize turn meters
        for bc in self.team_a + self.team_b:
            self.turn_meters[bc] = 0

        # First turn deterministic: highest speed, then highest damage
        all_chars = self.team_a + self.team_b
        first_char = max(all_chars, key=lambda bc: (bc.character.speed, bc.character.damage))
        self.active_character = first_char

    def next_turn(self) -> str:
        """Progress the battle to the next action; always returns a character turn."""
        if self.state != BattleState.ONGOING:
            return "Battle is not ongoing!"

        # Keep ticking until at least one character reaches the threshold
        while True:
            # Step 1: Increase turn meters for all alive characters
            for bc in self.team_a + self.team_b:
                if bc.is_alive:
                    self.turn_meters[bc] += bc.calculate_turn_meter_gain()

            # Step 2: Check who can act
            ready_to_act = [bc for bc in self.team_a + self.team_b
                            if bc.is_alive and bc.can_take_action() and self.turn_meters[bc] >= self.TURN_METER_THRESHOLD]

            if ready_to_act:
                # Pick the character with the highest turn meter
                active_bc = max(ready_to_act, key=lambda bc: self.turn_meters[bc])
                self.active_character = active_bc
                self.turn_meters[active_bc] = 0  # reset after acting

                # Step 3: Execute the turn
                enemies = self._get_enemies_bc(active_bc)
                if not enemies:
                    self._check_battle_end()
                    return "❌ No enemies left!"

                ability_index = 0  # for simplicity, pick first ability
                target_index = 0   # first alive enemy
                result = self.execute_turn(ability_index, "enemy", target_index)
                return result

    def get_active_character(self) -> Optional[BattleCharacter]:
        return self.active_character

    def execute_turn(self, ability_index: int, target_team: str = "enemy", target_index: int = 0) -> str:
        """Execute a turn for the active character."""
        if self.state != BattleState.ONGOING:
            return "Battle is not ongoing!"

        active_bc = self.get_active_character()
        if not active_bc or not active_bc.can_take_action():
            return f"{active_bc.character.name if active_bc else 'No one'} cannot act!"

        target_bc = self._get_target(active_bc, target_team, target_index)
        if not target_bc:
            return "No valid target!"

        allies = self._get_allies_bc(active_bc)
        enemies = self._get_enemies_bc(active_bc)

        result = active_bc.use_ability(ability_index, target_bc, allies, enemies)

        # Update death status immediately
        self._update_death_status()

        # Process end-of-turn effects
        self._process_end_of_turn(active_bc)

        # Check if battle ended
        self._check_battle_end()

        # Increment turn count if battle ongoing
        if self.state == BattleState.ONGOING:
            self.current_turn += 1

        return result

    # ---------- Helper Methods ----------

    def _get_target(self, active_bc: BattleCharacter, target_team: str, target_index: int) -> Optional[BattleCharacter]:
        target_pool = self.team_b if active_bc in self.team_a else self.team_a
        if target_team == "ally":
            target_pool = self.team_a if active_bc in self.team_a else self.team_b

        alive_targets = [bc for bc in target_pool if bc.is_alive]
        if not alive_targets:
            return None

        return alive_targets[target_index] if 0 <= target_index < len(alive_targets) else alive_targets[0]

    def _get_allies_bc(self, character: BattleCharacter) -> List[BattleCharacter]:
        team = self.team_a if character in self.team_a else self.team_b
        return [bc for bc in team if bc.is_alive and bc != character]

    def _get_enemies_bc(self, character: BattleCharacter) -> List[BattleCharacter]:
        team = self.team_b if character in self.team_a else self.team_a
        return [bc for bc in team if bc.is_alive]

    def _update_death_status(self):
        for bc in self.team_a + self.team_b:
            if bc.current_health <= 0 and bc.is_alive:
                bc.is_alive = False

    def _process_end_of_turn(self, character: BattleCharacter):
        to_remove = []
        for eff, data in character.status_effects.items():
            data['duration'] -= 1
            if data['duration'] <= 0:
                to_remove.append(eff)
        for eff in to_remove:
            del character.status_effects[eff]

    def _check_battle_end(self):
        team_a_alive = any(bc.is_alive for bc in self.team_a)
        team_b_alive = any(bc.is_alive for bc in self.team_b)

        if not team_a_alive and not team_b_alive:
            self.state = BattleState.DRAW
        elif not team_a_alive:
            self.state = BattleState.DEFEAT
        elif not team_b_alive:
            self.state = BattleState.VICTORY

    def get_battle_summary(self) -> Dict:
        return {
            "state": self.state.value,
            "turn": self.current_turn,
            "team_a": [bc for bc in self.team_a],
            "team_b": [bc for bc in self.team_b],
            "active_character": str(self.get_active_character()) if self.get_active_character() else None,
            "log": self.battle_log[-5:]
        }

    def auto_play_round(self) -> List[str]:
        """Auto-play with safety limits."""
        results = []
        if self.state != BattleState.ONGOING:
            return ["Battle is not ongoing!"]

        max_turns = 50
        turns_played = 0

        while self.state == BattleState.ONGOING and turns_played < max_turns:
            result = self.next_turn()
            results.append(result)
            turns_played += 1

        if turns_played >= max_turns:
            results.append("⚠️ Auto-play stopped: reached turn limit")

        return results
