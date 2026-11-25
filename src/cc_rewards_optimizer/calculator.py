
from decimal import Decimal

from cc_rewards_optimizer.models import CreditCard, RewardCategory



def calculate_category_rewards(
    spending: Decimal,
    reward_rate: Decimal,
    annual_spending_cap: Decimal | None = None,
    base_reward_rate: Decimal = Decimal("0"),
) -> Decimal:
    """Calculate rewards using a category rate and a base rate above the cap."""

    if spending < Decimal("0"):
        raise ValueError("Spending cannot be negative.")

    if reward_rate < Decimal("0") or reward_rate > Decimal("1"):
        raise ValueError("Reward rate must be between 0% and 100%.")

    if base_reward_rate < Decimal("0") or base_reward_rate > Decimal("1"):
        raise ValueError("Base reward rate must be between 0% and 100%.")

    if annual_spending_cap is None:
        return spending * reward_rate

    if annual_spending_cap < Decimal("0"):
        raise ValueError("Annual spending cap cannot be negative.")

    bonus_eligible_spending = min(spending, annual_spending_cap)
    spending_above_cap = max(
        Decimal("0"),
        spending - annual_spending_cap,
    )

    bonus_rewards = bonus_eligible_spending * reward_rate
    base_rewards = spending_above_cap * base_reward_rate

    return bonus_rewards + base_rewards


def calculate_card_rewards(
    card: CreditCard,
    spending: dict[RewardCategory, Decimal],
) -> Decimal:
    """Calculate total annual rewards earned on a credit card."""

    total_rewards = Decimal("0")

    for rule in card.reward_rules:
        category_spending = spending.get(
            rule.category,
            Decimal("0"),
        )

        category_rewards = calculate_category_rewards(
            spending=category_spending,
            reward_rate=rule.reward_rate,
            annual_spending_cap=rule.annual_spending_cap,
            base_reward_rate=rule.base_reward_rate,
        )

        total_rewards += category_rewards

    return total_rewards


def calculate_net_rewards(
    card: CreditCard,
    spending: dict[RewardCategory, Decimal],
) -> Decimal:
    """Calculate net annual rewards after the annual fee."""

    gross_rewards = calculate_card_rewards(card, spending)

    return gross_rewards - card.annual_fee
