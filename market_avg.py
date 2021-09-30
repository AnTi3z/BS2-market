from datetime import date, timedelta

from peewee import fn, SQL
from typing import Dict, List

from db_models import PriceVolumeData, Resource

DAY_1 = timedelta(days=1)
DAY_7 = timedelta(days=7)


class Data:
    def __init__(self):
        self._max: Dict[date, int] = {}
        self._avg: Dict[date, float] = {}
        self.last_day: date = date.min

    def _window_prev_7d(self, day: date) -> List[int]:
        return [v for k, v in self.max.items() if day - DAY_7 <= k < day]

    @property
    def max(self):
        return self._max

    @property
    def avg(self):
        return self._avg

    def update_7d_avg(self, day: date = None):
        if day is None:
            day = self.last_day + DAY_1
        window_data = self._window_prev_7d(day)
        if len(window_data) > 0:
            self.avg[day] = sum(window_data) / len(window_data)


class VolDataset:
    def __init__(self):
        self._data = {'wood': Data(), 'stone': Data(), 'food': Data(), 'horses': Data()}

    def get_limit(self, res: str, day: date = None):
        avg_data = self.get_avg(res, day)
        if not avg_data:
            return None

        if day:
            result = {"date": str(day), "limit": int(avg_data / 4)}
        else:
            result = [{"date": str(k), "limit": int(v / 4)} for k, v in avg_data.items()]
        return result

    def get_avg(self, res: str, day: date = None):
        res_data = self._data[res]
        if res_data.last_day != date.today() - DAY_1:
            self._update_dataset(res)
        return res_data.avg.get(day) if day else res_data.avg

    def get_max(self, res: str, day: date = None):
        res_data = self._data[res]
        if res_data.last_day != date.today() - DAY_1:
            self._update_dataset(res)
        return res_data.max.get(day) if day else res_data.max

    def _update_dataset(self, res: str):
        res_id = Resource.get(name=res)
        res_data = self._data[res]

        query = (PriceVolumeData
                 .select(fn.DATE(PriceVolumeData.ts).alias('day'), fn.MAX(PriceVolumeData.volume).alias('max'))
                 .where(PriceVolumeData.res == res_id)
                 .where(fn.DATE(PriceVolumeData.ts) >= res_data.last_day)
                 .where(fn.DATE(PriceVolumeData.ts) <= date.today() - DAY_1)
                 .group_by(SQL('day'))
                 .order_by(SQL('day'))
                 )

        if len(query) == 0:
            return

        # update max dataset with new data
        for row in query:
            res_data.max[row.day] = row.max

        # if dataset is new then set last_day to first record of new data
        if res_data.last_day == date.min:
            res_data.last_day = query[0].day

        # Update avg for each day from self._data[res].last_day to query[-1].day
        while res_data.last_day <= query[-1].day:
            res_data.update_7d_avg()  # for day = last_day + 1
            res_data.last_day += DAY_1
