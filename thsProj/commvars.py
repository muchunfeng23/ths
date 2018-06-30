#coding=utf-8

from datetime import datetime, timedelta
import time
import calendar


class StrDate(object):
    """
    日期处理
    主要是获得当前时间以及delta时间
    """

    def __init__(self, dt):
        self._dt = dt

    @classmethod
    def now(cls):
        """Like datetime.now, except microsecond
        """
        return cls(datetime.fromtimestamp(int(time.time())))
    
    @classmethod
    def fromtimestamp(cls, ts):
        return cls(datetime.fromtimestamp(ts))

    @classmethod
    def fromdatekey(cls, datekey):
        return cls(datetime.strptime(str(datekey), '%Y%m%d'))

    def format(self, format):
        return self._dt.strftime(format)
    
    def strftime(self, format):
        return self._dt.strftime(format)
    
    @property
    def date(self):
        return self._dt.strftime("%Y-%m-%d")
    
    @property
    def time(self):
        return self._dt.strftime("%H:%M:%S")

    @property
    def datetime(self):
        return self._dt.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def datekey(self):
        return self._dt.strftime("%Y%m%d")

    @property
    def hour(self):
        return self._dt.hour

    @property
    def minute(self):
        return self._dt.minute

    @property
    def hm(self):
        return "%s%s" % (str(self._dt.hour), (str((self._dt.minute/30)*30) if len(str((self._dt.minute/30)*30)) == 2 else "00"))

    @property
    def second(self):
        return self._dt.second

    @property
    def year(self):
        return self._dt.year

    @property
    def month(self):
        return self._dt.month

    @property
    def yearmo(self):
        return self._dt.strftime("%Y%m")

    @property
    def day(self):
        return self._dt.day             

    @property
    def datestamp(self):
        tuple = self._dt.date().timetuple()
        return int(time.mktime(tuple))

    @property
    def timestamp(self):
        tuple = self._dt.timetuple()
        return int(time.mktime(tuple))

    def delta(self, *args, **kwargs):
        newdate = self._dt

        # If months is None, return 0 instead.
        month = newdate.month - int(kwargs.pop('months', 0))

        year = int(kwargs.pop('years', 0)) - month / 12 + (month % 12 == 0)

        # We can get the correct target month, even it is negative value.
        month = month % 12 + (month % 12 == 0) * 12
        year = newdate.year - year
        day = min(newdate.day, calendar.monthrange(year, month)[1])
        newdate = newdate.replace(year=year, month=month, day=day)
        return self.__class__(newdate - timedelta(*args, **kwargs))

    @property
    def month_begin_date(self):
        return self.__class__(self._dt.replace(day=1))
    
    @property
    def month_end_date(self):
        end_date = calendar.monthrange(self._dt.year, self._dt.month)[1]
        return self.__class__(self._dt.replace(day=end_date))
    
    @property
    def week_begin_date(self):
        return self.__class__(self._dt - timedelta(days=self._dt.weekday()))
    
    @property
    def week_end_date(self):
        return self.__class__(self._dt + timedelta(days=7-self._dt.weekday()-1))
    
    def delta_old(self, *args, **kwargs):
        return self.__class__(self._dt - timedelta(*args, **kwargs))

    def __sub__(self, start_date):
        return self._dt - start_date._dt

    def __repr__(self):
        return self.datetime


code = """
now = StrDate.now()
"""
def get_commvars():
    vars = {}
    exec (code.replace('\r\n', '\n') in globals(), vars)
    return vars

now = StrDate.now()

if __name__ == '__main__':
    now = StrDate.now()
    print (now.datetime)
