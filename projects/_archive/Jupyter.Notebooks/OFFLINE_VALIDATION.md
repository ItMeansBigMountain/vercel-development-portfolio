# Offline notebook validation

The finance notebooks default to safe offline execution:

- `NOTEBOOK_OFFLINE=1` and `LIVE_IEX_API=0` use bundled fixture data from `fixtures/iex_batch_sample.json`.
- `HERMES_NONINTERACTIVE=1` and `PORTFOLIO_SIZE=100000` avoid blocking on portfolio-size prompts.
- IEX tokens are loaded only from environment variables or a local ignored `.env`; tokens are not hardcoded or printed.

Run the deterministic smoke check from this project root:

```bash
uv run --with nbformat --with pandas --with numpy --with scipy --with xlsxwriter python scripts/validate_offline_notebooks.py
```

The validation script scans code cells for raw `input(...)`, raw `requests.get(...)`, and non-environment token assignments before executing cells. Generated spreadsheet/text outputs are removed after each notebook smoke run.

To intentionally run against the live IEX sandbox, set `NOTEBOOK_OFFLINE=0`, `LIVE_IEX_API=1`, and provide `IEX_CLOUD_API_TOKEN` in the environment or in a local `.env` copied from `.env.example`.
