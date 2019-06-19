# CCD Street Inventory Data Cleaning

## Info
Additional data exploration info [here](data/README.md).

## Getting started
make sure `ParkingZones.gdb` is in `data/raw`  

run:
```
export GEODATABASE=data/raw/ParkingZones.gdb
python -m ccd.clean $GEODATABASE
```

for a test examples (processing only the first 50 segments), add the `--test` flag:
```
python -m ccd.clean $GEODATABASE --test
```

## Unit tests
To run all unit tests, run:

```
python -m unittest discover -s ccd/tests/ -p "test_*.py"
```