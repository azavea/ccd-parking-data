# CCD Street Inventory Data Cleaning

## Info
Additional data exploration info [here](data/README.md).

## Getting started
make sure `ParkingZones.gdb` is in `data/raw`  

run:
```
export GEODATABASE=data/raw/ParkingZones.gdb
python ccd/clean.py $GEODATABASE
```