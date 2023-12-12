from datetime import datetime, timedelta

class Time():
    def __init__(self, datetime):
        self.time = datetime
    
    @classmethod
    def create_for_exact_datetime(cls, year, month, day, hours, minutes, seconds):
        time = datetime(year, month, day, hours, minutes, seconds)
        return Time(time)

    def advance_minutes(self, minutes):
        time_to_advance = timedelta(minutes=minutes)
        new_time = self.time + time_to_advance
        return Time(new_time)
    
    def passed_minutes(self, time, minutes):
        time_difference = self.time - timedelta(minutes=minutes) 
        return time_difference >= time.time