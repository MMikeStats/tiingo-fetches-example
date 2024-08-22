from tiingo import TiingoClient
from datetime import datetime, timedelta, time
import pandas as pd
import pytz

class TiingoDataFetcher:
    def __init__(self, api_key):
        self.config = {
            'session': True,
            'api_key': api_key
        }
        self.client = TiingoClient(self.config)

    def get_last_n_market_days(self, n):
        """Retrieve the last n market days."""
        now = datetime.now(pytz.utc)
        market_days = []
        while len(market_days) < n:
            now -= timedelta(days=1)
            if now.weekday() < 5:  # Monday=0, Friday=4
                market_days.append(now.date().isoformat())
        return market_days
    
    def get_last_n_days_till_today(self, n):
        """Retrieve the last n market days including today if it's a market day, working in UTC."""
        now = datetime.now(pytz.utc)
        market_days = []
        
        # Start with today in UTC
        current_date = now.date()
        while len(market_days) < n:
            if current_date.weekday() < 5:  # Monday=0, Friday=4
                market_days.append(current_date.isoformat())
            # Create a timezone-aware minimum time for comparison
            market_open_time = datetime.combine(current_date, time.min).replace(tzinfo=pytz.utc)
            if current_date == now.date() and now < market_open_time:
                break  # If it's before market open, we don't count today as a market day yet
            current_date -= timedelta(days=1)
        
        # If today should be included but we've already passed it, add it now
        if now.date().isoformat() not in market_days and now.date().weekday() < 5:
            market_days.append(now.date().isoformat())

        return market_days

    def get_ohlc(self, ticker, start_date, end_date, frequency):
        """Fetch OHLC data for a given ticker, date range, and frequency."""
        return self.client.get_dataframe(ticker, 
                                         startDate=start_date, 
                                         endDate=end_date,
                                         frequency=frequency)

    def fetch_data(self, ticker, n_days, frequency):
        """Fetch data for the last n market days with specified frequency."""
        market_days = self.get_last_n_days_till_today(n_days)
        all_data = pd.DataFrame()
        
        for date in market_days:
            print(date)
            try:
                data = self.get_ohlc(ticker, date, date, frequency)
                if not data.empty:
                    all_data = pd.concat([all_data, data])
                else:
                    print(f"No data for {date}")
            except Exception as e:
                print(f"Failed to get data for {date}: {e}")

        if not all_data.empty:
            if all_data.index.tz is None:
                all_data.index = all_data.index.tz_localize('UTC')
            
            all_data = all_data[['open', 'high', 'low', 'close']].reset_index()
            all_data = all_data.rename(columns={'date': 'time'}).sort_values('time')
            
        return all_data
