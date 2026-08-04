"""
car_tax/data.py

WHAT THIS FILE DOES:
Loads the KRA CRSP spreadsheet into memory ONE TIME when the server starts
(or on first request), cleans it, and keeps it cached in memory. Every
search just filters the already-cleaned data — no re-reading the file,
no re-cleaning, on every request.

WHY NO DATABASE:
KRA only updates this spreadsheet every year or two. There's no need for
the complexity of a database table for data that changes this rarely.
When KRA releases a new CRSP file, we just replace the .xlsx file in this
folder and redeploy — that's the entire "update" process.
"""
import re
from pathlib import Path

import pandas as pd

# The spreadsheet file lives right next to this Python file, inside
# car_tax/data/. Path(__file__).parent finds "wherever this file is",
# so this works the same on your machine and on Railway.
FILE_PATH = Path(__file__).parent / "data" / "New-CRSP---July-2025.xlsx"
SHEET_NAME = "M.Vehicle CRSP July 2025"

# ---------------------------------------------------------------------------
# FUEL TYPE NORMALIZATION
#
# The raw KRA file spells fuel types inconsistently — e.g. "GASOLINE" vs
# "PETROL", " DIESEL" (with a leading space), "DEISEL" (typo), "DI ESEL"
# (typo with a stray space), "ELECCTRIC" (typo), etc.
#
# Rather than trying to match every possible typo everywhere we search,
# we convert every raw value to ONE of these fixed categories, ONCE, when
# the data is first loaded. Every other part of the app only ever deals
# with these five clean values.
# ---------------------------------------------------------------------------
FUEL_PETROL = "PETROL"
FUEL_DIESEL = "DIESEL"
FUEL_HYBRID = "HYBRID"
FUEL_ELECTRIC = "ELECTRIC"
FUEL_UNKNOWN = "UNKNOWN"   # for blank cells or rows where the fuel column
                           # accidentally contains a number (a data-entry
                           # error we found in a couple of rows)

# A couple of typos are "letter transpositions" rather than just extra
# spaces (e.g. "DEISEL" instead of "DIESEL") — those need an explicit
# lookup rather than a pattern match.
FUEL_TYPO_ALIASES = {
    "DEISEL": FUEL_DIESEL,
}

# This dictionary acts as our in-memory "database" — loaded once, reused
# on every request. Using a module-level dict (rather than a variable)
# means it survives between function calls as long as the server process
# is running.
_cache = {}


