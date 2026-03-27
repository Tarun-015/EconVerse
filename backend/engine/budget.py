"""
budget.py — Starting budget logic
Converts player choices into actual country stats.
"""

from __future__ import annotations
from ..models.country import (
    CountryCreateRequest, CountryState,
    GeographyType, StartingWealth, CountrySize,
    StartingSituation, CultureVibe, SpecialTrait,
    BudgetAllocation
)
from ..models.crisis import CRISIS_CATALOGUE, RIVALRY_CATALOGUE, CrisisType, RivalryIntensity
import uuid

# ── Base coins every player starts with ──────────────────────────────────────
BASE_COINS = 1000


# ── Geography resource map ────────────────────────────────────────────────────
GEOGRAPHY_RESOURCES: dict[GeographyType, list[str]] = {
    GeographyType.COASTAL:    ["fish", "oil", "fertile_land"],
    GeographyType.LANDLOCKED: ["coal", "iron", "fertile_land"],
    GeographyType.ISLAND:     ["fish", "timber", "rare_minerals"],
    GeographyType.MOUNTAIN:   ["gold", "coal", "iron", "timber"],
    GeographyType.DESERT:     ["oil", "gas", "gold", "rare_earth"],
    GeographyType.JUNGLE:     ["timber", "rare_minerals", "fertile_land"],
    GeographyType.PLAINS:     ["fertile_land", "coal", "fresh_water"],
    GeographyType.ARCTIC:     ["oil", "gas", "rare_earth"],
}

# ── Wealth multipliers ────────────────────────────────────────────────────────
WEALTH_MULTIPLIER: dict[StartingWealth, float] = {
    StartingWealth.POOR:    0.6,
    StartingWealth.AVERAGE: 1.0,
    StartingWealth.RICH:    1.5,
}

# ── Size multipliers ──────────────────────────────────────────────────────────
SIZE_MULTIPLIER: dict[CountrySize, float] = {
    CountrySize.SMALL:  0.7,
    CountrySize.MEDIUM: 1.0,
    CountrySize.LARGE:  1.4,
}

# ── Situation penalties ───────────────────────────────────────────────────────
SITUATION_PENALTIES: dict[StartingSituation, dict] = {
    StartingSituation.FREE_STABLE:        {"gdp": 1.0,  "military": 1.0,  "happiness": 0.0},
    StartingSituation.FREE_UNSTABLE:      {"gdp": 0.8,  "military": 0.85, "happiness": -0.10},
    StartingSituation.UNDER_INFLUENCE:    {"gdp": 0.75, "military": 0.6,  "happiness": -0.12},
    StartingSituation.OCCUPIED:           {"gdp": 0.5,  "military": 0.2,  "happiness": -0.25},
    StartingSituation.NEWLY_INDEPENDENT:  {"gdp": 0.7,  "military": 0.65, "happiness": -0.08},
    StartingSituation.ISOLATED:           {"gdp": 0.9,  "military": 0.9,  "happiness": 0.05},
    StartingSituation.DISPUTED_TERRITORY: {"gdp": 0.8,  "military": 0.75, "happiness": -0.15},
    StartingSituation.VASSAL_STATE:       {"gdp": 0.65, "military": 0.5,  "happiness": -0.18},
}

# ── Special trait bonuses ─────────────────────────────────────────────────────
TRAIT_BONUSES: dict[SpecialTrait, dict] = {
    SpecialTrait.ANCIENT_KNOWLEDGE: {"gdp": 1.05, "diplomacy": 1.1},
    SpecialTrait.SEAFARERS:         {"gdp": 1.08, "resources": 1.1},
    SpecialTrait.WARRIOR_BLOOD:     {"military": 1.25},
    SpecialTrait.MERCHANT_GUILD:    {"gdp": 1.12, "capital": 1.1},
    SpecialTrait.FERTILE_LANDS:     {"resources": 1.2, "population": 1.1},
    SpecialTrait.INNOVATORS:        {"gdp": 1.10},
    SpecialTrait.DIPLOMATS:         {"diplomacy": 1.3, "happiness": 0.05},
    SpecialTrait.SHADOW_NETWORK:    {"military": 1.1, "diplomacy": 1.15},
}


def calculate_bonus_coins(req: CountryCreateRequest) -> int:
    """Total coins = BASE + crisis bonuses + rivalry bonuses"""
    total = BASE_COINS

    for crisis_str in req.chosen_crises:
        try:
            ct = CrisisType(crisis_str)
            total += CRISIS_CATALOGUE[ct].bonus_coins
        except (ValueError, KeyError):
            pass

    for rivalry in req.chosen_rivalries:
        try:
            ri = RivalryIntensity(rivalry.intensity)
            total += RIVALRY_CATALOGUE[ri].bonus_coins
        except (ValueError, KeyError):
            pass

    return total


