## Summary

A Python-based DCF evaluation tool can be organized into modular components including data ingestion, cash flow projection, discount rate calculation, DCF computation, and reporting . Historical financial data can be fetched from APIs such as yfinance for stock data  or Alpha Vantage for fundamental endpoints . Free cash flows are projected over a forecast period—commonly five to ten years—before calculating a terminal value using perpetuity growth or exit multiple methods ([en.wikipedia.org][1]). Discount factors derive from the company’s weighted average cost of capital (WACC), often estimated via CAPM and adjusted for debt cost ([en.wikipedia.org][2]). Present value computations can leverage NumPy’s `npv` function for numerical efficiency . Visualization modules based on matplotlib can render sensitivity analyses and intrinsic value charts . Sample codebases like the halessi DCF library provide practical reference implementations to accelerate development .

## 1. Data Ingestion

Financial data ingestion should be encapsulated in client classes, for example a `YFinanceClient` leveraging the yfinance library to retrieve income statements, balance sheets, and cash flow data . An `AlphaVantageClient` can call Alpha Vantage’s fundamental data endpoints—such as `OVERVIEW` and `CASH_FLOW`—requiring an API key for authenticated requests .

Optionally, a `FinancialModelingPrepClient` module can interface with Financial Modeling Prep’s REST API for supplemental or cross-verified data retrieval . Once fetched, all raw JSON or CSV responses should be standardized into pandas DataFrames, with consistent date indexing and column naming conventions to simplify downstream processing .

## 2. Cash Flow Projection

The projection component must calculate unlevered free cash flow (FCFF), defined as net income plus non-cash charges (e.g., depreciation and amortization) minus capital expenditures and changes in working capital . Users should be able to set growth assumptions for revenue, operating margins, reinvestment rates, and forecast periods—typically five to ten years—to generate year-over-year FCF estimates ([en.wikipedia.org][1]).

This module should support scenario analysis by accepting alternative growth rate vectors and sensitivity inputs, enabling side-by-side comparison of bull, base, and bear case valuations .

## 3. Discount Rate Calculation

A dedicated discount rate module computes the weighted average cost of capital (WACC) by combining the cost of equity—estimated via the capital asset pricing model (CAPM)—with the after-tax cost of debt, each weighted by their market values ([en.wikipedia.org][2]). Inputs for CAPM (risk-free rate, beta, equity risk premium) should be parameterized or fetched from market data sources.

For users who prefer simplicity, the tool should also allow direct input of a pre-calculated WACC value, bypassing component calculations ([corporatefinanceinstitute.com][3]).

## 4. DCF Computation

The valuation engine applies NumPy’s `npv` function to compute the present value of projected FCFs across the forecast horizon . Terminal value is estimated using the Gordon Growth Model—FCF in the final forecast year divided by (WACC − g)—and then discounted back to present value ([en.wikipedia.org][1]).

Enterprise value is the sum of the PVs of FCFs plus the PV of the terminal value, representing the total business value ([en.wikipedia.org][4]). An optional step subtracts net debt from enterprise value to derive equity value and calculates per-share intrinsic price ([en.wikipedia.org][4]).

## 5. Reporting and Visualization

A reporting module should export valuation outputs and assumptions to CSV or Excel files and generate summary tables via pandas DataFrames for auditability . Visualization functions built with matplotlib can render sensitivity charts—such as intrinsic value versus discount rate or growth rate—to aid investor decision-making .

Interactive dashboards (e.g., via Streamlit or Dash) can be layered on top for real-time adjustments and dynamic chart updates, though this extends beyond core DCF functionality.

## 6. Example Code Structure

```python
# dcftool/
# ├── data/
# │   ├── __init__.py
# │   ├── yfinance_client.py
# │   ├── alphavantage_client.py
# │   └── fmp_client.py
# ├── models/
# │   ├── __init__.py
# │   ├── forecast.py
# │   ├── discount_rate.py
# │   └── dcf_calculation.py
# ├── reports/
# │   ├── __init__.py
# │   ├── csv_report.py
# │   └── excel_report.py
# ├── visualization/
# │   ├── __init__.py
# │   └── sensitivity_plot.py
# ├── cli.py
# └── requirements.txt
```

## 7. Implementation Plan

1. **Week 1**: Set up project structure, virtual environment, and basic `YFinanceClient` prototype.
2. **Week 2**: Implement `AlphaVantageClient` and data normalization layer.
3. **Week 3**: Develop `forecast.py` to compute FCF projections with configurable assumptions.
4. **Week 4**: Build `discount_rate.py` for CAPM and WACC calculations.
5. **Week 5**: Create `dcf_calculation.py` leveraging NumPy for PV and terminal value functions.
6. **Week 6**: Add reporting modules (`csv_report`, `excel_report`) and integrate CLI entry points.
7. **Week 7**: Develop visualization scripts and optional dashboard prototype.
8. **Week 8**: Testing, documentation, and packaging for distribution (e.g., PyPI).

This roadmap balances core valuation functionality with extensibility for advanced analysis and user-friendly reporting.

[1]: https://en.wikipedia.org/wiki/Valuation_using_discounted_cash_flows "Valuation using discounted cash flows"
[2]: https://en.wikipedia.org/wiki/Corporate_finance "Corporate finance"
[3]: https://corporatefinanceinstitute.com/resources/valuation/discounted-cash-flow-dcf/ "Discounted Cash Flow (DCF) - Formula, Calculate, Pros and Cons"
[4]: https://en.wikipedia.org/wiki/Discounted_cash_flow "Discounted cash flow"
