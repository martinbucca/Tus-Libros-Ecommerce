class MonthOfYear:
    def __init__(self, month, year):
        self.month = month
        self.year = year
    
    @classmethod
    def with_month_and_year(cls, month, year):
        return MonthOfYear(month, year)
    
    @classmethod
    def invalid_month_of_year_string_error_message(cls):
        return "Can not convert string to month of year"

    @classmethod
    def create_from_string(cls, month_of_year):
        cls._validate_month_of_year(month_of_year)
        month = int(month_of_year[:2])
        year = int(month_of_year[2:])
        cls._validate_month(month)
        return MonthOfYear.with_month_and_year(month, year)

    @classmethod
    def _validate_month_of_year(cls, month_of_year):
        if (len(month_of_year) != 6):
            raise ValueError(cls.invalid_month_of_year_string_error_message())

    @classmethod
    def _validate_month(cls, month):
        if (month < 1 or month > 12):
            raise ValueError(cls.invalid_month_of_year_string_error_message())

    def is_before(self, month_of_year):
        return self.year < month_of_year.year or (self.year == month_of_year.year and self.month < month_of_year.month)
    
    def one_month_after(self):
        if (self.month == 12):
            return MonthOfYear.with_month_and_year(1, self.year + 1)
        return MonthOfYear.with_month_and_year(self.month + 1, self.year)
    
    def one_month_before(self):
        if (self.month == 1):
            return MonthOfYear.with_month_and_year(12, self.year - 1)
        return MonthOfYear.with_month_and_year(self.month - 1, self.year)
