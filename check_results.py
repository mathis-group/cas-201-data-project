"""Sanity-check results.json before you submit.

Run from the repository root:   python check_results.py

This checks FORMAT only: the right keys are filled in, values have the right
type, and numbers are physically possible. Passing does NOT mean your answers
are correct, and failing a range check usually means a units or masking slip.
"""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OPTIONS = {"A": "A_hot", "B": "B_eia", "C": "C_medsl"}
errors = []


def err(msg):
    errors.append(msg)
    print(f"  FAIL  {msg}")


def number(sec, key, lo, hi, integer=False):
    v = sec.get(key)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or (isinstance(v, float) and math.isnan(v)):
        return err(f"{key} must be a number, got {v!r}")
    if integer and not float(v).is_integer():
        return err(f"{key} must be a whole number, got {v!r}")
    if not lo <= v <= hi:
        return err(f"{key} = {v} is outside the possible range [{lo}, {hi}]; check units and missing-value flags")
    print(f"  ok    {key} = {v}")


def check_hot(s):
    number(s, "ph_trend_per_decade", -0.5, 0.5)
    number(s, "ph_trend_stderr_per_decade", 1e-7, 0.5)
    number(s, "n_surface_ph_samples", 10, 97444, integer=True)
    number(s, "sep_minus_apr_mean_surface_ph", -1, 1)


def check_eia(s):
    number(s, "april_min_hour", 0, 23, integer=True)
    number(s, "july_min_hour", 0, 23, integer=True)
    number(s, "april_min_net_load_mw", -20000, 60000)
    prof = s.get("april_mean_net_load_mw_by_hour")
    if not isinstance(prof, dict) or sorted(prof, key=int) != [str(h) for h in range(24)]:
        return err('april_mean_net_load_mw_by_hour must have exactly the keys "0" ... "23"')
    bad = [h for h, v in prof.items() if not isinstance(v, (int, float)) or isinstance(v, bool)
           or math.isnan(v) or not -20000 <= v <= 60000]
    if bad:
        return err(f"april_mean_net_load_mw_by_hour has missing or impossible values at hours {bad}")
    print("  ok    april_mean_net_load_mw_by_hour: 24 hours filled")
    m = s.get("april_min_hour")
    if isinstance(m, int) and 0 <= m <= 23 and isinstance(s.get("april_min_net_load_mw"), (int, float)):
        if min(prof.values()) != prof[str(m)]:
            err("april_min_hour is not the hour with the smallest value in your own April profile")
        if not math.isclose(prof[str(m)], s["april_min_net_load_mw"], rel_tol=1e-6, abs_tol=0.5):
            err("april_min_net_load_mw does not equal your profile's value at april_min_hour")


def fips_list(s, key):
    v = s.get(key)
    if not (isinstance(v, list) and len(v) == 10 and all(isinstance(f, str) and len(f) == 5 and f.isdigit() for f in v)):
        return err(f"{key} must be a list of 10 five-digit FIPS strings, e.g. \"04013\"")
    print(f"  ok    {key}: 10 FIPS codes")
    return v


def check_medsl(s):
    number(s, "n_counties_joined", 2500, 3300, integer=True)
    number(s, "median_shift_pts", -100, 100)
    top_r, top_d = fips_list(s, "top10_toward_R_fips"), fips_list(s, "top10_toward_D_fips")
    path = ROOT / (s.get("shifts_csv") or "results/county_shifts.csv")
    if not path.exists():
        return err(f"{path.relative_to(ROOT)} not found")
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    need = {"fips", "state_po", "county_name", "r_share_2020", "r_share_2024", "shift"}
    if not rows or not need <= set(rows[0]):
        return err(f"{path.name} needs columns {sorted(need)}")
    fips = [r["fips"] for r in rows]
    if any(len(x) != 5 or not x.isdigit() for x in fips):
        err(f"{path.name}: every fips must be a five-digit string with leading zeros kept")
    if len(set(fips)) != len(fips):
        err(f"{path.name}: some counties appear more than once")
    if any(x.startswith("02") for x in fips):
        err(f"{path.name}: Alaska should be excluded (see the assignment)")
    try:
        for r in rows:
            a, b, d = float(r["r_share_2020"]), float(r["r_share_2024"]), float(r["shift"])
            if not (0 <= a <= 100 and 0 <= b <= 100):
                raise ValueError(f"share outside 0-100 for {r['fips']}; shares are in percent")
            if abs((b - a) - d) > 0.01:
                raise ValueError(f"shift != r_share_2024 - r_share_2020 for {r['fips']}")
    except ValueError as e:
        err(f"{path.name}: {e}")
    if isinstance(s.get("n_counties_joined"), int) and s["n_counties_joined"] != len(rows):
        err(f"n_counties_joined ({s['n_counties_joined']}) != rows in {path.name} ({len(rows)})")
    for lst in (top_r, top_d):
        if lst and not set(lst) <= set(fips):
            err("top-10 FIPS must all appear in your shifts CSV")
    print(f"  ok    {path.name}: {len(rows):,} rows read")


def main():
    path = ROOT / "results.json"
    try:
        res = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Cannot read results.json: {e}")
    opt = str(res.get("option") or "").strip().upper()[:1]
    if opt not in OPTIONS:
        sys.exit('Set "option" in results.json to "A", "B" or "C".')
    key = OPTIONS[opt]
    print(f"Checking option {opt} ({key})")
    sec = res.get(key) or {}
    {"A": check_hot, "B": check_eia, "C": check_medsl}[opt](sec)
    for k, v in OPTIONS.items():
        if k != opt and any(x not in (None, [], {}) and not isinstance(x, (dict, str)) for x in (res.get(v) or {}).values()):
            print(f"  note  section {v} has values but you chose option {opt}; only {key} is read")
    if errors:
        print(f"\n{len(errors)} problem(s) to fix.")
        sys.exit(1)
    print("\nFormat looks right. This does not check whether the answers are correct.")


if __name__ == "__main__":
    main()