def validate_budget(budget: BudgetAllocation, total_coins: int) -> tuple[bool, str]:
    """Check player hasn't overspent"""
    spent = (
        budget.military + budget.infrastructure + budget.education +
        budget.resources + budget.diplomacy + budget.happiness + budget.treasury
    )
    if spent > total_coins:
        return False, f"Over budget: spent {spent} but only have {total_coins} coins."
    if spent < 0:
        return False, "Budget values cannot be negative."
    return True, "ok"


def build_country_state(req: CountryCreateRequest, total_coins: int) -> CountryState:
    """
    Convert CountryCreateRequest into a full CountryState.
    All stats are deterministically derived from:
      geography + wealth + size + situation + crises + budget allocation
    """

    b = req.budget
    wealth_m = WEALTH_MULTIPLIER[req.starting_wealth]
    size_m   = SIZE_MULTIPLIER[req.size]
    sit      = SITUATION_PENALTIES[req.starting_situation]

    # ── Crisis compound penalties ─────────────────────────────────────────────
    crisis_happiness_pen = 0.0
    crisis_military_m    = 1.0
    crisis_economy_m     = 1.0
    active_crises        = []

    for crisis_str in req.chosen_crises:
        try:
            ct = CrisisType(crisis_str)
            cd = CRISIS_CATALOGUE[ct]
            crisis_happiness_pen += cd.happiness_penalty
            crisis_military_m    *= cd.military_penalty
            crisis_economy_m     *= cd.economy_penalty
            active_crises.append(crisis_str)
        except (ValueError, KeyError):
            pass

    # ── Rival list ────────────────────────────────────────────────────────────
    rivals = [r.rival_country_id for r in req.chosen_rivalries]

    # ── Core stat formulas ────────────────────────────────────────────────────

    # GDP
    gdp_base = 500 + (b.infrastructure * 0.8) + (b.education * 0.5)
    gdp = gdp_base * wealth_m * size_m * sit["gdp"] * crisis_economy_m

    # Capital (treasury)
    capital_base = 200 + (b.treasury * 1.2)
    capital = capital_base * wealth_m

    # Military power
    military_base = 100 + (b.military * 1.5)
    military = military_base * sit["military"] * crisis_military_m

    # Population (millions)
    pop_base = {CountrySize.SMALL: 2.0, CountrySize.MEDIUM: 8.0, CountrySize.LARGE: 20.0}
    population = pop_base[req.size] * (1.0 + b.happiness * 0.001)

    # Happiness [0..1]
    happiness_base = 0.60
    happiness_budget_bonus = b.happiness * 0.0003
    happiness = (
        happiness_base
        + happiness_budget_bonus
        + sit["happiness"]
        - crisis_happiness_pen
    )
    happiness = max(0.10, min(happiness, 1.0))

    # Resources
    resource_base = 300 + (b.resources * 1.3)
    resources = resource_base * size_m

    # Diplomacy score
    diplomacy_base = 0.5 + (b.diplomacy * 0.001)
    diplomacy = min(diplomacy_base, 1.0)

    # Tax rate from culture
    tax_rate = 0.35 if req.tax_culture == "high_welfare" else 0.18

    # ── Apply special trait bonuses ───────────────────────────────────────────
    tb = TRAIT_BONUSES.get(req.special_trait, {})
    gdp        *= tb.get("gdp", 1.0)
    military   *= tb.get("military", 1.0)
    resources  *= tb.get("resources", 1.0)
    diplomacy  *= tb.get("diplomacy", 1.0)
    capital    *= tb.get("capital", 1.0)
    population *= tb.get("population", 1.0)
    happiness  += tb.get("happiness", 0.0)
    happiness   = max(0.10, min(happiness, 1.0))

    # ── Resource types from geography ─────────────────────────────────────────
    resource_types = GEOGRAPHY_RESOURCES.get(req.geography_type, ["fertile_land"])

    return CountryState(
        country_id         = str(uuid.uuid4())[:8].upper(),
        player_id          = req.player_id,
        world_id           = req.world_id,
        country_name       = req.country_name,
        capital_name       = req.capital_name,
        language           = req.language,
        religion           = req.religion,
        culture_vibe       = req.culture_vibe,
        national_symbol    = req.national_symbol,
        special_trait      = req.special_trait,
        geography_type     = req.geography_type,
        climate            = req.climate,
        size               = req.size,
        starting_situation = req.starting_situation,
        country_age        = req.country_age,
        origin_story       = req.origin_story,
        golden_age         = req.golden_age,
        past_trauma        = req.past_trauma,
        government_type    = req.government_type,
        leader_title       = req.leader_title,
        gdp                = round(gdp, 2),
        capital            = round(capital, 2),
        inflation          = 0.02,
        tax_rate           = tax_rate,
        interest_rate      = 0.05,
        currency_type      = req.currency_type,
        economy_focus      = req.economy_focus,
        military_power     = round(military, 2),
        military_stance    = req.military_stance,
        population         = round(population, 2),
        happiness          = round(happiness, 4),
        resources          = round(resources, 2),
        resource_types     = resource_types,
        diplomacy_score    = round(diplomacy, 4),
        rivals             = rivals,
        active_crises      = active_crises,
        budget_spent       = req.budget,
        total_coins_used   = total_coins,
    )
