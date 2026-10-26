# CAS 201 data exploration project

Starter repository for the data exploration project. **The assignment, deadlines and grading are on Canvas.**
This file covers only setup and where things are.

## Get started

1. On GitHub, click **Use this template → Create a new repository**. Make it **private**, under your own account.
2. Open it in a Codespace (**Code → Codespaces → Create codespace**). The container installs everything in `requirements.txt`.
   Working locally instead? Use Python 3.12: `python -m venv .venv`, activate it, then `pip install -r requirements.txt`.
3. In the terminal, run `python check_data.py`. Every line should say `OK`.
4. Open the notebook for the option you chose in `notebooks/` and start working.

## What's here

| Path | What it is |
|---|---|
| `data/` | The three provided datasets. **Read only.** `data/README.md` has provenance and the citation you must include. |
| `notebooks/A_hot.ipynb`, `B_eia.ipynb`, `C_medsl.ipynb` | Empty skeletons, one per option. Your code, figures and written explanations all go here (use Markdown cells). Work in yours; delete the other two if you like. |
| `results.json` | Where your first-target numbers go, in a fixed format. Fill in only your option's section. |
| `results/` | Anything your code writes (for Option C, `results/county_shifts.csv`). |
| `figures/` | Saved figures (PNG). |
| `AI_USE.md` | Your log of AI-tool use. |
| `check_data.py` | Confirms the data files are present and unmodified. |
| `check_results.py` | Confirms `results.json` is filled in and well formed. **It does not tell you whether your answers are right.** |

## Before you submit

```
python check_data.py
python check_results.py
```

Both should finish without problems. Then follow the submission steps on Canvas.
