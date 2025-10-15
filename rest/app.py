from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import uvicorn
import sys
import os

sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.dirname(p=__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from core.model.battle.battle import Battle, BattleState
from core.model.characters.character import Character, Element
from core.model.characters.knight.knight import Knight

app = FastAPI(title="Auto Chess War API")

# In-memory storage for battles
BATTLES = {}

BATTLES[1] = Battle(
    team_a=[Knight("Arthur", 5, Element.FIRE, speed=80), Knight("Lancelot", 5, Element.WATER, speed=90)],
    team_b=[Knight("Mordred", 5, Element.WIND, speed=50), Knight("Morgana", 5, Element.WIND, speed=70)],
)

class CreateBattleRequest(BaseModel):
    team_a: List[str]  # names of knights for simplicity
    team_b: List[str]
    level: Optional[int] = 5

class BattleIdResponse(BaseModel):
    battle_id: str

@app.post("/battles", response_model=BattleIdResponse)
def create_battle(req: CreateBattleRequest):
    # For simplicity, create Knights for each provided name
    level = req.level or 1
    team_a = [Knight(name, level, Element.FIRE) for name in req.team_a]
    team_b = [Knight(name, level, Element.WATER) for name in req.team_b]

    battle = Battle(team_a, team_b)
    battle_id = str(uuid.uuid4())
    BATTLES[battle_id] = battle
    return {"battle_id": battle_id}

@app.post("/battles/{battle_id}/turn")
def step_turn(battle_id: str):
    battle = BATTLES.get(battle_id)
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    if battle.state != BattleState.ONGOING:
        return {"state": battle.state.value, "message": "Battle not ongoing"}
    result = battle.next_turn()
    return {"result": result, "summary": battle.get_battle_summary()}

@app.post("/battles/{battle_id}/autoplay")
def autoplay(battle_id: str, max_turns: Optional[int] = 50):
    battle: Battle = BATTLES.get(battle_id)
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    results = []
    turns = 0
    while battle.state == BattleState.ONGOING and turns < max_turns:
        results.append(battle.next_turn())
        turns += 1
    return {"results": results, "summary": battle.get_battle_summary()}

@app.get("/battles/{battle_id}")
def get_battle(battle_id: str):
    battle: Battle = BATTLES.get(battle_id)
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    return battle.get_battle_summary()

@app.get("/battles")
def list_battles():
    return {bid: BATTLES[bid].get_battle_summary() for bid in BATTLES}

if __name__ == "__main__":
    uvicorn.run("app:app", log_level="info", host="0.0.0.0", port=10000, reload=True)