"""Check that the provided data files are present and unmodified.

Run from the repository root:   python check_data.py

This only checks the files you were given. It says nothing about whether
your analysis is right.
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# path: (md5, number of data rows, what the row count means)
FILES = {
    "data/hot/hot_aloha_bottle_1988_2024.nc": ("ec29d59f7cf8c43c3645bcd923d6addb", 97444, "bottles"),
    "data/eia/EIA930_BALANCE_2024_Jan_Jun_CISO.csv": ("7e472e0edd38183eb6132271adda9257", 4367, "rows"),
    "data/eia/EIA930_BALANCE_2024_Jul_Dec_CISO.csv": ("627a94a1dd3e77ff37227a84b97b0217", 4417, "rows"),
    "data/medsl/countypres_2000-2024.csv": ("bd6661282936006b4ef4f5ee71418f3e", 94151, "rows"),
    "data/medsl/codebook.md": ("bb49e28faf9b18266665ab01dccf295f", None, ""),
}


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_rows(path):
    if path.suffix == ".nc":
        import xarray as xr
        with xr.open_dataset(path, decode_times=False) as ds:
            return ds["crn"].size
    with open(path, "rb") as f:
        return sum(1 for _ in f) - 1  # minus the header line


def main():
    problems = 0
    for rel, (want_md5, want_rows, unit) in FILES.items():
        path = ROOT / rel
        if not path.exists():
            print(f"MISSING   {rel}")
            problems += 1
            continue
        if md5(path) != want_md5:
            print(f"MODIFIED  {rel}  (MD5 does not match; restore it with: git checkout -- {rel})")
            problems += 1
            continue
        if want_rows is None:
            print(f"OK        {rel}")
            continue
        rows = count_rows(path)
        status = "OK" if rows == want_rows else "ROWS?"
        problems += status != "OK"
        print(f"{status:<9} {rel}  ({rows:,} {unit})")
    if problems:
        print(f"\n{problems} problem(s). Never edit the files in data/; write cleaned data somewhere else.")
        sys.exit(1)
    print("\nAll data files present and unmodified.")


if __name__ == "__main__":
    main()
