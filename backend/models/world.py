"""
world.py — World data model
One world holds all countries and institutions.
"""

from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import time


class WorldStatus(str, Enum):
    LOBBY       = "lobby"        # players joining, creating countries
    ACTIVE      = "active"       # game running
    PAUSED      = "paused"
    FINISHED    = "finished"


class WorldCreateRequest(BaseModel):
    world_name:     str = Field(min_length=3, max_length=50)
    host_player_id: str
    max_players:    int = Field(ge=2, le=20, default=8)
    turn_limit:     int = Field(ge=10, le=200, default=50)


class WorldState(BaseModel):
    world_id:       str = Field(default_factory=lambda: str(uuid.uuid4())[:8].upper())
    world_name:     str
    host_player_id: str
    max_players:    int
    turn_limit:     int
    current_turn:   int = 0
    status:         WorldStatus = WorldStatus.LOBBY
    created_at:     float = Field(default_factory=time.time)

    # Country IDs in this world
    country_ids:    list[str] = Field(default_factory=list)

    # World events log
    events_log:     list[str] = Field(default_factory=list)

    # Institutions active
    world_bank_active: bool = False
    un_active:         bool = False
    unions:            list[str] = Field(default_factory=list)
