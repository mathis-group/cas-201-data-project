# Provided data

**Do not edit, re-save, or replace these files.** `python check_data.py` verifies them by MD5.
Write anything you derive (cleaned tables, subsets) to `results/` or another folder.

Each file is a frozen snapshot, so everyone in the class works from exactly the same data.
The source websites may since have revised their versions; use these files, not a fresh download.

---

## Option A: Hawaii Ocean Time-series (HOT) bottle data

| | |
|---|---|
| File | `hot/hot_aloha_bottle_1988_2024.nc` (netCDF, 11.7 MB, 97,444 bottles) |
| MD5 | `ec29d59f7cf8c43c3645bcd923d6addb` |
| Source | HOT-DOGS bottle extraction, https://hahana.soest.hawaii.edu/hot/hot-dogs/bextraction.html |
| Extracted | 2026-10-21. Station 2 (ALOHA), 1 January 1988 to 31 December 2024, all depths |
| Variables | `crn` cruise, `stn` station, `cast`, `ros` rosette position, `mdate` date (mmddyy), `mtime` time (hhmmss), `press` pressure (dbar), `temp` CTD temperature, `csal` CTD salinity, `bsal` bottle salinity, `boxy` oxygen, `dic` dissolved inorganic carbon, `ph` pH, `alk` alkalinity, `nit` nitrate + nitrite |
| Definitions and units | https://hahana.soest.hawaii.edu/hot/hot-dogs/units/hydrov.html |
| Version | HOT-DOGS extractions have no version number or DOI; this file is a snapshot of the HOT database on the extraction date |
| License | No license is stated. HOT asks users of the data to cite it as below |

**Required citation:**
> Data obtained via the Hawaii Ocean Time-series HOT-DOGS application; University of Hawai'i at Mānoa. National Science Foundation Award # 2241005.

Published result you will compare with:
> Dore, J. E., Lukas, R., Sadler, D. W., Church, M. J., & Karl, D. M. (2009). Physical and biogeochemical modulation of ocean acidification in the central North Pacific. *PNAS* 106(30), 12235–12240. https://doi.org/10.1073/pnas.0906044106

---

## Option B: EIA hourly electric grid data (Form EIA-930), California ISO

| | |
|---|---|
| Files | `eia/EIA930_BALANCE_2024_Jan_Jun_CISO.csv` (4,367 rows), `eia/EIA930_BALANCE_2024_Jul_Dec_CISO.csv` (4,417 rows) |
| MD5 | `7e472e0edd38183eb6132271adda9257`, `627a94a1dd3e77ff37227a84b97b0217` |
| Source | U.S. Energy Information Administration, Hourly Electric Grid Monitor, six-month BALANCE files `EIA930_BALANCE_2024_Jan_Jun.csv` (MD5 `75669ae2c4b02d635930e815510e5059`) and `EIA930_BALANCE_2024_Jul_Dec.csv` (MD5 `545f301108bbfd933e724a08de948651`), https://www.eia.gov/electricity/gridmonitor/ |
| Downloaded | 2026-10-21 |
| What was changed | Kept only rows with `Balancing Authority == "CISO"` (California ISO). Removed three columns: `Data Date`, `Hour Number`, `Local Time at End of Hour`. Every other column, every column name (typos included), and the split into two half-year files are exactly as EIA published them. |
| Documentation | https://www.eia.gov/electricity/gridmonitor/about and https://www.eia.gov/opendata/ |
| Version | EIA revises EIA-930 data and regenerates these files; the source MD5s above identify the snapshot used |
| License | Public domain (U.S. government work) |

**Required citation:**
> U.S. Energy Information Administration, Form EIA-930 Hourly Electric Grid Monitor, 2024 BALANCE data (accessed 21 October 2026). https://www.eia.gov/electricity/gridmonitor/

---

## Option C: MIT Election Data and Science Lab county presidential returns

| | |
|---|---|
| Files | `medsl/countypres_2000-2024.csv` (94,151 rows); `medsl/codebook.md` (the dataset's codebook, published on Dataverse as `County Presidential Returns 2000-2024.md`, dated 2025-07-12) |
| MD5 | CSV `bd6661282936006b4ef4f5ee71418f3e` (same as listed on Dataverse); codebook `bb49e28faf9b18266665ab01dccf295f` |
| Source | Harvard Dataverse, https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ |
| Version | 20.0, released 2026-02-25 (every row has `version == 20260225`) |
| Downloaded | 2026-10-21, original file format, unmodified |
| License | CC0 1.0 (public domain dedication) |

**Required citation:**
> MIT Election Data and Science Lab (2018). County Presidential Election Returns 2000–2024. Harvard Dataverse, V20. https://doi.org/10.7910/DVN/VOQCHQ
