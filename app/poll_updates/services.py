from datetime import datetime

from app.market.services import get_raw_data


def get_update(from_datetime: datetime):
    filtered_res = ('wood', 'stone', 'food', 'horses')
    result = {}
    for res_name in filtered_res:
        new_data = get_raw_data(res_name, 10000, from_datetime)
        if new_data:
            result[res_name] = new_data
    return result
