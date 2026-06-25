"""Core budget transaction operations."""

import csv
from pathlib import Path

TRANSACTION_FIELDS: tuple[str, ...] = (
    "date",
    "type",
    "category",
    "description",
    "amount",
    "memo",
)


def add_transaction(
    transactions: list[dict[str, object]],
    transaction: dict[str, object],
) -> list[dict[str, object]]:
    """Return transactions with a new transaction added."""
    normalized_transaction = {
        field: transaction[field] for field in TRANSACTION_FIELDS
    }
    return [*transactions, normalized_transaction]


def get_balance(transactions: list[dict[str, object]]) -> float:
    """Return the sum of income and expense amounts."""
    total = sum(
        int(transaction["amount"]) for transaction in transactions
    )
    return float(total)


def filter_by_category(
    transactions: list[dict[str, object]],
    category: str,
) -> list[dict[str, object]]:
    """Return transactions matching a category, ignoring case."""
    target_category = category.casefold()
    return [
        dict(transaction)
        for transaction in transactions
        if str(transaction["category"]).casefold() == target_category
    ]


def load_transactions_from_csv(path: str | Path) -> list[dict[str, object]]:
    """Load transactions from a CSV file."""
    csv_path = Path(path)
    with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        return [
            {**row, "amount": int(row["amount"])}
            for row in csv.DictReader(csv_file)
        ]


def monthly_summary(
    transactions: list[dict[str, object]],
) -> dict[str, dict[str, int]]:
    """Return monthly income, expense, and net totals."""
    summary: dict[str, dict[str, int]] = {}
    for transaction in transactions:
        month = str(transaction["date"])[:7]
        amount = int(transaction["amount"])
        summary.setdefault(month, {"income": 0, "expense": 0, "net": 0})
        if amount > 0:
            summary[month]["income"] += amount
        else:
            summary[month]["expense"] += amount
        summary[month]["net"] = (
            summary[month]["income"] + summary[month]["expense"]
        )
    return summary
