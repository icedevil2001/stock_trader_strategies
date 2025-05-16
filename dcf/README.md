## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd dcf
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
uv pip install .
```

### 4. Sync Environment (Optional, for full lockfile reproducibility)
```bash
uv sync
```

## How to Run the Tool

### Command-Line Interface (CLI)
Run the DCF analysis from the command line:
```bash
python -m dcftool.cli analyze \
  --ticker AAPL \
  --growth 0.05 --margin 0.15 --reinvestment 0.10 \
  --rf 0.02 --beta 1.2 --erp 0.05 --debt-rate 0.04 \
  --tax-rate 0.21 --forecast-years 7 \
  --terminal-growth 0.02 --shares-outstanding 16000000000 --net-debt 0
```

### Streamlit Web App
Launch the interactive web UI:
```bash
streamlit run dcftool/streamlit_app.py
```

### Jupyter Notebook Example
Open the example notebook:
```bash
jupyter notebook notebooks/example_aapl.ipynb
```

### Run Unit Tests
```bash
pytest
```

---
