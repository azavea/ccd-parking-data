# CCD Street Inventory Data Cleaning + CurbLR Feed

## Phase 1: Generate Hourly Parking Table

#### Info
Additional data exploration info [here](data/README.md).

#### Getting started
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

#### Unit tests
To run all unit tests, run:

```
python -m unittest discover -s ccd/tests/ -p "test_*.py"
```

## Phase 2: Generate CurbLR Dataset

#### Getting started

Requirements: [Docker](https://docs.docker.com/install/) 18+

Move the CCD curbs geojson (e.g. `CCD_curbs.geojson` to the `data` directory)

Run the linear referencing script:
`./scripts/linear_reference_all_radii.py --ccd_geoms=data/CCD_curbs.geojson --key=CCD_non-offset --max_radius=30`

In the example above:
- `data/CCD_curbs.geojson` is the input CCD geometry file
- `CCD_non-offset` specifies the name of the directory within `data` where the linear referencing output will be stored.
- `30` is the maximum radius that the linear referencing tool will search.

If you would like for the linear reference lines to be offset from the street centerline, add the offset parameter:

`./scripts/linear_reference_all_radii.py --ccd_geoms=data/CCD_curbs.geojson --key=CCD_non-offset --max_radius=30 --offset=5`

Build the Docker image:

`./docker/build`

Move the hourly parking table (i.e. `Parking_Regulations.csv`) and the regulation lookup JSON file (i.e. `reg_lookup.json`) to the data directory.

The script to generate the CurbLR data will take the following inputs:

- *segment_uri*: Path to original CCD geometries (`data/CCD_curbs.geojson`)
- *hour_table_uri*: Path to the hourly parking table (`data/Parking_Regulations.csv`)
- *linear_ref_dir*: Directory with linear reference output that you created in the linear referencing step (`data/CCD_non-offset/`)
- *reg_lookup_uri*: Path to regulation lookup JSON (`data/reg_lookup.json`)
- *output_key*: 'Name of directory to be created for all output (`CCD_CurbLR_non-offset`)

Run the Docker container:

`./docker/run`

This will open a console within the container. Run the command to generate the entire CurbLR dataset:
```
./scripts/generate_curblr.py \
    --segment_uri=data/CCD_curbs.geojson \
    --hour_table_uri=data/Parking_Regulations.csv \
    --linear_ref_dir=data/CCD_non-offset/ \
    --reg_lookup_uri=data/reg_lookup.json \
    --output_key=CCD_CurbLR_non-offset
```

When the script completes, you will be able to find the results in `data/CCD_CurbLR_non-offset/`