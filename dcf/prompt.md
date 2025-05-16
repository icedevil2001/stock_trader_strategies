## Summary

A high-quality AI prompt for building a Python DCF tool must clearly define the AI’s role, project scope, inputs/outputs, and evaluation criteria, while specifying module responsibilities, data sources, and coding standards to ensure a complete, production-ready solution ([OpenAI Help Center][1]). Best practices also recommend framing the problem with concrete examples, persona directives, and success metrics, then iteratively refining based on intermediate outputs ([MIT Sloan TLT][2]).

## Detailed Prompt Sections

### 1. Persona & Role

* **Persona**: “You are a senior Python financial engineer with expertise in valuation models and software architecture.” ([Medium][3])
* **Tone & Style**: “Write clean, well-commented, PEP8-compliant code. Explain each step concisely.” ([OpenAI Help Center][1])

### 2. Project Overview

* **Objective**: “Develop a modular Python package named `dcftool` that computes intrinsic stock value via Discounted Cash Flow analysis.”
* **Success Criteria**:

  1. Fetch historical financials for any ticker.
  2. Project free cash flows over a configurable horizon.
  3. Calculate WACC via CAPM and debt schedules.
  4. Compute PV of cash flows + terminal value.
  5. Output per-share intrinsic value and sensitivity tables.

### 3. Technical Requirements

* **Language & Libraries**: Python 3.9+, `pandas`, `numpy`, `yfinance` or equivalent API client, `matplotlib` for plots ([EODHD][4]).
* **Architecture**:

  * `data/`: API clients (e.g., `YFinanceClient`, `AlphaVantageClient`) ([GitHub][5])
  * `models/`: cash-flow projection, discount-rate calculation, DCF computation
  * `reports/`: CSV/Excel export, sensitivity analysis tables
  * `cli.py`: command-line interface

### 4. Data Sources & APIs

* **Default**: `yfinance` for price & cash-flow data.
* **Fallback**: Alpha Vantage (via `OVERVIEW` and `CASH_FLOW` endpoints).
* **Normalization**: Convert JSON/CSV responses into uniform `DataFrame` structures.

### 5. Input & Output Specifications

* **Inputs**:

  * `ticker` string
  * Forecast assumptions: revenue growth rate, margin, reinvestment rate, forecast years (5–10)
  * Discount parameters: risk-free rate, beta, equity premium, debt interest rate
* **Outputs**:

  * Intrinsic value per share (float)
  * Detailed DataFrame of annual FCF projections and present values
  * Terminal value computation
  * Sensitivity analysis matrix (e.g., value vs. WACC/growth)

### 6. Code Quality & Constraints

* **Standards**:

  * Adhere to PEP8 and type annotations.
  * Include unit tests for each module (e.g., using `pytest`).
* **Documentation**:

  * Docstrings for all classes/functions.
  * `README.md` with installation, usage examples, and assumptions.

### 7. Testing & Validation

* **Unit Tests**:

  * Mock API responses to test data ingestion.
  * Validate correct PV and terminal value formulas.
* **Example Notebook**: Provide a Jupyter notebook demonstrating valuation of a well-known stock (e.g., AAPL).

### 8. Example Usage

> ```bash
> pip install dcftool
> dcftool analyze --ticker AAPL \
>   --growth 0.05 --margin 0.15 --reinvestment 0.10 \
>   --rf 0.02 --beta 1.2 --erp 0.05 --debt-rate 0.04 \
>   --forecast-years 7
> ```
>
> **Expected Output**:
>
> * “Intrinsic value per share: \$150.23”
> * CSV report and sensitivity chart

---

**Full Prompt to AI**:

> You are a senior Python financial engineer. Your task is to develop a modular Python package called `dcftool` for performing Discounted Cash Flow (DCF) valuation of stocks.
>
> **Requirements**:
>
> 1. **Data Ingestion**: Implement `YFinanceClient` and `AlphaVantageClient` classes to fetch historical income statements, cash flows, and balance sheets. Normalize data into pandas DataFrames.
> 2. **Cash Flow Projection**: Build a `forecast` module that calculates unlevered Free Cash Flow (FCFF) for 5–10 years based on user-provided growth, margin, and reinvestment assumptions.
> 3. **Discount Rate**: Create a `discount_rate` module that computes WACC via CAPM (risk-free rate, beta, equity risk premium) and after-tax cost of debt. Allow users to override with a fixed WACC.
> 4. **DCF Calculation**: In `dcf_calculation`, compute the present value of projected FCFs using NumPy’s NPV functions, calculate terminal value via Gordon Growth Model, and sum to enterprise value. Subtract net debt to yield equity value and per-share intrinsic price.
> 5. **Reporting**: Add a `reports` module to export results to CSV/Excel and generate sensitivity tables.
> 6. **CLI & Documentation**: Provide a `cli.py` command-line interface for easy invocation, include detailed docstrings, unit tests (with pytest), and a README with installation and examples.
> 7. **Visualization**: Use matplotlib to plot sensitivity analyses (intrinsic value vs. WACC and growth).
>
> **Coding Standards**:
>
> * Python 3.9+, PEP8 compliance, type annotations.
> * Include unit tests for each component.
> * Deliver a Jupyter notebook example analyzing AAPL.
>
> **Success Criteria**:
>
> * Correct intrinsic value outputs matching known benchmarks.
> * Clear, maintainable code with full documentation.
> * Comprehensive test coverage.

This prompt outlines persona, scope, modules, technical specs, examples, and success metrics to guide the AI in delivering a robust Python DCF tool.

[1]: https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt?utm_source=chatgpt.com "Prompt engineering best practices for ChatGPT - OpenAI Help Center"
[2]: https://mitsloanedtech.mit.edu/ai/basics/effective-prompts/?utm_source=chatgpt.com "Effective Prompts for AI: The Essentials"
[3]: https://bryanjcollins.medium.com/the-secret-to-writing-effective-chatgpt-prompts-0fd8fb478fdd?utm_source=chatgpt.com "The secret to writing effective ChatGPT prompts | by Bryan Collins"
[4]: https://eodhd.com/financial-academy/fundamental-analysis-examples/automate-your-discounted-cash-flow-model-in-python?utm_source=chatgpt.com "Automate your Discounted Cash Flow model in Python"
[5]: https://github.com/halessi/DCF?utm_source=chatgpt.com "halessi/DCF - Discounted Cash Flow - GitHub"