def _normalize_fuel(raw) -> str:
    """
    Takes whatever messy string (or blank, or number) was in the Fuel
    column, and returns one of our five clean categories.
    """
    # Handle blank cells (pandas represents these as NaN, "Not a Number")
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return FUEL_UNKNOWN

    s = str(raw).strip().upper()          # remove leading/trailing spaces
    s_nospace = s.replace(" ", "")        # remove ALL spaces — this alone
                                           # fixes "DI ESEL" -> "DIESEL"
                                           # and "DIESE L" -> "DIESEL"

    # Check our manual typo list first (catches "DEISEL")
    if s_nospace in FUEL_TYPO_ALIASES:
        return FUEL_TYPO_ALIASES[s_nospace]

    # A couple of rows had a plain number in the Fuel column by mistake —
    # if there are no letters at all, we can't guess the fuel type.
    if not re.search(r"[A-Z]", s):
        return FUEL_UNKNOWN

    # Order matters here: check hybrid/electric combinations BEFORE plain
    # petrol/diesel, so e.g. "PETROL/ELECTRIC" gets caught as HYBRID and
    # not wrongly matched as PETROL.
    if "HYBRID" in s_nospace or "PLUGIN" in s_nospace or "PLUG-IN" in s:
        return FUEL_HYBRID
    if "PETROL/ELECTRIC" in s or "ELECTRIC/PETROL" in s:
        return FUEL_HYBRID
    if "ELEC" in s_nospace:               # catches ELECTRIC, ELECCTRIC,
                                           # ELECTRIC(EV)
        return FUEL_ELECTRIC
    if "DIES" in s_nospace:               # catches DIESEL and its typos
        return FUEL_DIESEL
    if "GASOLINE" in s or "PETROL" in s:
        return FUEL_PETROL

    return FUEL_UNKNOWN


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs every cleaning step on the raw spreadsheet data:
    - fixes column names (the real file has newlines inside some headers)
    - drops rows missing essential info (no Make, Model, or price)
    - converts engine capacity to a real number where possible
    - normalizes fuel type using the function above
    """
    df = df.copy()

    # The raw column names have embedded newlines, e.g. "Engine \nCapacity"
    # — this line strips those so we get clean, predictable column names.
    df.columns = [str(c).replace("\n", " ").strip() for c in df.columns]
    df = df.rename(columns={"Engine  Capacity": "Engine Capacity"})

    # A row with no Make, Model, or CRSP price is unusable — drop it.
    df = df.dropna(subset=["Make", "Model", "CRSP (KES.)"])

    df["Make"] = df["Make"].astype(str).str.strip()
    df["Model"] = df["Model"].astype(str).str.strip()

    # Convert engine capacity to a number. errors="coerce" means: if it
    # can't be converted (e.g. it says "63 kWh" for an electric car),
    # put NaN instead of crashing. We handle that NaN case explicitly
    # later, rather than letting it cause silent bugs.
    df["Engine Capacity (cc)"] = pd.to_numeric(df["Engine Capacity"], errors="coerce")

    # Keep the ORIGINAL fuel text too (useful for debugging / display),
    # then overwrite the working column with the cleaned version.
    df["Fuel (raw)"] = df["Fuel"]
    df["Fuel"] = df["Fuel"].apply(_normalize_fuel)

    df["CRSP (KES.)"] = pd.to_numeric(df["CRSP (KES.)"], errors="coerce")
    df = df.dropna(subset=["CRSP (KES.)"])

    return df.reset_index(drop=True)


def load_data(force_reload: bool = False) -> pd.DataFrame:
    """
    Returns the cleaned CRSP dataset.

    The first time this is called, it reads the Excel file from disk and
    cleans it — this takes a moment. Every call after that just returns
    the already-cleaned data from memory, which is instant.

    force_reload=True skips the cache — useful if you update the Excel
    file and want to reload it without restarting the whole server.
    """
    if force_reload or "df" not in _cache:
        raw = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME, header=1)
        _cache["df"] = _clean(raw)
    return _cache["df"]


def reset_cache():
    """Clears the cache. Next load_data() call will re-read the file."""
    _cache.clear()


def search_vehicles(make: str = "", model_keyword: str = "", fuel: str = "",
                     engine_cc: int = None, cc_tolerance: int = 50) -> list[dict]:
    """
    Searches the cleaned dataset and returns matching vehicles as a plain
    list of dictionaries — ready to be converted straight to JSON for
    the frontend.

    IMPORTANT: for electric vehicles, we deliberately SKIP the engine_cc
    filter. Their "Engine Capacity" field is often not a cc number at all
    (e.g. "63 kWh" or blank), so filtering by cc would wrongly hide them.
    """
    df = load_data()

    # Start with "match everything", then narrow down with each filter
    # that was actually provided.
    mask = pd.Series(True, index=df.index)

    if make:
        mask &= df["Make"].str.upper() == make.strip().upper()

    if model_keyword:
        mask &= df["Model"].str.upper().str.contains(
            model_keyword.strip().upper(), na=False, regex=False
        )

    fuel_normalized = None
    if fuel:
        # Normalize the SEARCH INPUT the same way we normalized the data,
        # so searching "PETROL" correctly matches rows stored as "GASOLINE".
        fuel_normalized = _normalize_fuel(fuel)
        mask &= df["Fuel"] == fuel_normalized

    is_electric_search = fuel_normalized == FUEL_ELECTRIC
    if engine_cc is not None and not is_electric_search:
        mask &= df["Engine Capacity (cc)"].between(
            engine_cc - cc_tolerance, engine_cc + cc_tolerance
        )

    results = df[mask]

    # Convert each matching row into a plain dictionary. This is the
    # shape the frontend will actually receive as JSON.
    def _clean_value(value):
        """
        Converts a pandas NaN (which can't be sent as JSON) into a plain
        Python None. Used on every field before it goes into the response,
        so we never accidentally try to send NaN to the frontend.
        """
        if isinstance(value, float) and pd.isna(value):
            return None
        return value


    # ... inside search_vehicles(), replace the existing return statement with:

    return [
        {
            "make": row["Make"],
            "model": row["Model"],
            "transmission": _clean_value(row.get("Transmission")),
            "engine_cc": (
                None if pd.isna(row["Engine Capacity (cc)"])
                else int(row["Engine Capacity (cc)"])
            ),
            "engine_capacity_raw": _clean_value(row["Engine Capacity"]),
            "fuel": row["Fuel"],
            "crsp_value": float(row["CRSP (KES.)"]),
        }
        for _, row in results.iterrows()
    ]