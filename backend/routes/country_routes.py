"""
country_routes.py — Country creation and retrieval
"""

from fastapi import APIRouter, HTTPException
from ..models.country import CountryCreateRequest
from ..models.crisis import CRISIS_CATALOGUE, RIVALRY_CATALOGUE
from ..engine.budget import calculate_bonus_coins, validate_budget, build_country_state
from ..db import save_country, get_country, get_countries_in_world, get_world

router = APIRouter(prefix="/country", tags=["Country"])


@router.get("/options")
def get_creation_options():
    """Return all enums and catalogues the frontend needs to build the creation form."""
    crises = {
        k.value: {
            "label":            v.label,
            "description":      v.description,
            "bonus_coins":      v.bonus_coins,
            "happiness_penalty": v.happiness_penalty,
            "special_note":     v.special_note,
        }
        for k, v in CRISIS_CATALOGUE.items()
    }
    rivalries = {
        k.value: {
            "label":            v.label,
            "description":      v.description,
            "bonus_coins":      v.bonus_coins,
            "happiness_penalty": v.happiness_penalty,
        }
        for k, v in RIVALRY_CATALOGUE.items()
    }
    return {
        "base_coins": 1000,
        "crises": crises,
        "rivalries": rivalries,
    }


@router.post("/preview-coins")
def preview_coins(req: CountryCreateRequest):
    """Before submitting, let player see how many coins they'll have."""
    total = calculate_bonus_coins(req)
    return {"total_coins": total, "base_coins": 1000, "bonus_coins": total - 1000}


@router.post("/create")
def create_country(req: CountryCreateRequest):
    # Check world exists
    world = get_world(req.world_id)
    if not world:
        raise HTTPException(status_code=404, detail="World not found")

    # Check world not full
    existing = get_countries_in_world(req.world_id)
    if len(existing) >= world["max_players"]:
        raise HTTPException(status_code=400, detail="World is full")

    # Check player hasn't already created a country here
    for c in existing:
        if c["player_id"] == req.player_id:
            raise HTTPException(status_code=400, detail="Player already has a country in this world")

    # Calculate total coins
    total_coins = calculate_bonus_coins(req)

    # Validate budget
    ok, msg = validate_budget(req.budget, total_coins)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    # Build country
    country = build_country_state(req, total_coins)
    save_country(country.model_dump())

    return {
        "success":    True,
        "country_id": country.country_id,
        "country":    country.model_dump(),
        "coins_used": total_coins,
    }


@router.get("/world/{world_id}")
def get_countries(world_id: str):
    countries = get_countries_in_world(world_id)
    return {"countries": countries}


@router.get("/{country_id}")
def get_country_by_id(country_id: str):
    c = get_country(country_id)
    if not c:
        raise HTTPException(status_code=404, detail="Country not found")
    return {"country": c}
