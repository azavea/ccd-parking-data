import click

from utils import read_layers_from_gdb
from parking_zone_evaluator import ParkingZoneEvaluator

@click.command()
@click.argument('geodatabase')
def clean(geodatabase):
    layers = read_layers_from_gdb(geodatabase)
    pz = layers['Parking_Zones']
    pzr = layers['Parking_Zone_Regulations']
    pza = layers['Parking_Zones__ATTACH']

    pze = ParkingZoneEvaluator(pz, pzr, pza)

    sample_uuid = '{8EDBF341-6399-4A77-B90E-D4E34425145E}'
    parking_hours = pze.generate_base_shape_json(sample_uuid)
    print(parking_hours)

if __name__ == "__main__":
    clean()