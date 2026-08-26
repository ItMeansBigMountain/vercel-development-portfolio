# Jupyter.Notebooks

Research lab for notebook-driven market analysis, technical-analysis experiments, statistical trend studies, and strategy/backtest prototyping. This README is the local index for the current legacy notebooks and aligns the project with `DATA_SCIENCE_RESTART_PLAN.md`: keep experiments reproducible, keep secrets out of git, and use notebooks as research artifacts before productionizing any strategy.

## Contents

### Notebooks

| Notebook | Purpose | Local data | External/API behavior | Notes |
|---|---|---|---|---|
| `EqualWeightSMP500/EqualWeight500.ipynb` | Builds an equal-weight S&P 500 portfolio/order-sheet workflow. | `EqualWeightSMP500/sp_500_stocks.csv` | Calls the IEX Cloud sandbox quote endpoint when executed. Requires `IEX_CLOUD_API_TOKEN`. | Prompts for portfolio size and writes Excel output with `xlsxwriter`. |
| `priceReturn_momentum/Rudementary_dataframe/quantMomementum.ipynb` | Basic price-return momentum strategy using batch advanced-stats/price data. | `priceReturn_momentum/Rudementary_dataframe/sp_500_stocks.csv` | Calls IEX Cloud sandbox batch `advanced-stats,price`. Requires `IEX_CLOUD_API_TOKEN`. | Prompts for portfolio size and exports an order sheet. |
| `priceReturn_momentum/highQuality_dataframe/highQuality_momentum.ipynb` | Higher-quality momentum screen using multiple return windows and percentile scores. | `priceReturn_momentum/highQuality_dataframe/sp_500_stocks.csv` | Calls IEX Cloud sandbox batch `advanced-stats,price`. Requires `IEX_CLOUD_API_TOKEN`. | Uses `statistics` and `scipy.stats.percentileofscore`; prompts for portfolio size. |
| `robustValue/rudementary/P_E_ratio.ipynb` | Intro quantitative value notebook focused on P/E ratio ranking. | `robustValue/rudementary/sp_500_stocks.csv` | Calls IEX Cloud sandbox batch quote data. Requires `IEX_CLOUD_API_TOKEN`. | Prompts for portfolio size and exports an order sheet. |
| `robustValue/better/robustValue.ipynb` | More robust value strategy using valuation metrics such as P/E, P/B, P/S, EV/EBITDA, and EV/GP. | `robustValue/better/sp_500_stocks.csv`, `robustValue/better/test.csv` | Calls IEX Cloud sandbox batch `quote,advanced-stats`. Requires `IEX_CLOUD_API_TOKEN`. | `test.csv` appears to be a large local sample/cache with ticker-only rows; the notebook still expects live API data for full results. |

### CSV sample data

- Every notebook directory includes `sp_500_stocks.csv`, a single-column `Ticker` sample containing 505 S&P 500 symbols.
- `robustValue/better/test.csv` is also single-column `Ticker` data with 11,702 rows. Treat it as local sample/cache data, not a secret store.
- The CSV files are safe to load offline with pandas, but the notebooks' market metrics come from IEX Cloud sandbox calls unless cells are adapted to use cached responses.

### Supporting docs

- `DATA_SCIENCE_RESTART_PLAN.md` defines the project direction: technical analysis, statistical trend studies, bot research, reusable datasets/chart templates, and reproducible backtests.
- `DEVELOPMENT_PLAN.md` tracks the high-level modernization phases and hosting posture. This project is not a direct Vercel app unless notebooks are exported into a static dashboard or docs site.
- `OFFLINE_VALIDATION.md` documents the fixture-backed, non-interactive notebook smoke check.
- `EqualWeightSMP500/valueMetrics.txt` contains notes on value metrics and the learning-oriented workflow.

## Safe local setup

Prerequisites:

- Python 3.11+ available as `python3`.
- `uv` installed for isolated virtual environments.
- Optional: an IEX Cloud sandbox token if you intentionally execute cells that call the IEX API.

Install dependencies:

```bash
cd /opt/data/HeRmEz/projects/Jupyter.Notebooks
uv venv --clear .venv --python python3
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m ipykernel install --user --name jupyter-notebooks --display-name "Python (Jupyter.Notebooks)"
```

Configure secrets locally only:

```bash
cp .env.example .env
# edit .env and set IEX_CLOUD_API_TOKEN=... if you need live IEX sandbox data
```

Do not commit `.env`, real API tokens, generated Excel order sheets, or private account data. The notebooks read `IEX_CLOUD_API_TOKEN` from the environment through `finance_notebook_helpers.py`, default to offline fixture-backed behavior, and require `LIVE_IEX_API=1` before live IEX sandbox calls are made.

Start JupyterLab:

```bash
cd /opt/data/HeRmEz/projects/Jupyter.Notebooks
.venv/bin/jupyter lab
```

## Local validation commands

These commands are deterministic and do not execute notebook cells or call external APIs:

```bash
cd /opt/data/HeRmEz/projects/Jupyter.Notebooks
uv venv --clear .venv --python python3
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python - <<'PY'
from pathlib import Path
import ast
import nbformat
from nbformat.validator import validate

root = Path('.')
for notebook in sorted(root.rglob('*.ipynb')):
    data = nbformat.read(notebook, as_version=4)
    validate(data)
    for index, cell in enumerate(data.cells):
        if cell.cell_type == 'code':
            ast.parse(cell.source, filename=f'{notebook}#cell-{index}')
print('validated notebook JSON, nbformat schema, and Python syntax')
PY
.venv/bin/python - <<'PY'
import importlib
for name in ['numpy', 'pandas', 'requests', 'scipy', 'xlsxwriter', 'nbformat']:
    importlib.import_module(name)
print('dependency import smoke passed')
PY
git status --short -- .
```

The project also includes an optional offline/non-interactive execution check. It uses `finance_notebook_helpers.py` plus `fixtures/iex_batch_sample.json` to avoid live API calls and prompts:

```bash
cd /opt/data/HeRmEz/projects/Jupyter.Notebooks
uv run --with nbformat --with pandas --with numpy --with scipy --with xlsxwriter python scripts/validate_offline_notebooks.py
```

The script removes generated Excel/text outputs after each notebook smoke run.

## External API usage

The notebooks use IEX Cloud sandbox endpoints under `https://sandbox.iexapis.com/stable/stock/...` for quote, price, and advanced-stats data. Required credential name:

- `IEX_CLOUD_API_TOKEN`

Use a sandbox token for local experiments and set `LIVE_IEX_API=1` only when intentionally making network calls. Do not place real token values in notebook cells, README text, committed config, or screenshots.

## Restart-plan alignment

Next modernization steps should follow `DATA_SCIENCE_RESTART_PLAN.md`:

1. Keep these legacy notebooks indexed as market-data, momentum, and value-strategy examples.
2. Add offline sample API responses or cached fixtures before running notebooks in CI.
3. Refactor repeated API batching, portfolio-sizing input, scoring, and Excel export code into reusable Python modules.
4. Build first new notebooks for moving averages/RSI/MACD/volatility/drawdowns, portfolio performance decomposition, sentiment-versus-price exploration, and train/test-safe backtest templates.
5. Publish only static dashboards/docs from sanitized outputs; never publish credentials or account-specific trading recommendations.
