"""
car_tax/calculator.py

WHAT THIS FILE DOES:
Implements the actual KRA tax cascade, step by step, as separate small
functions. Each function does exactly one job. This file does NOT touch
the database, the API, or the frontend — it's pure calculation logic,
which makes it easy to test on its own (you can call these functions
directly in a Django shell and check the numbers by hand).

WHERE THESE NUMBERS COME FROM:
Every rate below was read directly out of KRA's own "TEMPLATE 2025" sheet
(inside New-CRSP---July-2025.xlsx), not estimated from a third-party site.
"""
from datetime import date


# ---------------------------------------------------------------------------
# CONSTANTS — every rate KRA applies, taken from the official template.
#
# These are grouped together at the top of the file (not scattered through
# the functions) so that if KRA changes a rate in the future, there is
# exactly ONE place to look.
# ---------------------------------------------------------------------------

IMPORT_DUTY_RATE = 0.35   # flat, applies to all vehicle categories
VAT_RATE = 0.16           # flat
RDL_RATE = 0.02           # Railway Development Levy — % of Customs Value
IDF_RATE = 0.025          # Import Declaration Fee — % of Customs Value

# Excise duty depends on fuel type + engine size. Stored as a list of rules
# checked in order — the first rule that matches wins. This mirrors the
# four car-relevant categories from KRA's template exactly.
#
# NOTE: KRA's template has no separate category for HYBRID vehicles — only
# plain Petrol/Diesel (by cc) and 100% Electric. Until we can confirm this
# with KRA directly, hybrids are treated the same as petrol/diesel of the
# same engine size. This assumption is deliberately visible here (not
# buried), and the calculation result should say so explicitly to the user.
EXCISE_RULES = [
    # (fuel_types this rule applies to, cc_min, cc_max, excise_rate, category_label)
    (["ELECTRIC"], None, None, 0.10, "100% Electric"),
    (["PETROL", "DIESEL", "HYBRID"], 0, 1500, 0.20, "Engine up to 1500cc"),
    (["PETROL", "HYBRID"], 1500, 3000, 0.25, "Petrol engine 1501cc–3000cc"),
    (["DIESEL"], 1500, 2500, 0.25, "Diesel engine 1501cc–2500cc"),
    (["PETROL", "HYBRID"], 3000, None, 0.35, "Petrol engine above 3000cc"),
    (["DIESEL"], 2500, None, 0.35, "Diesel engine above 2500cc"),
]

# Depreciation bands for DIRECT IMPORTS, based on Year of Manufacture.
# A vehicle 1 year old or newer isn't listed in KRA's table at all, which
# we interpret as 0% depreciation (full CRSP value counts as Customs Value).
DEPRECIATION_BANDS = [
    # (age_min_years, age_max_years, depreciation_pct)
    (0, 1, 0.00),
    (1, 2, 0.20),
    (2, 3, 0.30),
    (3, 4, 0.40),
    (4, 5, 0.50),
    (5, 6, 0.55),
    (6, 7, 0.60),
    (7, 8, 0.65),
]

MAX_IMPORT_AGE_YEARS = 8  # Kenya's hard cutoff — cars older than this
                           # cannot be imported at all.


class CalculationError(Exception):
    """
    Raised whenever we can't safely calculate a result — e.g. the vehicle
    is too old to import, or no excise rule matches. We raise a clear
    error rather than silently returning a wrong number.
    """
    pass


# ---------------------------------------------------------------------------
# STEP FUNCTIONS — one per stage of the cascade
# ---------------------------------------------------------------------------

def get_vehicle_age_years(year_of_manufacture: int, as_of: date = None) -> int:
    """
    Step 0: figure out how old the vehicle is, in whole years, based on
    Year of Manufacture (confirmed as the correct basis for direct imports
    from KRA's own template).
    """
    as_of = as_of or date.today()
    age = as_of.year - year_of_manufacture
    return max(age, 0)


def get_depreciation_pct(age_years: int) -> float:
    """
    Step 1: look up how much the CRSP value should be depreciated, based
    on the vehicle's age, using KRA's official band table above.
    """
    for age_min, age_max, pct in DEPRECIATION_BANDS:
        if age_min < age_years <= age_max or (age_years == 0 and age_min == 0):
            return pct
    # If we get here, the vehicle is older than 8 years — should already
    # have been blocked earlier, but we double-check here too.
    raise CalculationError(
        f"No depreciation band found for a vehicle {age_years} years old. "
        f"Kenya does not permit importing vehicles older than {MAX_IMPORT_AGE_YEARS} years."
    )


