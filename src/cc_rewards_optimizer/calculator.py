
from decimal import Decimal

from cc_rewards_optimizer.models import CreditCard, RewardCategory


def calculate_category_rewards(
    spending: Decimal,
    reward_rate: Decimal,
    annual_spending_cap: Decimal | None = None,
) -> Decimal:
    """Calculate rewards earned for a spending category."""

    if spending < Decimal("0"):
        raise ValueError("Spending cannot be negative.")

    if reward_rate < Decimal("0"):
        raise ValueError("Reward rate cannot be negative.")

    if annual_spending_cap is not None:
        if annual_spending_cap < Decimal("0"):
            raise ValueError("Annual spending cap cannot be negative.")

        eligible_spending = min(spending, annual_spending_cap)
    else:
        eligible_spending = spending

    return eligible_spending * reward_rate


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
