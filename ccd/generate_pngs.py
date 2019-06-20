import os

import click
import numpy as np
from tqdm import tqdm

from ccd.utils import byte_to_image, read_layers_from_gdb


@click.command()
@click.argument('geodatabase')
@click.option('--test', is_flag=True)
@click.option('--replace', is_flag=True)
def generate_pngs(geodatabase, test, replace):
    layers = read_layers_from_gdb(geodatabase)
    pza = layers['Parking_Zones__ATTACH']
    all_ids = np.unique(pza['REL_GLOBALID'].values)

    if test:
        all_ids = all_ids[0:5]

    output_dir = 'data/output/images/'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for id in tqdm(all_ids):
        rows = pza[pza['REL_GLOBALID'] == id]
        id_str = id.replace('{', '').replace('}', '')
        byte_images = list(rows['DATA'].values)
        for i, bi in enumerate(byte_images):
            fname = '{}.png'.format(id_str)
            if len(byte_images) > 1:
                fname = '{}-{}.png'.format(id_str, i)
            out_uri = os.path.join(output_dir, fname)
            if replace or not os.path.isfile(out_uri):
                im = byte_to_image(bi).rotate(270)
                im.save(out_uri, 'png')
        

if __name__ == "__main__":
    generate_pngs()
