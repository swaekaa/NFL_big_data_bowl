"""
data_loading.py — Memory-safe loaders for all competition dataset files.

Design principles:
- Small files (players, combine_results, etc.) load fully into memory.
- Medium files (combine_tracking, player_play) load fully but with typed dtypes
  to minimize RAM usage.
- Large files (game_tracking_*) support column selection and optional chunking.
- Every loader logs what it loaded and warns about missing values.
- No data is silently dropped; any filtering is explicit and logged.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Iterator, Optional

import numpy as np
import pandas as pd

# Add project root to sys.path so we can import src.config from notebooks.
_SRC_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SRC_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.config import (
    COMBINE_TRACKING_COLS,
    GAME_TRACKING_COLS,
    PLAYER_PLAY_COLS,
    TRADITIONAL_COMBINE_COLS,
    ALL_RAW_FILES,
    PLAYERS_CSV,
    COMBINE_RESULTS_CSV,
    COMBINE_TRACKING_CSV,
    CAREER_SUCCESSES_CSV,
    PLAYER_PLAY_CSV,
    GAMES_CSV,
    GAME_TRACKING_FILES,
)

log = logging.getLogger(__name__)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _log_load(name: str, df: pd.DataFrame, path: Path) -> None:
    mem_mb = df.memory_usage(deep=True).sum() / 1_048_576
    log.info(
        f"Loaded {name}: {len(df):,} rows × {df.shape[1]} cols | "
        f"{mem_mb:.1f} MB | source: {path.name}"
    )


def _check_missing(df: pd.DataFrame, name: str) -> None:
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        log.warning(f"{name} — columns with missing values:\n{missing.to_string()}")
    else:
        log.info(f"{name} — no missing values detected.")


def _available_cols(requested: list[str], available: list[str], name: str) -> list[str]:
    """Return intersection of requested columns and those actually in the file."""
    result = [c for c in requested if c in available]
    skipped = [c for c in requested if c not in available]
    if skipped:
        log.warning(f"{name}: requested columns not in file (skipped): {skipped}")
    return result


# ── Small Files ───────────────────────────────────────────────────────────────

def load_players(path: Path = PLAYERS_CSV) -> pd.DataFrame:
    """
    Load players.csv fully.
    Asserts nfl_id is unique and non-null.
    """
    _require_file(path, "players.csv")
    df = pd.read_csv(path)
    if "nfl_position" in df.columns and "position" not in df.columns:
        df = df.rename(columns={"nfl_position": "position"})
    _log_load("players", df, path)

    assert "nfl_id" in df.columns, "players.csv must have an 'nfl_id' column"
    assert df["nfl_id"].notna().all(), "players.nfl_id contains null values"
    assert df["nfl_id"].is_unique, "players.nfl_id is not unique — check data"

    _check_missing(df, "players")
    return df


def load_games(path: Path = GAMES_CSV) -> pd.DataFrame:
    """Load games.csv fully."""
    _require_file(path, "games.csv")
    df = pd.read_csv(path)
    _log_load("games", df, path)
    _check_missing(df, "games")
    return df


def load_career_successes(path: Path = CAREER_SUCCESSES_CSV) -> pd.DataFrame:
    """Load player_career_successes.csv fully."""
    _require_file(path, "player_career_successes.csv")
    df = pd.read_csv(path)
    _log_load("career_successes", df, path)
    _check_missing(df, "career_successes")
    return df


def load_combine_results(
    path: Path = COMBINE_RESULTS_CSV,
    cols: Optional[list[str]] = None,
) -> pd.DataFrame:
    """
    Load combine_results.csv.
    Optionally restrict to specific columns (defaults to TRADITIONAL_COMBINE_COLS).
    """
    _require_file(path, "combine_results.csv")
    peek_cols = pd.read_csv(path, nrows=0).columns.tolist()

    if cols is None:
        cols = TRADITIONAL_COMBINE_COLS

    usecols = _available_cols(cols, peek_cols, "combine_results")
    df = pd.read_csv(path, usecols=usecols if usecols else None)

    _log_load("combine_results", df, path)
    _check_missing(df, "combine_results")
    return df


# ── Medium Files ──────────────────────────────────────────────────────────────

def load_combine_tracking(
    path: Path = COMBINE_TRACKING_CSV,
    cols: Optional[list[str]] = None,
    nfl_ids: Optional[list[int]] = None,
    drill_types: Optional[list[str]] = None,
    chunksize: Optional[int] = None,
) -> pd.DataFrame | Iterator[pd.DataFrame]:
    """
    Load combine_tracking.csv.

    Parameters
    ----------
    path : Path
        Path to the CSV.
    cols : list[str] | None
        Columns to load. Defaults to COMBINE_TRACKING_COLS.
    nfl_ids : list[int] | None
        If provided, filter to these players after loading.
    drill_types : list[str] | None
        If provided, filter to these drill_type values after loading.
    chunksize : int | None
        If provided, returns an iterator of DataFrames rather than one frame.
        Each chunk will still be filtered by nfl_ids / drill_types if supplied.

    Returns
    -------
    pd.DataFrame or Iterator[pd.DataFrame]
    """
    _require_file(path, "combine_tracking.csv")
    peek_cols = pd.read_csv(path, nrows=0).columns.tolist()

    if cols is None:
        cols = COMBINE_TRACKING_COLS

    usecols = _available_cols(cols, peek_cols, "combine_tracking")

    dtypes = {
        "x": "float32",
        "y": "float32",
        "s": "float32",
        "a": "float32",
        "dis": "float32",
        "dir": "float32",
        "attempt": "Int16",
    }
    # Only apply dtypes for columns actually being loaded
    dtypes_use = {k: v for k, v in dtypes.items() if k in usecols}

    reader_kwargs = dict(
        usecols=usecols if usecols else None,
        dtype=dtypes_use,
        low_memory=False,
    )

    if chunksize is not None:
        log.info(f"combine_tracking: returning chunked iterator (chunksize={chunksize})")
        return _chunked_filter(
            path, reader_kwargs, chunksize, nfl_ids, drill_types
        )

    df = pd.read_csv(path, **reader_kwargs)
    _log_load("combine_tracking", df, path)

    if nfl_ids is not None:
        before = len(df)
        df = df[df["nfl_id"].isin(nfl_ids)]
        log.info(f"combine_tracking: filtered by nfl_ids — {before:,} → {len(df):,} rows")

    if drill_types is not None:
        before = len(df)
        df = df[df["drill_type"].isin(drill_types)]
        log.info(f"combine_tracking: filtered by drill_types — {before:,} → {len(df):,} rows")

    _check_missing(df, "combine_tracking")
    return df


def _chunked_filter(
    path: Path,
    reader_kwargs: dict,
    chunksize: int,
    nfl_ids: Optional[list[int]],
    drill_types: Optional[list[str]],
) -> Iterator[pd.DataFrame]:
    for chunk in pd.read_csv(path, chunksize=chunksize, **reader_kwargs):
        if nfl_ids is not None:
            chunk = chunk[chunk["nfl_id"].isin(nfl_ids)]
        if drill_types is not None:
            chunk = chunk[chunk["drill_type"].isin(drill_types)]
        if not chunk.empty:
            yield chunk


def load_player_play(
    path: Path = PLAYER_PLAY_CSV,
    cols: Optional[list[str]] = None,
    nfl_ids: Optional[list[int]] = None,
    positions: Optional[list[str]] = None,
) -> pd.DataFrame:
    """
    Load player_play.csv with column selection and optional filtering.

    Parameters
    ----------
    cols : list[str] | None
        Defaults to PLAYER_PLAY_COLS.
    nfl_ids : list[int] | None
        If provided, filter to these players.
    positions : list[str] | None
        If provided, filter to these position codes.
    """
    _require_file(path, "player_play.csv")
    peek_cols = pd.read_csv(path, nrows=0).columns.tolist()

    if cols is None:
        cols = PLAYER_PLAY_COLS

    usecols = _available_cols(cols, peek_cols, "player_play")

    df = pd.read_csv(path, usecols=usecols if usecols else None, low_memory=False)
    _log_load("player_play", df, path)

    if nfl_ids is not None:
        before = len(df)
        df = df[df["nfl_id"].isin(nfl_ids)]
        log.info(f"player_play: filtered by nfl_ids — {before:,} → {len(df):,} rows")

    if positions is not None and "position" in df.columns:
        before = len(df)
        df = df[df["position"].isin(positions)]
        log.info(f"player_play: filtered by positions — {before:,} → {len(df):,} rows")

    _check_missing(df, "player_play")
    return df


# ── Large Files — Game Tracking ───────────────────────────────────────────────

def load_game_tracking(
    season: int,
    cols: Optional[list[str]] = None,
    game_ids: Optional[list] = None,
    nfl_ids: Optional[list[int]] = None,
    chunksize: int = 500_000,
    max_chunks: Optional[int] = None,
) -> pd.DataFrame:
    """
    Load a game tracking CSV for a given season.

    Loads in chunks and filters eagerly to avoid OOM.

    Parameters
    ----------
    season : int
        One of 2023, 2024, 2025.
    cols : list[str] | None
        Columns to load. Defaults to GAME_TRACKING_COLS.
    game_ids : list | None
        If provided, only rows with these game_ids are retained.
    nfl_ids : list[int] | None
        If provided, only rows for these players are retained.
    chunksize : int
        Rows per chunk. Default 500,000.
    max_chunks : int | None
        Cap the number of chunks read (useful for quick exploration).

    Returns
    -------
    pd.DataFrame
        Concatenated, filtered result.
    """
    if season not in GAME_TRACKING_FILES:
        raise ValueError(f"season must be one of {list(GAME_TRACKING_FILES)}. Got: {season}")

    path = GAME_TRACKING_FILES[season]
    _require_file(path, f"game_tracking_{season}.csv")

    peek_cols = pd.read_csv(path, nrows=0).columns.tolist()
    if cols is None:
        cols = GAME_TRACKING_COLS

    usecols = _available_cols(cols, peek_cols, f"game_tracking_{season}")

    dtypes = {
        "x": "float32",
        "y": "float32",
        "s": "float32",
        "a": "float32",
        "dis": "float32",
        "o": "float32",
        "dir": "float32",
    }
    dtypes_use = {k: v for k, v in dtypes.items() if k in usecols}

    chunks = []
    total_rows = 0
    for i, chunk in enumerate(
        pd.read_csv(
            path,
            usecols=usecols if usecols else None,
            dtype=dtypes_use,
            chunksize=chunksize,
            low_memory=False,
        )
    ):
        if max_chunks is not None and i >= max_chunks:
            log.warning(f"game_tracking_{season}: stopped after {max_chunks} chunks.")
            break

        if game_ids is not None:
            chunk = chunk[chunk["game_id"].isin(game_ids)]
        if nfl_ids is not None:
            chunk = chunk[chunk["nfl_id"].isin(nfl_ids)]

        if not chunk.empty:
            chunks.append(chunk)
            total_rows += len(chunk)

        if (i + 1) % 5 == 0:
            log.info(f"game_tracking_{season}: processed {i+1} chunks, {total_rows:,} rows retained")

    if not chunks:
        log.warning(f"game_tracking_{season}: no rows matched filters — returning empty DataFrame")
        return pd.DataFrame(columns=usecols)

    df = pd.concat(chunks, ignore_index=True)
    _log_load(f"game_tracking_{season}", df, path)
    return df


def load_game_tracking_for_players(
    nfl_ids: list[int],
    seasons: Optional[list[int]] = None,
    cols: Optional[list[str]] = None,
    chunksize: int = 500_000,
) -> pd.DataFrame:
    """
    Convenience: load game tracking for a specific set of players across seasons.

    Only loads frames where nfl_id is in the supplied list, which keeps memory
    manageable even for the large 2025 file.
    """
    if seasons is None:
        seasons = [2023, 2024, 2025]

    dfs = []
    for season in seasons:
        path = GAME_TRACKING_FILES[season]
        if not path.exists():
            log.warning(f"game_tracking_{season}.csv not found — skipping.")
            continue
        df = load_game_tracking(
            season=season,
            cols=cols,
            nfl_ids=nfl_ids,
            chunksize=chunksize,
        )
        df["season"] = season
        dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    result = pd.concat(dfs, ignore_index=True)
    log.info(
        f"load_game_tracking_for_players: {len(nfl_ids)} players, "
        f"seasons={seasons}, total rows={len(result):,}"
    )
    return result


# ── Inventory Helper ──────────────────────────────────────────────────────────

def quick_schema(path: Path, n_rows: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read just the head of a CSV and return (head_df, dtypes_df).
    Useful for schema inspection without loading the full file.
    """
    df = pd.read_csv(path, nrows=n_rows, low_memory=False)
    dtypes_df = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.values,
        "sample_value": [df[c].iloc[0] if len(df) > 0 else None for c in df.columns],
    })
    return df, dtypes_df


# ── Internal Helpers ──────────────────────────────────────────────────────────

def _require_file(path: Path, name: str) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}\n"
            f"Place '{name}' in the data/raw/ directory. "
            f"Download from: https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/data"
        )
