from datetime import date, timedelta

from typing import Dict

from app.market.services import get_max_volumes

DAY_1 = timedelta(days=1)
DAY_7 = timedelta(days=7)


class CachedData:
    # TODO: Not thread safe
    # TODO: Store avg values in DB
    def __init__(self, res: str):
        self.res: str = res
        self._max: Dict[date, int] = {}
        self._avg: Dict[date, float] = {}
        self.last_day: date = date.min
        self.query_and_update_data()

    def add_data(self, vol: int, day: date):
        """
        Add maximum volume data for given day to the cache and calculate average
        volume for that day from maximum volumes for previous 7 day.
        :param vol: Maximum volume for given day
        :param day: Day for which data is added
        """
        self._max[day] = vol
        if day >= self.last_day:
            self.last_day = day
        self._update_7d_avg(day)
        # if day < self.last_day:
        #     for d in range(day, self.last_day):
        #         self._update_7d_avg(d)

    def get_avg(self, day: date) -> float:
        if self.last_day != date.today() - DAY_1:
            self.query_and_update_data()
        return self._avg.get(day)

    def get_limit(self, day: date = None):
        if day:
            avg_data = self.get_avg(day)
            if not avg_data:
                return None
            result = {"date": str(day), "limit": int(avg_data / 4)}
        else:
            result = [{"date": str(k), "limit": int(v / 4)} for k, v in self._avg.items()]
        return result

    def _update_7d_avg(self, day: date):
        window_data = [v for k, v in self._max.items() if day - DAY_7 <= k < day]
        if len(window_data) > 0:
            self._avg[day] = sum(window_data) / len(window_data)

    def query_and_update_data(self):
        """
        Query from DB and update data cache for every day since already cashed(last_day) and to today.
        """
        yesterday = date.today() - DAY_1
        query = get_max_volumes(self.res, self.last_day, yesterday)
        if len(query) == 0:
            return
        # add queried data to cache
        for row in query:
            self.add_data(row.max, row.day)


class VolDataset:
    def __init__(self):
        self._data: Dict[str, CachedData] = {
            'wood': CachedData('wood'),
            'stone': CachedData('stone'),
            'food': CachedData('food'),
            'horses': CachedData('horses')
        }

    def get_limit(self, res: str, day: date = None):
        return self._data[res].get_limit(day)

    def get_avg(self, res: str, day: date):
        return self._data[res].get_avg(day)
