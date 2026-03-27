"""
world_routes.py — Create and fetch worlds
"""

from fastapi import APIRouter, HTTPException
from ..models.world import WorldCreateRequest, WorldState
from ..db import save_world, get_world, list_worlds

router = APIRouter(prefix="/world", tags=["World"])


@router.post("/create")
def create_world(req: WorldCreateRequest):
    world = WorldState(
        world_name     = req.world_name,
        host_player_id = req.host_player_id,
        max_players    = req.max_players,
        turn_limit     = req.turn_limit,
    )
    save_world(world.model_dump())
    return {"success": True, "world": world.model_dump()}


@router.get("/list")
def get_all_worlds():
    return {"worlds": list_worlds()}


@router.get("/{world_id}")
def get_world_by_id(world_id: str):
    w = get_world(world_id)
    if not w:
        raise HTTPException(status_code=404, detail="World not found")
    return {"world": w}
