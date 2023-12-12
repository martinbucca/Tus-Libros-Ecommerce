from datetime import datetime
from src.utils.month_of_year import MonthOfYear
from src.utils.time import Time

class CurrentDateAndTimeProvider:
    def __init__(self) -> None:
        pass

    def current_month_of_year(self):
        current_datetime = self._current_datetime()
        return MonthOfYear.with_month_and_year(current_datetime.month, current_datetime.year)
    
    def current_time(self):
        current_datetime = self._current_datetime()
        return Time(current_datetime)
    
    def _current_datetime(self):
        return datetime.now()
