################################################################
#                                                              #
#  Michael Adams - Satellite Data Anomaly Detection            #
#                                                              #
################################################################

# find list of filenames in data dirs
# generate list of strings with sat names
# get user input for satellite name
# check against list
# ask about for telem selection
# load data based on selection - efficient
# search telem channel for anomalous conditions as defined by error threshold

import os
from pathlib import Path
import pandas as pd

#TODO: note the inefficiency of loading all sats

# directory info
sat_telem_dir = Path('sat_telem')
#sats = [os.path.splitext(filename)[0] for filename in os.listdir(sat_telem_dir)]

# build dict with sat_name : DataFrame pairs
sats = {os.path.splitext(filename)[0]: pd.read_csv(sat_telem_dir/filename) for filename in os.listdir(sat_telem_dir)}
# build dict with [s]at_name : sat_name for user convenience 
sats_char = {sat[0]: sat for sat in sats}
print(sats.keys())
print(sats_char)

print("\n####################################")
print("# Satellite Anomaly Detection Util #")
print("####################################\n")

# get satellite
do = True
while do:
    print("Satellites:")
    [print(f"{key}: {value}") for key, value in sats_char.items()]
    char = input("Enter char of satellite or 'q' to quit: ")

    if (char == 'q'):
        quit()

    if (char in sats_char.keys()):
        do = False

    print()
print(f"Satellite: {sats_char[char].upper()}\n")

# extract selected satellite for convenience
sat = sats[sats_char[char]]

# build dict with [t]elem_channe[l] : telem_channel for user convenience
telem_char = {f"{col[0]}{col[-1]}": col for col in sat}

# select telem channel
do = True
while do:
    print("Telemetry Channels:")
    [print(f"{key}: {value}") for key, value in telem_char.items()]
    char = input("Select telemetry channel or enter 'q' to quit: ")

    if (char == 'q'):
        quit()

    if (char in telem_char.keys()):
        do = False

    print()

print(f"Telem Channel: {telem_char[char].upper()}\n")

# access with sat[telem_char[char]]
