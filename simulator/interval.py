import datetime
import calendar

class interval:
    def __init__(self, timeframe):
        if timeframe in ["1s", "1m", "1h", "1d", "1w"]:
            self.timeframe = timeframe
            self.set_timedelta()
        else:
            raise Exception("Invalid Timeframe. Must be 1s, 1m, 1h, 1d, 1w")
    
    @staticmethod
    def get_epoch_time(timestamp: datetime.datetime):
        return int(calendar.timegm(timestamp.utctimetuple()))
    
    def set_timedelta(self):
        if self.timeframe == "1s":
            self.timedelta = datetime.timedelta(seconds=1)
        elif self.timeframe == "1m":
            self.timedelta = datetime.timedelta(minutes=1)
        elif self.timeframe == "1h":
            self.timedelta = datetime.timedelta(hours=1)
        elif self.timeframe == "1d":
            self.timedelta = datetime.timedelta(days=1)
        elif self.timeframe == "1w":
            self.timedelta = datetime.timedelta(weeks=1)
