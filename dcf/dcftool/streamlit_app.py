import streamlit as st
from dcftool.data.yfinance_client import YFinanceClient
from dcftool.models.forecast import Forecast
from dcftool.models.discount_rate import DiscountRate
from dcftool.models.dcf_calculation import DCFCalculation
from dcftool.reports.report import Report
import plotly.graph_objects as go

st.title("DCF Valuation Tool")
with st.sidebar:
    st.header("Input Parameters")
    ticker = st.text_input("Ticker", "AAPL")
    growth = st.number_input("Revenue Growth Rate", value=0.05)
    margin = st.number_input("FCF Margin", value=0.15)
    reinvestment = st.number_input("Reinvestment Rate", value=0.10)
    rf = st.number_input("Risk-Free Rate", value=0.02)
    beta = st.number_input("Beta", value=1.2)
    erp = st.number_input("Equity Risk Premium", value=0.05)
    debt_rate = st.number_input("Debt Interest Rate", value=0.04)
    tax_rate = st.number_input("Tax Rate", value=0.21)
    forecast_years = st.number_input("Forecast Years", value=7, min_value=5, max_value=10)
    terminal_growth = st.number_input("Terminal Growth Rate", value=0.02)
    shares_outstanding = st.number_input("Shares Outstanding", value=16000000000.0)
    net_debt = st.number_input("Net Debt", value=0.0)

st.markdown("""
**Example Usage:**

- Ticker: `AAPL`
- Revenue Growth Rate: `0.05`
- FCF Margin: `0.15`
- Reinvestment Rate: `0.10`
- Risk-Free Rate: `0.02`
- Beta: `1.2`
- Equity Risk Premium: `0.05`
- Debt Interest Rate: `0.04`
- Tax Rate: `0.21`
- Forecast Years: `7`
- Terminal Growth Rate: `0.02`
- Shares Outstanding: `16000000000`
- Net Debt: `0`

Click **Analyze** to run the DCF valuation and see the intrinsic value per share, FCF projections, and export results.
""")

