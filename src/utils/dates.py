from datetime import datetime


class UtilsDate:
    '''Utility class for date-related operations.'''

    def timestamp(self, date_format):
        '''Returns the current timestamp in the specified format.

        Args:
            date_format (str): The format string for the timestamp.

        Returns:
            str: The formatted current timestamp.
        '''
        return datetime.now().strftime(date_format)

    def first_day_month(self, date_format):
        '''Returns the first day of the current month in the specified format.

        Args:
            date_format (str): The format string for the date.

        Returns:
            str: The formatted date of the first day of the current month.
        '''
        now = datetime.now()
        return datetime(now.year, now.month, 1).strftime(date_format)
