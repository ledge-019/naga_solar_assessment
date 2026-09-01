import calendar
from datetime import date

year = 2026

for month in range(1, 13):

    ndays = calendar.monthrange(year, month)[1]
    print(ndays)