if st.button("Analyze"):
    client = YFinanceClient(ticker)
    income = client.get_income_statement()
    base_year = income.index.max()
    # Handle DatetimeIndex, PeriodIndex, or string index
    if hasattr(base_year, 'year'):
        base_year_val = base_year.year
    else:
        try:
            base_year_val = int(base_year)
        except Exception:
            base_year_val = 0

    # Debug: Show the DataFrame structure in the app
    st.write('Income Statement DataFrame (head):')
    st.dataframe(income.head())
    st.write('Income Statement Columns:', income)
    st.write('Income Statement Index:', list(income.index))

    # Robust revenue column selection
    revenue_cols = [
        'Total Revenue', 'Revenue', 'totalRevenue', 'Revenues', 'revenues', 'Operating Revenue', 'operatingRevenue'
    ]
    found_col = None
    for col in revenue_cols:
        if col in income.columns:
            found_col = col
            break
    # Try to get the last available revenue value
    base_revenue = None
    if found_col:
        try:
            base_revenue = income[found_col].dropna().iloc[-1]
        except Exception:
            base_revenue = None
    if base_revenue is None or not isinstance(base_revenue, (int, float)):
        # fallback: use last value of first numeric column
        numeric_cols = income.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            try:
                base_revenue = income[numeric_cols[0]].dropna().iloc[-1]
            except Exception:
                base_revenue = 0.0
        else:
            base_revenue = 0.0

    # Fetch historical cash flow using yfinance API directly
    import yfinance as yf
    ticker_obj = yf.Ticker(ticker)
    hist_cf_df = ticker_obj.cashflow.T  # Transpose to get years as index
    hist_fcf = None
    hist_years = None
    # Try to find FCF column in yfinance cashflow
    fcf_cols = ['Free Cash Flow', 'freeCashFlow', 'Total Cash From Operating Activities', 'totalCashFromOperatingActivities']
    found_fcf_col = None
    for col in fcf_cols:
        if col in hist_cf_df.columns:
            found_fcf_col = col
            break
    if found_fcf_col:
        hist_fcf = hist_cf_df[found_fcf_col].dropna().tail(5)
        hist_years = hist_fcf.index.astype(str)

    # Align base_year and base_revenue to the last available historical FCF year if possible
    aligned_base_year = None
    aligned_base_revenue = None
    if hist_years is not None and len(hist_years) > 0:
        last_hist_year = hist_years[-1]
        # Try to find matching year in income statement index
        if last_hist_year in income.index:
            aligned_base_year = last_hist_year
            if found_col and found_col in income.columns:
                aligned_base_revenue = income.loc[last_hist_year, found_col]
            else:
                numeric_cols = income.select_dtypes(include='number').columns
                if len(numeric_cols) > 0:
                    aligned_base_revenue = income.loc[last_hist_year, numeric_cols[0]]
    # Use aligned base_year and base_revenue if available
    if aligned_base_year is not None and aligned_base_revenue is not None and isinstance(aligned_base_revenue, (int, float)) and aligned_base_revenue > 0:
        try:
            base_year_val = int(aligned_base_year) if isinstance(aligned_base_year, (int, float, str)) and str(aligned_base_year).isdigit() else base_year_val
        except Exception:
            pass
        base_revenue = aligned_base_revenue
        st.info(f"Base year and revenue aligned to last historical FCF year: {aligned_base_year}")
    elif base_revenue is not None and isinstance(base_revenue, (int, float)) and base_revenue > 0:
        st.info("Base revenue taken from most recent available year in income statement.")
    else:
        st.warning("Could not find a valid base revenue. Projections may be inaccurate.")

    forecast = Forecast(base_year=base_year_val, base_revenue=base_revenue, base_margin=margin, base_reinvestment=reinvestment, growth=growth, margin=margin, reinvestment=reinvestment, years=forecast_years)
    fcf_proj = forecast.project()
    discount = DiscountRate(rf, beta, erp, debt_rate, tax_rate, shares_outstanding, net_debt)
    wacc = discount.wacc()
    dcf = DCFCalculation(fcf_proj, wacc, terminal_growth, net_debt, shares_outstanding)
    intrinsic = dcf.present_value()
    details = dcf.details()
    st.write(f"Intrinsic value per share: ${intrinsic:.2f}")
    st.dataframe(fcf_proj)
    st.write(details)
    Report.export_to_csv(fcf_proj, f"{ticker}_fcf_projection.csv")
    st.success(f"Projection exported to {ticker}_fcf_projection.csv")

    # --- Visual Summary Section ---
    st.header("Summary & Visuals")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Assumptions")
        st.markdown(f"""
        - **Tax Rate:** {tax_rate:.0%}
        - **Discount Rate (WACC):** {wacc:.0%} (auto or user)
        - **Perpetual Growth Rate:** {terminal_growth:.0%}
        - **Shares Outstanding:** {shares_outstanding:,.0f}
        - **Net Debt:** ${net_debt:,.0f}
        """)

    with col2:
        st.subheader("Intrinsic Value vs Market Value")
        try:
            import yfinance as yf
            price = yf.Ticker(ticker).info.get('regularMarketPrice', 0)
        except Exception:
            price = 0
        upside = float(intrinsic) - price
        fig = go.Figure(data=[
            go.Bar(name="Market Value", x=["Market Value"], y=[price]),
            go.Bar(name="Intrinsic Value", x=["Intrinsic Value"], y=[float(intrinsic)])
        ])
        fig.add_trace(go.Bar(name="Upside", x=["Upside"], y=[upside]))
        fig.update_layout(barmode='group', yaxis_title="$/Share")
        st.plotly_chart(fig, use_container_width=True)

    # --- Cash Flow Chart (show historical + projected, with trendline) ---
    # Fetch historical cash flow using yfinance API directly
    ticker_obj = yf.Ticker(ticker)
    hist_cf_df = ticker_obj.cashflow.T  # Transpose to get years as index
    hist_fcf = None
    hist_years = None
    # Try to find FCF column in yfinance cashflow
    fcf_cols = ['Free Cash Flow', 'freeCashFlow', 'Total Cash From Operating Activities', 'totalCashFromOperatingActivities']
    found_fcf_col = None
    for col in fcf_cols:
        if col in hist_cf_df.columns:
            found_fcf_col = col
            break
    if found_fcf_col:
        hist_fcf = hist_cf_df[found_fcf_col].dropna().tail(5)
        hist_years = hist_fcf.index.astype(str)
    # If available, plot historical and projected FCF together
    if (hist_fcf is not None and not hist_fcf.empty) and ('fcf' in fcf_proj.columns and fcf_proj['fcf'].notna().any()):
        st.subheader("Cash Flow Projection (with Historical)")
        fig_cf = go.Figure()
        # Historical
        fig_cf.add_trace(go.Bar(x=hist_years, y=hist_fcf.values, name="Historical FCF", marker_color='gray'))
        # Projected
        fig_cf.add_trace(go.Bar(x=fcf_proj['year'], y=fcf_proj['fcf'], name="Projected FCF", marker_color='blue'))
        # Trendline (linear fit on combined data)
        import numpy as np
        all_years = list(hist_years) + list(fcf_proj['year'].astype(str))
        all_fcf = list(hist_fcf.values) + list(fcf_proj['fcf'].values)
        if len(all_years) > 1 and np.any(np.array(all_fcf) != 0):
            x_numeric = np.arange(len(all_years))
            z = np.polyfit(x_numeric, all_fcf, 1)
            p = np.poly1d(z)
            trend = p(x_numeric)
            fig_cf.add_trace(go.Scatter(x=all_years, y=trend, mode='lines', name='Trendline', line=dict(dash='dash', color='orange')))
            st.write(f"**FCF Trendline Rate of Change:** {z[0]:,.2f} per year")
        fig_cf.update_layout(xaxis_title="Year", yaxis_title="Free Cash Flow", title="Historical & Projected Free Cash Flows")
        st.plotly_chart(fig_cf, use_container_width=True)
    elif 'fcf' in fcf_proj.columns and fcf_proj['fcf'].notna().any() and fcf_proj['fcf'].sum() != 0:
        st.subheader("Cash Flow Projection")
        fig_cf = go.Figure()
        fig_cf.add_trace(go.Bar(x=fcf_proj['year'], y=fcf_proj['fcf'], name="FCF"))
        fig_cf.update_layout(xaxis_title="Year", yaxis_title="Free Cash Flow", title="Projected Free Cash Flows")
        st.plotly_chart(fig_cf, use_container_width=True)
    else:
        st.info("No free cash flow data available to plot.")

    # --- Detailed Tables ---
    st.subheader("Discounted Cash Flow Table")
    st.dataframe(fcf_proj)

    st.subheader("Intrinsic Value Details")
    st.json(details)
