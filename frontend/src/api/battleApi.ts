import axios from "axios";

const API_BASE = "http://localhost:10000"; // FastAPI backend

export const createBattle = async (teamA: string[], teamB: string[], level = 5) => {
  const { data } = await axios.post(`${API_BASE}/battles`, {
    team_a: teamA,
    team_b: teamB,
    level,
  });
  return data.battle_id;
};

export const getBattle = async (battleId: string) => {
  const { data } = await axios.get(`${API_BASE}/battles/${battleId}`);
  return data;
};

export const nextTurn = async (battleId: string) => {
  const { data } = await axios.post(`${API_BASE}/battles/${battleId}/turn`);
  return data;
};
