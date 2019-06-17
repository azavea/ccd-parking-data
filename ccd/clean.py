import os

import click
import pandas as pd
from tqdm import tqdm

from ccd.parking_zone_evaluator import ParkingZoneEvaluator
from ccd.utils import read_layers_from_gdb


@click.command()
@click.argument('geodatabase')
@click.option('--test', is_flag=True)
def clean(geodatabase, test):
    layers = read_layers_from_gdb(geodatabase)
    pz = layers['Parking_Zones']
    pzr = layers['Parking_Zone_Regulations']
    pza = layers['Parking_Zones__ATTACH']

    pze = ParkingZoneEvaluator(pz, pzr, pza)

    all_dfs = []
    all_ids = pz['GlobalID'].values
    fname = 'output-all.csv'
    if test:
        all_ids = all_ids[0:50]
        fname = fname.replace('all', 'test')

    for id in tqdm(all_ids):
        all_dfs += pze.generate_base_shape_json(id)

    df = pd.concat(all_dfs)
    df.to_csv(os.path.join('data/output/', fname), index=False)


if __name__ == "__main__":
    clean()
