export interface Character {
  name: string;
  element: string;
  level: number;
  health: number;
  speed: number;
  damage: number;
}

export interface BattleCharacter {
  character: Character;
  current_health: number;
  is_alive: boolean;
  status_effects: Record<string, any>;
}

export interface BattleSummary {
  state: string;
  turn: number;
  team_a: BattleCharacter[];
  team_b: BattleCharacter[];
  active_character: string | null;
  log: string[];
}
