"""
Module for fetching option data from external APIs
"""

from typing import Optional

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOptionContractsRequest
from alpaca.trading.enums import AssetStatus
from alpaca.data.historical import OptionHistoricalDataClient
from alpaca.data.requests import OptionLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockLatestTradeRequest
import pandas as pd

class OptionFetcher:
    """Class to handle API calls and option data retrieval"""
    
    def __init__(self, api_key: str, secret_key: str):
        if not api_key or not secret_key:
            raise ValueError("API Key and Secret Key required")
        self.api_key = api_key
        self.secret_key = secret_key
        self.trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=True)
        self.option_historical_client = OptionHistoricalDataClient(api_key=api_key, secret_key=secret_key)
        self.stock_historical_client = StockHistoricalDataClient(api_key=api_key, secret_key=secret_key)

    def fetch_options_contracts(self, 
                      symbol: list, 
                      expiration_date: Optional[str] = None,
                      strike_price_gte: Optional[float] = None,
                      strike_price_lte: Optional[float] = None,
                      option_type=None,
                      limit: int = 100,
    ):
        """Fetch options data for a given symbol and expiration date"""
        req = GetOptionContractsRequest(
            underlying_symbols = symbol,              
            status = AssetStatus.ACTIVE,                          
            expiration_date = expiration_date,                                
            expiration_date_gte = None,                            # we can pass date object
            expiration_date_lte = None,                            # or string (YYYY-MM-DD)
            root_symbol = None,                                    # specify root symbol
            type = option_type,                                           # specify option type (ContractType.CALL or ContractType.PUT)
            style = None,                                          # specify option style (ContractStyle.AMERICAN or ContractStyle.EUROPEAN)
            strike_price_gte = strike_price_gte,                               # specify strike price range
            strike_price_lte = strike_price_lte,                               # specify strike price range
            limit = limit,                                             # specify limit
            page_token = None,                                     # specify page token
        )
        return self.trade_client.get_option_contracts(req)
    
    def get_option_prices(self, contract_symbols: list, chunk_size: int = 100):
        all_quotes = {}

        for i in range(0, len(contract_symbols), chunk_size):
            chunk = contract_symbols[i:i + chunk_size]
            resp = self.option_historical_client.get_option_latest_quote(
                OptionLatestQuoteRequest(symbol_or_symbols=chunk)
            )

            if isinstance(resp, dict):
                all_quotes.update(resp)
            else:
                for sym, quote in resp.items():
                    all_quotes[sym] = quote

        return all_quotes
    
    def get_spot_price(self, symbol : str):
        request = StockLatestQuoteRequest(symbol_or_symbols=[symbol])
        response = self.stock_historical_client.get_stock_latest_quote(request)
        quote = response[symbol]

        if quote.bid_price and quote.ask_price and quote.ask_price > 0:
            return (quote.bid_price + quote.ask_price) / 2

        trade_request = StockLatestTradeRequest(symbol_or_symbols=[symbol])
        trade_response = self.stock_historical_client.get_stock_latest_trade(trade_request)
        return trade_response[symbol].price
    
    def build_options_df(self, symbol : str, expiration_dates : list, spot_delta : int, n_contracts : int):
        spot = self.get_spot_price(symbol)
        lower_bound = str(spot-spot_delta)
        upper_bound = str(spot+spot_delta)

        contracts = []
        for exp in expiration_dates:
            resp = self.fetch_options_contracts(
                symbol=[symbol],
                expiration_date=exp,
                strike_price_gte=lower_bound,
                strike_price_lte=upper_bound,
                limit=n_contracts,
            )

            if resp and getattr(resp, "option_contracts", None):
                contracts.extend(resp.option_contracts)

        contract_symbols = [c.symbol for c in contracts]
        if not contract_symbols:
            return pd.DataFrame([])
        
        quotes = self.get_option_prices(contract_symbols)

        data = []
        for contract in contracts:
            s = contract.symbol
            # quotes peut être un dict-like ; utiliser .get pour éviter KeyError
            quote = quotes.get(s) if hasattr(quotes, "get") else quotes[s] if s in quotes else None
            if quote is None:
                continue

            bid = getattr(quote, "bid_price", 0.0) or 0.0
            ask = getattr(quote, "ask_price", 0.0) or 0.0

            # filtrer les instruments illiquides ou quotes invalides
            if bid <= 0 or ask <= bid:
                continue

            typ = None
            if hasattr(contract, "type") and contract.type is not None:
                typ = getattr(contract.type, "value", None) or contract.type.name.lower()
            else:
                typ = getattr(contract, "contract_type", None)

            mid = (bid + ask) / 2

            data.append({
                "symbol": s,
                "strike": getattr(contract, "strike_price", None),
                "expiry": getattr(contract, "expiration_date", None),
                "type": typ,
                "bid": bid,
                "ask": ask,
                "mid": mid,
                "spread": ask - bid,
                "timestamp": getattr(quote, "timestamp", None),
            })

        return pd.DataFrame(data)

