import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.dirname(p=__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from core.service.battle_service import BattleService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auto Chess War API")
battle_service = BattleService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

class CreateBattleRequest(BaseModel):
    team_a: List[str]
    team_b: List[str]
    level: Optional[int] = 5

@app.post("/battles")
def create_battle(req: CreateBattleRequest):
    battle_id, battle = battle_service.create_battle(req.team_a, req.team_b, req.level)
    return {"battle_id": battle_id}

@app.post("/battles/{battle_id}/turn")
def step_turn(battle_id: str):
    try:
        result = battle_service.next_turn(battle_id)
        battle = battle_service.get_battle(battle_id)
        return {"result": result, "summary": battle.get_battle_summary()}
    except ValueError:
        raise HTTPException(status_code=404, detail="Battle not found")

@app.post("/battles/{battle_id}/autoplay")
def autoplay(battle_id: str, max_turns: Optional[int] = 50):
    try:
        results, battle = battle_service.autoplay(battle_id, max_turns)
        return {"results": results, "summary": battle.get_battle_summary()}
    except ValueError:
        raise HTTPException(status_code=404, detail="Battle not found")

@app.get("/battles/{battle_id}")
def get_battle(battle_id: str):
    battle = battle_service.get_battle(battle_id)
    if not battle:
        raise HTTPException(status_code=404, detail="Battle not found")
    return battle.get_battle_summary()

@app.get("/battles")
def list_battles():
    return {bid: b.get_battle_summary() for bid, b in battle_service._battles.items()}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000, reload=True)