# Stock Analysis Tool with Custom Ollama Model

A production-ready Python application that leverages a custom Ollama LLM model to analyze stock market data from Excel files (e.g., Screener.in exports) and provide AI-powered investment recommendations.

## 🚀 Features

- **Custom LLM Model**: Uses a fine-tuned Ollama model (`stocker`) specialized for stock market analysis
- **Automated Data Processing**: Loads and processes stock data from Excel files
- **Comprehensive Analysis**: Provides detailed investment recommendations including:
  - Buy/Hold/Sell recommendations
  - Entry and exit strategies
  - Target prices and stop-loss levels
  - Risk assessment
  - Time horizon analysis
- **Production-Ready**: Includes logging, error handling, and audit trails
- **DevOps Integration**: Structured for CI/CD pipelines and automated trading workflows

## 📋 Prerequisites

- Python 3.8 or higher
- Ollama installed and running on your system
- Excel file with stock data (from Screener.in or similar sources)

## 🛠️ Installation

### 1. Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com/download](https://ollama.com/download)

**Verify installation:**
```bash
ollama --version
```

### 2. Create Custom Ollama Model

Create a file named `Modelfile` with the following content:

```dockerfile
FROM ministral-3:3b
SYSTEM """You are a stock market analyst who takes company data as input from screener 
and suggests if I should invest in this stock or not and for how much time. 

Your analysis should be structured and include:
- Financial health assessment (profitability, leverage, liquidity)
- Valuation metrics (P/E, P/B, dividend yield, market cap)
- Growth trends (revenue, profit, margins)
- Clear BUY/HOLD/SELL recommendation
- Entry point with specific price levels
- Exit strategy with target price and stop-loss
- Time horizon for investment
- Risk factors and confidence level

Be specific, data-driven, and provide actionable insights."""
```

**Build the custom model:**
```bash
# Pull the base model first
ollama pull ministral-3:3b

# Create the custom model
ollama create stocker:latest -f Modelfile
```

**Verify the model:**
```bash
ollama list | grep stocker
```

### 3. Install Python Dependencies

Create a `requirements.txt` file:

```txt
langchain-ollama>=0.1.0
langchain-community>=0.0.38
unstructured[xlsx]>=0.12.0
python-magic>=0.4.27
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
stock-analyzer/
├── main.py                 # Main analysis script
├── Modelfile              # Ollama model configuration
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── 3m.xlsx               # Sample stock data file
├── data/                 # Directory for input Excel files
├── results/              # Directory for analysis outputs
└── logs/                 # Directory for log files
```

## 🎯 Usage

### Basic Usage

1. **Place your stock data Excel file** (exported from Screener.in) in the project directory

2. **Run the analysis:**
```bash
python main.py
```

### Expected Input Format

The Excel file should contain stock data from Screener.in with columns such as:
- Company Name
- Market Cap
- Current Price
- P/E Ratio
- Dividend Yield
- ROE (Return on Equity)
- Debt to Equity
- Revenue Growth
- Profit Growth
- And other financial metrics

### Output

The script generates:

1. **Console Output**: Real-time analysis results
2. **Log Files**: `stock_analysis_YYYYMMDD.log`
3. **Analysis Reports**: `analysis_YYYYMMDD_HHMMSS.txt`

**Sample Output:**
```
================================================================================
STOCK ANALYSIS IN PROGRESS
================================================================================

Investment Recommendation: BUY

Entry Strategy:
- Current Price: ₹2,450
- Recommended Entry: ₹2,350-₹2,400 (on any dip)
- Accumulation Zone: ₹2,300-₹2,450

Exit Strategy:
- Target Price (6-12 months): ₹2,900-₹3,100
- Stop Loss: ₹2,150
- Expected Returns: 20-25%

Key Metrics Analysis:
- Strong ROE of 18.5%
- Consistent revenue growth of 15% YoY
- Healthy profit margins improving from 12% to 14%
- Low debt-to-equity ratio of 0.3

Risk Factors:
- Industry headwinds due to regulatory changes
- Competition increasing in core segments
- Valuation slightly above historical average

Confidence Level: 75% (Moderate-High)

Time Horizon: 6-12 months for medium-term gains

================================================================================
```

## ⚙️ Configuration

### Model Configuration

Modify the `ModelConfig` class in `main.py`:

```python
@dataclass
class ModelConfig:
    model_name: str = "stocker:latest"  # Your custom model
    temperature: float = 0.1            # Lower = more deterministic
    seed: int = 42                      # For reproducibility
    max_tokens: int = 2000              # Response length
    top_p: float = 0.9                  # Nucleus sampling
    top_k: int = 10                     # Top-k sampling
```

### Advanced Configuration

Create a `config.yaml` file for environment-specific settings:

```yaml
model:
  name: "stocker:latest"
  temperature: 0.1
  max_tokens: 2000
  seed: 42

files:
  input_dir: "./data"
  output_dir: "./results"
  log_dir: "./logs"

analysis:
  risk_threshold: 0.7
  min_confidence: 0.6
```

## 🔧 Troubleshooting

### Issue: Model not found
```bash
Error: model 'stocker:latest' not found
```
**Solution:**
```bash
ollama list  # Check available models
ollama create stocker:latest -f Modelfile  # Recreate model
```

### Issue: Excel file not loading
```bash
FileNotFoundError: File not found: ./3m.xlsx
```
**Solution:**
- Ensure the Excel file exists in the correct path
- Check file permissions
- Verify file format (.xlsx or .xls)

### Issue: Ollama not responding
```bash
Error: Failed to initialize
