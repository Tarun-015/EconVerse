"""
db.py — Simple JSON file-based storage
No heavy DB setup needed for now.
"""

import json
import os
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "db.json"


def _load() -> dict:
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _save({"worlds": {}, "countries": {}})
    with open(DB_PATH, "r") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


# ── Worlds ────────────────────────────────────────────────────────────────────

def save_world(world: dict) -> None:
    data = _load()
    data["worlds"][world["world_id"]] = world
    _save(data)


def get_world(world_id: str) -> dict | None:
    return _load()["worlds"].get(world_id)


def list_worlds() -> list[dict]:
    return list(_load()["worlds"].values())


# ── Countries ─────────────────────────────────────────────────────────────────

def save_country(country: dict) -> None:
    data = _load()
    data["countries"][country["country_id"]] = country
    # also link to world
    wid = country["world_id"]
    if wid in data["worlds"]:
        cids = data["worlds"][wid].get("country_ids", [])
        if country["country_id"] not in cids:
            cids.append(country["country_id"])
        data["worlds"][wid]["country_ids"] = cids
    _save(data)


def get_country(country_id: str) -> dict | None:
    return _load()["countries"].get(country_id)


def get_countries_in_world(world_id: str) -> list[dict]:
    data = _load()
    world = data["worlds"].get(world_id, {})
    ids = world.get("country_ids", [])
    return [data["countries"][cid] for cid in ids if cid in data["countries"]]
