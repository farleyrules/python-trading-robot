from datetime import datetime
from datetime import timedelta

import pandas as pd
import pandas_market_calendars as mcal

class MarketHours():

    def __init__(self) -> None:

        """ 
        The code was added below to obtain market hours data from the NYSE
        
        Pip Install: pip install pandas_market_calendars
        Github site: https://github.com/rsheftel/pandas_market_calendars
        Github usage: https://github.com/rsheftel/pandas_market_calendars/blob/master/examples/usage.ipynb
        
        The calendar for the NYSE is obtained 
        The calendar only contains actual days the market is open
        The calendar does not include weekends and holidays
        """
        self.nyse = mcal.get_calendar('NYSE')
        
        # The market date, which is tested, is for today
        self.market_date = datetime.today().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        # The hours of the market are returned in a Pandas DataFrame
        # The market open and market close are included for today
        self.hours = self.nyse.schedule(start_date=self.market_date, end_date=self.market_date)

        self.right_now = datetime.utcnow().timestamp()

        if len(self.hours.index) > 0:
            
            # Market open is the value in the market_open column
            self.market_open_column = self.hours['market_open']
            self.market_open = self.market_open_column[0].to_pydatetime()
            self.market_open_time = self.market_open.timestamp()
            
            # Market close is the value in the market_close column
            self.market_close_column = self.hours['market_close']
            self.market_close = self.market_close_column[0].to_pydatetime()
            self.market_close_time = self.market_close.timestamp()

            # Pre-Market opens 5 hours 30 minutes prior to the regular market
            self.pre_market_open = self.market_open - timedelta(hours=5, minutes=30)
            self.pre_market_open_time = self.pre_market_open.timestamp()

            # Post-Market remaines open 4 hours after the regular market
            self.post_market_close = self.market_close + timedelta(hours=4)
            self.post_market_close_time = self.post_market_close.timestamp()

        else:
            # Without a market open and close, the market will not be open at all today
            # All variables are set to the begining of the next day (1 day)
            self.market_open_time = self.market_date + timedelta(days=1)
            self.market_close_time = self.market_open_time
            self.pre_market_open_time = self.market_open_time
            self.post_market_close_time = self.market_open_time

    @property
    def regular_market_open(self) -> bool:
        
        market_open_time = self.market_open_time
        market_close_time = self.market_close_time
        right_now = self.right_now

        if market_open_time <= right_now <= market_close_time:
            return True
        else:
            return False

    @property
    def pre_market_open(self) -> bool:
        
        pre_market_open_time = self.pre_market_open_time
        pre_market_close_time = self.market_open_time
        right_now = self.right_now

        if pre_market_open_time <= right_now <= pre_market_close_time:
            return True
        else:
            return False

    @property
    def post_market_open(self) -> bool:
        
        post_market_open_time = self.market_close_time
        post_market_close_time = self.post_market_close_time
        right_now = self.right_now

        if post_market_open_time <= right_now <= post_market_close_time:
            return True
        else:
            return False
