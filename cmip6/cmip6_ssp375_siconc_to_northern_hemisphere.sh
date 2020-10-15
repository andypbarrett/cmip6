#!/bin/bash

EXPERIMENT="ssp370"

python siconc_to_northern_hemisphere.py $EXPERIMENT r1i1p1f1 --verbose
python siconc_to_northern_hemisphere.py $EXPERIMENT r2i1p1f1 --verbose
python siconc_to_northern_hemisphere.py $EXPERIMENT r3i1p1f1 --verbose
