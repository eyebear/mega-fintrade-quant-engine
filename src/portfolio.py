from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass
class EqualWeightAllocator:
    """Convert asset-level active signals into portfolio weights."""

    def allocate(self, signal_frame: pd.DataFrame) -> pd.DataFrame:
        active_count = signal_frame.sum(axis=1)
        weights = signal_frame.div(active_count.replace(0.0, pd.NA), axis=0)
        return weights.fillna(0.0)
