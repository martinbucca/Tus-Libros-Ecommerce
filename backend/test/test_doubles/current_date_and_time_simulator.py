class CurrentDateAndTimeSimulator:
    def __init__(self, month_of_year, time) -> None:
        self.month_of_year = month_of_year
        self.time = time

    @classmethod
    def create_with_month_of_year(cls, month_of_year):
        return CurrentDateAndTimeSimulator(month_of_year, None)
    
    @classmethod
    def create_with_time(self, time):
        return CurrentDateAndTimeSimulator(None, time)
    
    @classmethod
    def create_with_month_of_year_and_time(cls, month_of_year, time):
        return CurrentDateAndTimeSimulator(month_of_year, time)

    def current_month_of_year(self):
        return self.month_of_year

    def current_time(self):
        return self.time

    def advance_minutes(self, minutes):
        self.time = self.time.advance_minutes(minutes)