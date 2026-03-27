"""
institution.py — World Bank, UN, Trade Unions
"""

from pydantic import BaseModel, Field


class WorldBank(BaseModel):
    world_id:           str
    total_reserves:     float = 50000.0
    active_loans:       dict[str, float] = Field(default_factory=dict)  # country_id: amount
    loan_interest_rate: float = 0.08
    board_members:      list[str] = Field(default_factory=list)         # top 3 GDP countries


class UnitedNations(BaseModel):
    world_id:       str
    member_ids:     list[str] = Field(default_factory=list)
    veto_holders:   list[str] = Field(default_factory=list)   # top 5 military
    resolutions:    list[str] = Field(default_factory=list)
    sanctions:      dict[str, str] = Field(default_factory=dict)  # country_id: reason


class TradeUnion(BaseModel):
    union_id:       str
    union_name:     str
    member_ids:     list[str] = Field(default_factory=list)
    trade_bonus:    float = 0.15     # 15% cheaper trade within bloc
    shared_currency: bool = False
