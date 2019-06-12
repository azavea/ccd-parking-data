from io import BytesIO

import numpy as np
import pandas as pd
from PIL import Image

import fiona
import geopandas as gpd


def byte_to_image(byte_image):
    return Image.open(BytesIO(byte_image))

def get_permit_zone(chars):
    # TODO: confirm this
    pz1 = chars['PermitZone1']
    pz2 = chars['PermitZone2']
    pe = chars['PermitException']
    
    def _a(b):
        if np.isnan(b):
            return 'none'
        return str(b)
    
    return '{}|{}|{}'.format(_a(pz1), _a(pz2), pe.lower())

def metering_to_paid(m):
    if not m:
        return None
    
    mtp = {
        'No Meters': 'No',
        'Kiosk': 'Yes',
        'Meters': 'Yes'
    }
    
    return mtp[m]

def read_layers_from_gdb(gdb_uri):
    layer_names = fiona.listlayers(gdb_uri)
    layers = {}
    for l in layer_names:
        df = gpd.read_file(gdb_uri, driver='FileGDB', layer=l)
        if df.geometry.isnull().all():
            df = pd.DataFrame(df).drop('geometry', 1)
        layers[l] = df
        
    return layers

def validate_dow(dow):
    if dow in ['888', '999', 'N/A']:
        return None
    
    if dow.endswith('day'):
        return dow[0:2]
    
    dow_map = {
        '1':'Mo',
        '2':'Tu',
        '3':'We',
        '4':'Th',
        '5':'Fr',
        '6':'Sa',
        '7':'Su',
    }
    
    try:
        return dow_map[dow]
    except KeyError:
        print('Unknown day value')
