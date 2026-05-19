from pathlib import Path

import pandas as pd


RAW_PATH = Path("data/raw/events.csv")
CLEAN_PATH = Path("data/clean/events.csv")
VALID_EVENT_TYPES = ["click", "login", "purchase", "scroll", "view"]


def main():
    events = pd.read_csv(RAW_PATH)

    events = events.dropna()

    events["timestamp"] = pd.to_datetime(events["timestamp"], format="mixed", errors="coerce")
    events["duration_seconds"] = pd.to_numeric(events["duration_seconds"], errors="coerce")

    valid_rows = (
        events["event_type"].isin(VALID_EVENT_TYPES)
        & events["timestamp"].notna()
        & events["duration_seconds"].gt(0)
    )
    events = events.loc[valid_rows].copy()

    events["duration_seconds"] = events["duration_seconds"].astype("int64")
    events["timestamp"] = events["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(CLEAN_PATH, index=False)


if __name__ == "__main__":
    main()
