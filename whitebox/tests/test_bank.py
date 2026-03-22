"""White-box unit tests for bank decision paths and edge cases."""

import pytest

from moneypoly.bank import Bank
from moneypoly.player import Player


@pytest.mark.parametrize("amount", [0, 1, 75, 1000])
def test_collect_adds_non_negative_amounts(amount):
    """Collect should increase bank balance for valid non-negative values."""
    bank = Bank()
    start = bank.get_balance()

    bank.collect(amount)

    assert bank.get_balance() == start + amount


@pytest.mark.parametrize("amount", [-1, -50, -999])
def test_collect_ignores_negative_amounts(amount):
    """Negative collect amounts should not reduce bank funds."""
    bank = Bank()
    start = bank.get_balance()

    bank.collect(amount)

    assert bank.get_balance() == start


@pytest.mark.parametrize("amount", [0, -1, -40])
def test_pay_out_non_positive_returns_zero(amount):
    """Non-positive payouts should return 0 and not alter bank balance."""
    bank = Bank()
    start = bank.get_balance()

    paid = bank.pay_out(amount)

    assert paid == 0
    assert bank.get_balance() == start


@pytest.mark.parametrize("amount", [1, 200, 800])
def test_pay_out_reduces_balance_for_valid_amount(amount):
    """Valid payout should deduct the exact amount from bank funds."""
    bank = Bank()
    start = bank.get_balance()

    paid = bank.pay_out(amount)

    assert paid == amount
    assert bank.get_balance() == start - amount


def test_pay_out_raises_when_funds_are_insufficient():
    """Payout larger than reserves should raise ValueError."""
    bank = Bank()
    with pytest.raises(ValueError):
        bank.pay_out(bank.get_balance() + 1)


@pytest.mark.parametrize("amount", [0, -10])
def test_give_loan_ignores_non_positive_amounts(amount):
    """Loan requests with non-positive amounts should do nothing."""
    bank = Bank()
    player = Player("P")
    start_bank = bank.get_balance()
    start_player = player.balance

    bank.give_loan(player, amount)

    assert bank.get_balance() == start_bank
    assert player.balance == start_player
    assert bank.loan_count() == 0


@pytest.mark.parametrize("amount", [1, 150, 700])
def test_give_loan_reduces_bank_funds_and_credits_player(amount):
    """Emergency loan should reduce bank funds and increase player balance."""
    bank = Bank()
    player = Player("P")
    start_bank = bank.get_balance()
    start_player = player.balance

    bank.give_loan(player, amount)

    assert bank.get_balance() == start_bank - amount
    assert player.balance == start_player + amount
    assert bank.loan_count() == 1


def test_total_loans_and_count_accumulate_multiple_loans():
    """Loan statistics should reflect all issued loans."""
    bank = Bank()
    p1 = Player("A")
    p2 = Player("B")

    bank.give_loan(p1, 40)
    bank.give_loan(p2, 60)

    assert bank.loan_count() == 2
    assert bank.total_loans_issued() == 100
