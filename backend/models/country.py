"""
country.py — Country data model
Holds everything about a player's nation.
"""

from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ── Enums ─────────────────────────────────────────────────────────────────────

class GeographyType(str, Enum):
    COASTAL     = "coastal"
    LANDLOCKED  = "landlocked"
    ISLAND      = "island"
    MOUNTAIN    = "mountain"
    DESERT      = "desert"
    JUNGLE      = "jungle"
    PLAINS      = "plains"
    ARCTIC      = "arctic"


class ClimateType(str, Enum):
    TROPICAL  = "tropical"
    COLD      = "cold"
    DRY       = "dry"
    TEMPERATE = "temperate"


class GovernmentType(str, Enum):
    MONARCHY     = "monarchy"
    DEMOCRACY    = "democracy"
    DICTATORSHIP = "dictatorship"
    THEOCRACY    = "theocracy"
    REPUBLIC     = "republic"


class CultureVibe(str, Enum):
    PEACEFUL    = "peaceful"
    AGGRESSIVE  = "aggressive"
    SPIRITUAL   = "spiritual"
    SCIENTIFIC  = "scientific"
    MERCHANT    = "merchant"


class EconomyFocus(str, Enum):
    TRADE         = "trade"
    FARMING       = "farming"
    MINING        = "mining"
    MANUFACTURING = "manufacturing"
    TOURISM       = "tourism"


class CurrencyType(str, Enum):
    FIAT             = "fiat"
    RESOURCE_BACKED  = "resource_backed"


class MilitaryStance(str, Enum):
    DEFENSIVE  = "defensive"
    AGGRESSIVE = "aggressive"
    MERCENARY  = "mercenary"


class StartingSituation(str, Enum):
    FREE_STABLE        = "free_stable"
    FREE_UNSTABLE      = "free_unstable"
    UNDER_INFLUENCE    = "under_influence"
    OCCUPIED           = "occupied"
    NEWLY_INDEPENDENT  = "newly_independent"
    ISOLATED           = "isolated"
    DISPUTED_TERRITORY = "disputed_territory"
    VASSAL_STATE       = "vassal_state"


class CountrySize(str, Enum):
    SMALL  = "small"
    MEDIUM = "medium"
    LARGE  = "large"


class StartingWealth(str, Enum):
    POOR    = "poor"
    AVERAGE = "average"
    RICH    = "rich"


class SpecialTrait(str, Enum):
    ANCIENT_KNOWLEDGE = "ancient_knowledge"   # science faster
    SEAFARERS         = "seafarers"           # trade routes cheaper
    WARRIOR_BLOOD     = "warrior_blood"       # military morale always high
    MERCHANT_GUILD    = "merchant_guild"      # trade income bonus
    FERTILE_LANDS     = "fertile_lands"       # food always surplus
    INNOVATORS        = "innovators"          # tech development faster
    DIPLOMATS         = "diplomats"           # alliance bonuses
    SHADOW_NETWORK    = "shadow_network"      # espionage advantage


# ── Budget Allocation ─────────────────────────────────────────────────────────

class BudgetAllocation(BaseModel):
    military:       int = Field(ge=0)
    infrastructure: int = Field(ge=0)
    education:      int = Field(ge=0)
    resources:      int = Field(ge=0)
    diplomacy:      int = Field(ge=0)
    happiness:      int = Field(ge=0)
    treasury:       int = Field(ge=0)


# ── Rivalry Choice ────────────────────────────────────────────────────────────

class RivalryChoice(BaseModel):
    rival_country_id: str
    intensity: str   # cold / moderate / hot


# ── Country Creation Input (from player) ─────────────────────────────────────

class CountryCreateRequest(BaseModel):
    player_id:          str
    world_id:           str

    # Identity
    country_name:       str = Field(min_length=2, max_length=40)
    capital_name:       str = Field(min_length=2, max_length=40)
    language:           str = Field(min_length=2, max_length=30)
    religion:           str = Field(min_length=2, max_length=40)
    culture_vibe:       CultureVibe
    national_symbol:    str = Field(min_length=2, max_length=60)

    # Geography
    geography_type:     GeographyType
    climate:            ClimateType
    size:               CountrySize
    starting_situation: StartingSituation

    # History
    country_age:        int = Field(ge=1, le=5000, description="Years old")
    origin_story:       str = Field(min_length=10, max_length=300)
    has_old_rivalry:    bool = False
    golden_age:         bool = False
    past_trauma:        Optional[str] = None

    # Government
    government_type:    GovernmentType
    leader_title:       str = Field(min_length=2, max_length=30)

    # Economy
    economy_focus:      EconomyFocus
    currency_type:      CurrencyType
    starting_wealth:    StartingWealth
    tax_culture:        str = Field(description="high_welfare or low_tax_free_market")

    # Military
    military_stance:    MilitaryStance

    # Special trait
    special_trait:      SpecialTrait

    # Crises chosen (list of crisis type strings)
    chosen_crises:      list[str] = Field(default_factory=list, max_length=3)

    # Rivalries chosen
    chosen_rivalries:   list[RivalryChoice] = Field(default_factory=list, max_length=2)

    # Budget allocation (after bonus coins calculated)
    budget:             BudgetAllocation


# ── Country State (stored in world) ──────────────────────────────────────────

class CountryState(BaseModel):
    country_id:         str
    player_id:          str
    world_id:           str

    # Identity
    country_name:       str
    capital_name:       str
    language:           str
    religion:           str
    culture_vibe:       CultureVibe
    national_symbol:    str
    special_trait:      SpecialTrait
    flag_color:         str = "#1a1a2e"   # default, player can change later

    # Geography
    geography_type:     GeographyType
    climate:            ClimateType
    size:               CountrySize
    starting_situation: StartingSituation

    # History
    country_age:        int
    origin_story:       str
    golden_age:         bool
    past_trauma:        Optional[str]

    # Government
    government_type:    GovernmentType
    leader_title:       str

    # Economy stats (computed from budget + crises)
    gdp:                float
    capital:            float
    inflation:          float
    tax_rate:           float
    interest_rate:      float
    currency_type:      CurrencyType
    economy_focus:      EconomyFocus

    # Military
    military_power:     float
    military_stance:    MilitaryStance

    # Population & happiness
    population:         float
    happiness:          float

    # Resources
    resources:          float
    resource_types:     list[str]

    # Diplomacy
    diplomacy_score:    float
    alliances:          list[str] = Field(default_factory=list)
    rivals:             list[str] = Field(default_factory=list)

    # Crisis & status
    active_crises:      list[str] = Field(default_factory=list)
    is_locked:          bool = False   # locked = creation confirmed

    # Budget spent
    budget_spent:       BudgetAllocation
    total_coins_used:   int
