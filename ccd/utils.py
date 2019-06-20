from io import BytesIO

import numpy as np
import pandas as pd
from PIL import Image

import fiona
import geopandas as gpd
from ccd.constants import DTD, PERMIT_ZONE_DEFAULT


def byte_to_image(byte_image):
    return Image.open(BytesIO(byte_image))


def day_range(start_day, end_day):
    days = list(DTD.keys())

    if start_day == '888' or end_day == '888':
        return days[0:5]

    s = start_day.lower()[0:2]
    if start_day in ['1', '2', '3', '4', '5', '6', '7']:
        si = int(start_day) - 1
    elif s in days:
        si = days.index(s)
    else:
        si = None

    e = end_day.lower()[0:2]
    if end_day in ['1', '2', '3', '4', '5', '6', '7']:
        ei = int(end_day) - 1
    elif e in days:
        ei = days.index(e)
    else:
        ei = None

    if si is None and ei is None:
        return None
    if ei is None:
        ei = si
    if si is None:
        si = ei

    if si <= ei:
        return days[si:ei + 1]
    return days[si:] + days[:ei + 1]


def get_permit_zone(chars):
    # TODO: confirm this
    pz1 = chars['PermitZone1']
    pz2 = chars['PermitZone2']

    if not np.isnan(pz1):
        return pz1
    if not np.isnan(pz2):
        return pz2
    return PERMIT_ZONE_DEFAULT


def metering_to_paid(m):
    if not m:
        return None
    m = m.lower()

    mtp = {
        'no meters': 'No',
        'kiosk': 'Yes',
        'meters': 'Yes'
    }

    if m in mtp.keys():
        return mtp[m]

    return None


def read_layers_from_gdb(gdb_uri):
    layer_names = fiona.listlayers(gdb_uri)
    layers = {}
    for l in layer_names:
        df = gpd.read_file(gdb_uri, driver='FileGDB', layer=l)
        if df.geometry.isnull().all():
            df = pd.DataFrame(df).drop('geometry', 1)
        layers[l] = df

    return layers


def series_profile(series):
    name = series.name
    is_null = series.isnull().value_counts().to_dict()
    print(name)
    if True not in is_null.keys():
        print('No null values')
    elif False not in is_null.keys():
        print('All values are null')
        return
    else:
        print(
            '{} null values and {} non-null values'.format(is_null[True], is_null[False]))

    vc = series.value_counts().to_dict()
    print('{} unique values'.format(len(vc)))
    print('value counts: ')
    print(vc)


def shift_days(days):
    dows = list(DTD.keys())

    if days is None:
        return days

    for d in days:
        if d not in dows:
            raise Exception('{} not a valid day of the week'.format(d))

    if len(days) == len(dows):
        return days
    si = dows.index(days[0].lower()) + 1
    ei = dows.index(days[-1].lower()) + 1

    if si == 7:
        si = 0
    if ei == 7:
        ei = 0

    if ei < si:
        return dows[si:] + dows[0:ei + 1]
    return dows[si:ei + 1]


def show_image(image_df, id):
    b = image_df[image_df['REL_GLOBALID'] == id]['DATA']
    l = [byte_to_image(bb) for bb in b]
    if len(l) == 0:
        print('No images associated with this id')
        return None
    if len(l) == 1:
        return l[0].rotate(270)
    print('Multiple ({}) images'.format(len(l)))
    return l


def time_to_hm(time):
    if time == 9911:
        return 'all'

    if time == 9910:
        return 'school'

    if time > 2400 or time < 0:
        return None, None

    if len(str(time)) < 3:
        return 0, time

    h = int(str(time)[:-2])
    m = int(str(time)[-2:])
    return h, m


def validate_dow(dow):
    dow = str(dow)
    dow = dow[0:2].capitalize()

    dow_map = {
        '1': 'Mo',
        '2': 'Tu',
        '3': 'We',
        '4': 'Th',
        '5': 'Fr',
        '6': 'Sa',
        '7': 'Su',
    }

    if dow in dow_map.keys():
        dow = dow_map[dow]
    
    if dow in dow_map.values():
        return dow
    return None
