from dataclasses import dataclass
from enum import Enum


class RewardCategory(Enum):
    RESTAURANTS = "restaurants"
    GROCERIES = "groceries"
    GAS = "gas"
    TRAVEL = "travel"
    OTHER = "other"



@dataclass
class RewardRule:
    category: RewardCategory
    reward_rate: float
    annual_spending_cap: float | None = None

@dataclass
class CreditCard:
    name: str
    annual_fee: float
    reward_rules: list[RewardRule]