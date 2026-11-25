
from decimal import Decimal

import pytest

from cc_rewards_optimizer.calculator import (
    calculate_category_rewards,
    calculate_card_rewards,
    calculate_net_rewards,
)
from cc_rewards_optimizer.models import CreditCard, RewardCategory, RewardRule


def test_calculate_category_rewards_below_cap():
    result = calculate_category_rewards(
        spending=Decimal("1000"),
        reward_rate=Decimal("0.03"),
        annual_spending_cap=Decimal("6000"),
    )

    assert result == Decimal("30.00")


def test_calculate_category_rewards_above_cap():
    result = calculate_category_rewards(
        spending=Decimal("8000"),
        reward_rate=Decimal("0.03"),
        annual_spending_cap=Decimal("6000"),
        base_reward_rate=Decimal("0.01"),
    )

    assert result == Decimal("200.00")


def test_calculate_category_rewards_without_cap():
    result = calculate_category_rewards(
        spending=Decimal("5000"),
        reward_rate=Decimal("0.02"),
    )

    assert result == Decimal("100.00")


def test_calculate_category_rewards_rejects_negative_spending():
    with pytest.raises(ValueError):
        calculate_category_rewards(
            spending=Decimal("-100"),
            reward_rate=Decimal("0.03"),
        )


def test_calculate_card_rewards():
    card = CreditCard(
        name="Everyday Rewards",
        annual_fee=Decimal("95.00"),
        reward_rules=[
            RewardRule(
                RewardCategory.RESTAURANTS,
                Decimal("0.03"),
                Decimal("6000"),
            ),
            RewardRule(
                RewardCategory.GROCERIES,
                Decimal("0.02"),
            ),
        ],
    )

    spending = {
        RewardCategory.RESTAURANTS: Decimal("8000"),
        RewardCategory.GROCERIES: Decimal("6000"),
    }

    result = calculate_card_rewards(card, spending)

    assert result == Decimal("300.00")


def test_calculate_net_rewards():
    card = CreditCard(
        name="Everyday Rewards",
        annual_fee=Decimal("95.00"),
        reward_rules=[
            RewardRule(
                RewardCategory.RESTAURANTS,
                Decimal("0.03"),
                Decimal("6000"),
                Decimal("0.01"),
            ),
            RewardRule(
                RewardCategory.GROCERIES,
                Decimal("0.02"),
            ),
        ],
    )

    spending = {
        RewardCategory.RESTAURANTS: Decimal("8000"),
        RewardCategory.GROCERIES: Decimal("6000"),
    }

    result = calculate_net_rewards(card, spending)

    assert result == Decimal("225.00")


def test_calculate_category_rewards_exactly_at_cap():
    result = calculate_category_rewards(
        spending=Decimal("6000"),
        reward_rate=Decimal("0.03"),
        annual_spending_cap=Decimal("6000"),
        base_reward_rate=Decimal("0.01"),
    )

    assert result == Decimal("180.00")


def test_calculate_category_rewards_zero_spending():
    result = calculate_category_rewards(
        spending=Decimal("0"),
        reward_rate=Decimal("0.03"),
        annual_spending_cap=Decimal("6000"),
        base_reward_rate=Decimal("0.01"),
    )

    assert result == Decimal("0.00")


def test_calculate_card_rewards_missing_category():
    card = CreditCard(
        name="Everyday Rewards",
        annual_fee=Decimal("95.00"),
        reward_rules=[
            RewardRule(
                RewardCategory.RESTAURANTS,
                Decimal("0.03"),
            ),
            RewardRule(
                RewardCategory.GROCERIES,
                Decimal("0.02"),
            ),
        ],
    )

    spending = {
        RewardCategory.RESTAURANTS: Decimal("1000"),
    }

    result = calculate_card_rewards(card, spending)

    assert result == Decimal("30.00")