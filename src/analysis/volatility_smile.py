"""
Module for volatility smile analysis and calculations
"""

from math import log, sqrt, exp
from scipy.stats import norm
from scipy.optimize import brentq
from datetime import datetime, timezone, time
import pandas as pd

class VolatilitySmileAnalyzer:
    """Class to analyze volatility smile from option data"""
    
    def __init__(self, options_data, spot_price, risk_free_rate):
        """Initialize the analyzer with options data"""
        self.options_data = options_data
        self.spot_price = spot_price
        self.risk_free_rate = risk_free_rate

    def get_time_to_expiry(self, expiry_timestamp):
        now = datetime.now(timezone.utc)

        if isinstance(expiry_timestamp, datetime):
            expiry_datetime = expiry_timestamp
            if expiry_datetime.tzinfo is None:
                expiry_datetime = expiry_datetime.replace(tzinfo=timezone.utc)
        else:
            expiry_datetime = datetime.combine(expiry_timestamp, time(16, 0), tzinfo=timezone.utc)

        return max((expiry_datetime - now).total_seconds() / (365.25 * 24 * 3600), 0)
    
    def calculate_implied_volatility(self, option_price: float, spot_price: float, 
                                    strike: float, time_to_expiry: float, 
                                    risk_free_rate: float, option_type: str):
        """Calculate implied volatility using Black-Scholes model"""
        if option_price <= 0 or spot_price <= 0 or strike <= 0 or time_to_expiry <= 0:
            return None

        # Black-Scholes formula
        def black_scholes_price(vol):
            d1 = (log(spot_price / strike) + (risk_free_rate + 0.5 * vol**2) * time_to_expiry) / (vol * sqrt(time_to_expiry))
            d2 = d1 - vol * sqrt(time_to_expiry)

            if option_type.lower() == "call":
                return spot_price * norm.cdf(d1) - strike * exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
            else:
                return strike * exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)

        # Difference between theoretical B-S price and real price
        def objective(vol):
            return black_scholes_price(vol) - option_price

        try:
            # Since there is no analytical solution for sigma, we test a wide range of values
            # until we find the one that makes the difference between the price given by 
            # the B-S formula and the real price equal to 0. 
            return brentq(objective, 1e-6, 5.0)
        except ValueError:
            return None
    
    def build_smile_data(self):
        """Build the volatility smile data"""
        implied_vols = []
        strikes = []
        tte = []
        expiration_dates = []
        moneyness = []
        option_type = []
        for row in self.options_data.itertuples():
            iv = self.calculate_implied_volatility(
                option_price=row.mid,
                spot_price=self.spot_price,
                strike=row.strike,
                time_to_expiry=self.get_time_to_expiry(row.expiry),
                risk_free_rate=self.risk_free_rate,
                option_type=row.type,
            )

            if iv is not None:
                strikes.append(row.strike)
                implied_vols.append(iv)
                tte.append(self.get_time_to_expiry(row.expiry))
                expiration_dates.append(row.expiry)
                moneyness.append(row.strike / self.spot_price)
                option_type.append(row.type)

        if not strikes:
            print("No IV to plot")
            return

        return pd.DataFrame({"implied_vol" : implied_vols, "strike" : strikes, "expiration_date" : expiration_dates, "time_to_expiry" : tte, "moneyness" : moneyness, "type" : option_type})
        
    
    def fit_smile_model(self, model_type: str = 'spline'):
        """Fit a model to the volatility smile"""
        pass
