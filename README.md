# Volatility Smile Analyzer

An application to fetch option prices via an API, analyze the volatility smile, and visualize the data in 2D and 3D.

## Description

This project enables you to:
- Fetch current option prices from the Alpaca API
- Calculate and analyze the volatility smile
- Visualize the volatility smile in 2D and 3D

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone the repository
```bash
git clone https://github.com/etiennevzn/VolatilitySmileAnalyzer.git
cd volatility_smile
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your API and Secret keys and any other settings
```

## Usage

Configure parameters and run the analysis notebook:

Open and run the `vol_smile.ipynb` Jupyter notebook to configure parameters and execute the volatility-smile algorithms (recommended in JupyterLab or VS Code):

```bash
# from the project root, open the notebook in JupyterLab
jupyter lab vol_smile.ipynb
# or open in VS Code
code vol_smile.ipynb
```

## Project structure

```
volatility_smile/
├── src/                 # Main source code
│   ├── api/             # Module to fetch data from APIs
│   └── analysis/        # Volatility smile analysis
├── config/              # Configuration and settings
├── requirements.txt     # Dependencies
├── .env.example         # Example .env file
├── .gitignore           # Files to ignore in Git
└── README.md            # Documentation
```

## Configuration

See `.env.example` for required configuration (API key, etc.).

## API support

This project currently only supports the Alpaca API. If you want to use another API, edit the volatility_smile.py and option_fetcher.py files. 

## License

MIT [LICENSE](LICENSE)