def get_excise_rate(fuel_type: str, engine_cc: int) -> tuple[float, str]:
    """
    Step 3 (used after import duty is calculated): look up the excise
    duty rate for this vehicle's fuel type and engine size.

    Returns a tuple of (rate, category_label) — we return the label too
    so the calculation breakdown can show the user WHICH category their
    vehicle was matched to, not just the resulting number.
    """
    fuel_type = fuel_type.upper()

    for fuel_list, cc_min, cc_max, rate, label in EXCISE_RULES:
        if fuel_type not in fuel_list:
            continue
        if fuel_type == "ELECTRIC":
            return rate, label  # electric vehicles skip the cc check entirely
        if engine_cc is None:
            continue  # can't match a cc-based rule without a cc value
        lower_ok = cc_min is None or engine_cc > cc_min
        upper_ok = cc_max is None or engine_cc <= cc_max
        if lower_ok and upper_ok:
            return rate, label

    raise CalculationError(
        f"No excise duty rule matched fuel type '{fuel_type}' with engine "
        f"size {engine_cc}cc. This vehicle may need manual assessment."
    )


def calculate_import_tax(crsp_value: float, fuel_type: str, engine_cc: int,
                          year_of_manufacture: int) -> dict:
    """
    Runs the FULL cascade, step by step, and returns every intermediate
    number — not just the final total. This is what powers the "show your
    working" breakdown on the frontend.
    """
    age_years = get_vehicle_age_years(year_of_manufacture)

    if age_years > MAX_IMPORT_AGE_YEARS:
        raise CalculationError(
            f"This vehicle is {age_years} years old. Kenya does not permit "
            f"importing vehicles older than {MAX_IMPORT_AGE_YEARS} years."
        )

    # --- Step 1: Depreciation -> Customs Value -------------------------
    depreciation_pct = get_depreciation_pct(age_years)
    customs_value = round(crsp_value * (1 - depreciation_pct), 2)

    # --- Step 2: Import Duty --------------------------------------------
    import_duty_amount = round(customs_value * IMPORT_DUTY_RATE, 2)

    # --- Step 3: Excise Duty (on Customs Value + Import Duty) ----------
    excise_rate, excise_category = get_excise_rate(fuel_type, engine_cc)
    excise_base = customs_value + import_duty_amount
    excise_amount = round(excise_base * excise_rate, 2)

    # --- Step 4: VAT (on Customs Value + Import Duty + Excise) ---------
    vat_base = customs_value + import_duty_amount + excise_amount
    vat_amount = round(vat_base * VAT_RATE, 2)

    # --- Step 5: Flat fees, both based on Customs Value -----------------
    rdl_amount = round(customs_value * RDL_RATE, 2)
    idf_amount = round(customs_value * IDF_RATE, 2)

    total_tax_payable = round(
        import_duty_amount + excise_amount + vat_amount + rdl_amount + idf_amount, 2
    )

    # We return every step, in order, as a list — this is what the
    # frontend will loop over to display the breakdown.
    return {
        "vehicle_age_years": age_years,
        "hybrid_assumption_applied": fuel_type.upper() == "HYBRID",
        "steps": [
            {"label": "CRSP (base value)", "amount": crsp_value},
            {"label": f"Customs Value (after {depreciation_pct*100:.0f}% depreciation, age {age_years} yrs)", "amount": customs_value},
            {"label": f"Import Duty ({IMPORT_DUTY_RATE*100:.0f}%)", "amount": import_duty_amount},
            {"label": f"Excise Duty ({excise_rate*100:.0f}% — {excise_category})", "amount": excise_amount},
            {"label": f"VAT ({VAT_RATE*100:.0f}%)", "amount": vat_amount},
            {"label": f"RDL ({RDL_RATE*100:.1f}%)", "amount": rdl_amount},
            {"label": f"IDF ({IDF_RATE*100:.1f}%)", "amount": idf_amount},
            {"label": "TOTAL TAX PAYABLE", "amount": total_tax_payable},
        ],
        "total_tax_payable": total_tax_payable,
    }