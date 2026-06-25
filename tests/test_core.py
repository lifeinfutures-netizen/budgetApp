from pathlib import Path

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    load_transactions_from_csv,
    monthly_summary,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_add_transaction_increases_length() -> None:
    transactions: list[dict[str, object]] = []
    transaction: dict[str, object] = {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1


def test_add_transaction_stores_negative_expense_amount() -> None:
    transactions: list[dict[str, object]] = []
    transaction: dict[str, object] = {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == -12000


def test_add_transaction_stores_positive_income_amount() -> None:
    transactions: list[dict[str, object]] = []
    transaction: dict[str, object] = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == 3500000


def test_add_transaction_allows_empty_description() -> None:
    transactions: list[dict[str, object]] = []
    transaction: dict[str, object] = {
        "date": "2026-01-10",
        "type": "지출",
        "category": "교통",
        "description": "",
        "amount": -1500,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["description"] == ""


def test_get_balance_returns_zero_for_empty_transactions() -> None:
    assert get_balance([]) == 0.0


def test_get_balance_sums_income_and_expense_amounts() -> None:
    transactions: list[dict[str, object]] = [
        {
            "date": "2026-01-07",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 3500000,
            "memo": "1월급여",
        },
        {
            "date": "2026-01-10",
            "type": "지출",
            "category": "교통",
            "description": "지하철",
            "amount": -1500,
            "memo": "",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "식비",
            "description": "점심식사",
            "amount": -12000,
            "memo": "",
        },
    ]

    assert get_balance(transactions) == 3486500.0


def test_get_balance_matches_step2_transactions_csv() -> None:
    transactions = load_transactions_from_csv(
        PROJECT_ROOT / "data" / "step2_transactions.csv"
    )

    assert get_balance(transactions) == 24285027.0


def test_load_transactions_from_csv_reads_step1_transactions() -> None:
    transactions = load_transactions_from_csv(
        PROJECT_ROOT / "data" / "step1_transactions.csv"
    )

    assert len(transactions) == 10
    assert transactions[0] == {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }
    assert isinstance(transactions[0]["amount"], int)
    assert transactions[1]["memo"] == "1월급여"


def test_filter_by_category_matches_category_case_insensitively() -> None:
    transactions = load_transactions_from_csv(
        PROJECT_ROOT / "data" / "step2_transactions.csv"
    )

    result = filter_by_category(transactions, "의료")

    assert len(result) == 7
    assert all(
        transaction["category"].casefold() == "의료".casefold()
        for transaction in result
    )


def test_filter_by_category_returns_empty_list_for_missing_category() -> None:
    transactions = load_transactions_from_csv(
        PROJECT_ROOT / "data" / "step2_transactions.csv"
    )

    result = filter_by_category(transactions, "없는카테고리")

    assert result == []


def test_filter_by_category_returns_independent_result() -> None:
    transactions = load_transactions_from_csv(
        PROJECT_ROOT / "data" / "step2_transactions.csv"
    )

    result = filter_by_category(transactions, "의료")
    result[0]["memo"] = "changed"

    assert result is not transactions
    assert transactions[1]["memo"] == "카드결제"


def test_monthly_summary_returns_empty_dict_for_empty_transactions() -> None:
    assert monthly_summary([]) == {}


def test_monthly_summary_calculates_income_expense_and_net_by_month() -> None:
    transactions: list[dict[str, object]] = [
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "식비",
            "description": "점심식사",
            "amount": -12000,
            "memo": "",
        },
        {
            "date": "2026-01-07",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 3500000,
            "memo": "1월급여",
        },
        {
            "date": "2026-02-01",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -651009,
            "memo": "카드결제",
        },
    ]

    assert monthly_summary(transactions) == {
        "2026-01": {
            "income": 3500000,
            "expense": -12000,
            "net": 3488000,
        },
        "2026-02": {
            "income": 0,
            "expense": -651009,
            "net": -651009,
        },
    }


def test_monthly_summary_matches_step3_transactions_csv() -> None:
    transactions = load_transactions_from_csv(
        PROJECT_ROOT / "data" / "step3_transactions.csv"
    )

    summary = monthly_summary(transactions)

    assert len(summary) == 15
    assert summary["2025-11"] == {
        "income": 17019996,
        "expense": -801636,
        "net": 16218360,
    }
    assert summary["2026-01"] == {
        "income": 5140637,
        "expense": -1283712,
        "net": 3856925,
    }
