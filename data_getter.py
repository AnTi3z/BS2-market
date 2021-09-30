from datetime import datetime

from peewee import fn, SQL

from db_models import PriceVolumeData, Resource


def get_raw_data(res_name: str, limit: int, from_datetime: datetime = None):
    # res_id = Resources.get(name=res_name)
    result = []
    select = PriceVolumeData.select(
        PriceVolumeData.ts,
        PriceVolumeData.price,
        PriceVolumeData.volume
    # ).where(PriceVolumeData.res == res_id)
    ).join(Resource).where(Resource.name == res_name)

    if from_datetime:
        select = select.where(PriceVolumeData.ts >= from_datetime)
        order = PriceVolumeData.ts
    else:
        order = PriceVolumeData.ts.desc()

    query = (select.order_by(order).limit(limit))

    for row in query:
        result.append({
            'date': row.ts.isoformat(),
            'price': row.price,
            'volume': row.volume
        })
    return result


def get_grouped_data(res_name: str, limit: int, group: int, from_datetime: datetime = None):
    res_id = Resource.get(name=res_name)
    result = []
    select = PriceVolumeData.select(
        fn.MIN(PriceVolumeData.ts).alias('ts_min'),
        fn.MAX(PriceVolumeData.ts).alias('ts_max'),
        fn.MIN(PriceVolumeData.volume).alias('vol_min'),
        fn.MAX(PriceVolumeData.volume).alias('vol_max'),
        fn.AVG(PriceVolumeData.price).alias('price_avg'),
        fn.FLOOR(PriceVolumeData.ts.to_timestamp() / group).alias('nterval')
    ).where(PriceVolumeData.res == res_id)

    if from_datetime:
        select = select.where(PriceVolumeData.ts >= from_datetime)
        order = SQL('ts_min')
    else:
        order = SQL('ts_min').desc()
        limit = limit + 1

    cte = (select.group_by(SQL('nterval')).order_by(order).limit(limit))

    ma = PriceVolumeData.alias()

    query = (cte
             .select_from((cte.c.nterval*group).alias('date_open'),
                          ((cte.c.nterval+1)*group).alias('date_close'),
                          cte.c.price_avg.alias('price'), cte.c.vol_min, cte.c.vol_max,
                          ma.volume.alias('vol_close'))
             .join(ma, on=((ma.ts == SQL('ts_max')) & (ma.res == res_id)))
             )

    if from_datetime:
        data = query.dicts()
    else:
        data = query.dicts()[::-1]

    vol_next_open = data[0]['vol_close']

    for row in data if from_datetime else data[1::]:
        row['price'] = int(row['price']*1000)/1000
        row['vol_open'] = vol_next_open
        vol_next_open = row['vol_close']
        row['date_open'] = datetime.utcfromtimestamp(row['date_open']).isoformat()
        row['date_close'] = datetime.utcfromtimestamp(row['date_close']).isoformat()
        result.append(row)

    return result


def get_update(from_datetime: datetime):
    # res_names = {1: 'wood', 2: 'stone', 3: 'food', 4: 'horses'}
    # Resources.get(id=i)
    filtred_res = ('wood', 'stone', 'food', 'horses')
    result = {}
    for res_name in filtred_res:
        new_data = get_raw_data(res_name, 10000, from_datetime)
        if new_data:
            result[res_name] = new_data
    return result
