"""
crisis.py — Crisis and Rivalry definitions
Each crisis gives bonus coins but adds starting penalties.
"""

from enum import Enum
from dataclasses import dataclass


class CrisisType(str, Enum):
    ECONOMIC_COLLAPSE     = "economic_collapse"
    CIVIL_WAR             = "civil_war"
    NATURAL_DISASTER      = "natural_disaster"
    OCCUPATION_RESISTANCE = "occupation_resistance"
    RESOURCE_CURSE        = "resource_curse"
    BRAIN_DRAIN           = "brain_drain"
    PLAGUE                = "plague"
    REVOLUTION            = "revolution"


class RivalryIntensity(str, Enum):
    COLD      = "cold"       # diplomatic tension only
    MODERATE  = "moderate"   # trade sanctions, proxy conflicts
    HOT       = "hot"        # open hostility, war likely


@dataclass
class CrisisDefinition:
    crisis_type:     CrisisType
    label:           str
    description:     str
    bonus_coins:     int
    happiness_penalty:   float   # subtracted from starting happiness
    military_penalty:    float   # multiplier on starting military (e.g. 0.7 = 30% weaker)
    economy_penalty:     float   # multiplier on starting GDP
    special_note:        str


@dataclass
class RivalryDefinition:
    intensity:       RivalryIntensity
    label:           str
    bonus_coins:     int
    happiness_penalty:   float
    description:     str


# ── Crisis catalogue ──────────────────────────────────────────────────────────

CRISIS_CATALOGUE: dict[CrisisType, CrisisDefinition] = {

    CrisisType.ECONOMIC_COLLAPSE: CrisisDefinition(
        crisis_type       = CrisisType.ECONOMIC_COLLAPSE,
        label             = "Economic Collapse",
        description       = "Your treasury is in ruins. Debt is high, currency is weak.",
        bonus_coins       = 300,
        happiness_penalty = 0.15,
        military_penalty  = 1.0,
        economy_penalty   = 0.55,
        special_note      = "World Bank loans are easier but come with harsh conditions.",
    ),

    CrisisType.CIVIL_WAR: CrisisDefinition(
        crisis_type       = CrisisType.CIVIL_WAR,
        label             = "Civil War",
        description       = "Two factions are tearing your country apart from within.",
        bonus_coins       = 350,
        happiness_penalty = 0.25,
        military_penalty  = 0.6,
        economy_penalty   = 0.65,
        special_note      = "Win the civil war to unify population and get a massive loyalty bonus.",
    ),

    CrisisType.NATURAL_DISASTER: CrisisDefinition(
        crisis_type       = CrisisType.NATURAL_DISASTER,
        label             = "Natural Disaster",
        description       = "A recent earthquake/flood wiped out infrastructure.",
        bonus_coins       = 250,
        happiness_penalty = 0.10,
        military_penalty  = 0.9,
        economy_penalty   = 0.70,
        special_note      = "International sympathy gives diplomatic bonus. Aid flows in faster.",
    ),

    CrisisType.OCCUPATION_RESISTANCE: CrisisDefinition(
        crisis_type       = CrisisType.OCCUPATION_RESISTANCE,
        label             = "Occupation Resistance",
        description       = "A stronger nation controls your land. You operate in the shadows.",
        bonus_coins       = 500,
        happiness_penalty = 0.20,
        military_penalty  = 0.3,
        economy_penalty   = 0.50,
        special_note      = "Hardest mode. If you break free, your nation becomes a global symbol.",
    ),

    CrisisType.RESOURCE_CURSE: CrisisDefinition(
        crisis_type       = CrisisType.RESOURCE_CURSE,
        label             = "Resource Curse",
        description       = "You are rich in oil/minerals but everyone wants a piece of you.",
        bonus_coins       = 400,
        happiness_penalty = 0.10,
        military_penalty  = 0.85,
        economy_penalty   = 1.0,
        special_note      = "Constant coup risk. Foreign interference is high from turn one.",
    ),

    CrisisType.BRAIN_DRAIN: CrisisDefinition(
        crisis_type       = CrisisType.BRAIN_DRAIN,
        label             = "Brain Drain",
        description       = "Your educated class is fleeing abroad. Innovation is stalling.",
        bonus_coins       = 200,
        happiness_penalty = 0.08,
        military_penalty  = 0.95,
        economy_penalty   = 0.80,
        special_note      = "Diaspora abroad sends remittances. Can be reversed with education investment.",
    ),

    CrisisType.PLAGUE: CrisisDefinition(
        crisis_type       = CrisisType.PLAGUE,
        label             = "Plague / Epidemic",
        description       = "A disease is spreading. Population productivity is crashing.",
        bonus_coins       = 280,
        happiness_penalty = 0.20,
        military_penalty  = 0.75,
        economy_penalty   = 0.72,
        special_note      = "Solve it fast and become a global medical research hub.",
    ),

    CrisisType.REVOLUTION: CrisisDefinition(
        crisis_type       = CrisisType.REVOLUTION,
        label             = "Ideological Revolution",
        description       = "Government just flipped. Old loyalists are fighting back.",
        bonus_coins       = 320,
        happiness_penalty = 0.12,
        military_penalty  = 0.70,
        economy_penalty   = 0.75,
        special_note      = "Your new ideology shapes every future policy decision.",
    ),
}


# ── Rivalry catalogue ─────────────────────────────────────────────────────────

RIVALRY_CATALOGUE: dict[RivalryIntensity, RivalryDefinition] = {

    RivalryIntensity.COLD: RivalryDefinition(
        intensity         = RivalryIntensity.COLD,
        label             = "Cold Rivalry",
        bonus_coins       = 100,
        happiness_penalty = 0.03,
        description       = "Diplomatic tension, propaganda, espionage. No open conflict yet.",
    ),

    RivalryIntensity.MODERATE: RivalryDefinition(
        intensity         = RivalryIntensity.MODERATE,
        label             = "Moderate Rivalry",
        bonus_coins       = 200,
        happiness_penalty = 0.08,
        description       = "Trade sanctions, border skirmishes, proxy conflicts in third nations.",
    ),

    RivalryIntensity.HOT: RivalryDefinition(
        intensity         = RivalryIntensity.HOT,
        label             = "Hot Rivalry",
        bonus_coins       = 350,
        happiness_penalty = 0.15,
        description       = "Open hostility. War can break out any turn. Citizens are fearful.",
    ),
}
