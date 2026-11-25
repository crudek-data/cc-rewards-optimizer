
from dataclasses import dataclass
from decimal import Decimal
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
    reward_rate: Decimal
    annual_spending_cap: Decimal | None = None
    base_reward_rate: Decimal = Decimal("0")

    def __post_init__(self):
        if self.reward_rate < Decimal("0") or self.reward_rate > Decimal("1"):
            raise ValueError("Reward rate must be between 0% and 100%.")

        if self.base_reward_rate < Decimal("0") or self.base_reward_rate > Decimal("1"):
            raise ValueError("Base reward rate must be between 0% and 100%.")

        if self.annual_spending_cap is not None:
            if self.annual_spending_cap < Decimal("0"):
                raise ValueError("Annual spending cap cannot be negative.")



@dataclass
class CreditCard:
    name: str
    annual_fee: Decimal
    reward_rules: list[RewardRule]

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Credit card name cannot be empty.")

        if self.annual_fee < Decimal("0"):
            raise ValueError("Annual fee cannot be negative.")

        categories = [rule.category for rule in self.reward_rules]

        if len(categories) != len(set(categories)):
            raise ValueError("A credit card cannot have duplicate reward categories.")
