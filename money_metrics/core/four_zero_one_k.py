"""Utilities for managing 401(k) datasets.

The :class:`FourZeroOneK` class stores monthly contribution data and the
resulting account balance after applying a growth rate.  The dataset is stored
as a list of dictionaries so it can be serialised directly to JSON for
inclusion in an :class:`~money_metrics.core.profile.AppProfile`.

Inputs such as the monthly contribution and growth rate are kept alongside the
output balance, allowing the data to be graphed or displayed in tabular form by
the UI.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Iterable


@dataclass
class Entry:
    """Single month of 401(k) data."""

    month: int
    contribution: float
    growth_rate: float
    balance: float


class FourZeroOneK:
    """Simple 401(k) tracker with add/modify/delete operations.

    The internal ``entries`` list is maintained in chronological order. Each
    operation that alters the sequence will recompute the balance of the
    affected month and all subsequent months.
    """

    def __init__(self, entries: Iterable[Dict[str, float]] | None = None):
        self.entries: List[Entry] = []
        if entries:
            for item in entries:
                self.entries.append(Entry(**item))
            # ensure balances are consistent when loading external data
            self._recalculate_from(0)

    # ------------------------------------------------------------------
    def add_month(self, contribution: float, growth_rate: float) -> None:
        """Append a new month to the dataset."""

        prev_balance = self.entries[-1].balance if self.entries else 0.0
        balance = (prev_balance + contribution) * (1 + growth_rate)
        self.entries.append(
            Entry(len(self.entries) + 1, contribution, growth_rate, balance)
        )

    def delete_month(self, month: int) -> None:
        """Remove a month by index (1-based)."""

        index = month - 1
        if not (0 <= index < len(self.entries)):
            raise IndexError("month out of range")
        del self.entries[index]
        self._recalculate_from(index)

    def modify_month(
        self,
        month: int,
        *,
        contribution: float | None = None,
        growth_rate: float | None = None,
    ) -> None:
        """Modify contribution and/or growth rate for a month."""

        index = month - 1
        if not (0 <= index < len(self.entries)):
            raise IndexError("month out of range")

        entry = self.entries[index]
        if contribution is not None:
            entry.contribution = contribution
        if growth_rate is not None:
            entry.growth_rate = growth_rate
        self.entries[index] = entry
        self._recalculate_from(index)

    # ------------------------------------------------------------------
    def to_dict(self) -> List[Dict[str, float]]:
        """Return the dataset as a list of serialisable dicts."""

        return [asdict(e) for e in self.entries]

    # ------------------------------------------------------------------
    def _recalculate_from(self, start: int) -> None:
        """Recompute balances starting at ``start`` index."""

        prev_balance = self.entries[start - 1].balance if start > 0 else 0.0
        for i in range(start, len(self.entries)):
            entry = self.entries[i]
            entry.month = i + 1
            entry.balance = (prev_balance + entry.contribution) * (
                1 + entry.growth_rate
            )
            self.entries[i] = entry
            prev_balance = entry.balance


__all__ = ["FourZeroOneK", "Entry"]

