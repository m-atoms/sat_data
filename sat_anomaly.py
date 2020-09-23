################################################################
#                                                              #
#  Michael Adams - Satellite Data Anomaly Detection            #
#                                                              #
################################################################

import os
import time
from pathlib import Path
import pandas as pd
from SAT_LIMIT_CONDITIONS import WHEEL_SATURATION, GYRO_SPIN, LOW_VOLTAGE
from SAT_ANOMALY_CONDITIONS import WHEEL_SATURATION_LIMIT, GYRO_SPIN_LIMIT, LOW_VOLTAGE_LIMIT

##################################
# Get Sat From User
##################################
def get_sat(sats_char):
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

    return char

##################################
# Get Channel From User
##################################
def get_channel(telem_char):

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

    return char

##################################
# Compute Limit Occurrence
##################################
def compute_limit_occurrence(channel, limit_condition):
    size = channel.size
    lim = channel[abs(channel) >= limit_condition]
    lim_size = lim.size
    lim_occurrence = lim_size / size * 100
    return lim_occurrence

#########################################
# Check User Selected Channel for Anomaly 
#########################################
def sat_anomaly(sats):

    print("\n####################################")
    print("# Satellite Anomaly Detection Util #")
    print("####################################\n")

    # build dict with [s]at_name : sat_name for user convenience 
    sats_char = {sat[0]: sat for sat in sats}

    # get sat from user
    selected_sat = get_sat(sats_char)

    # extract selected satellite for convenience
    sat = sats[sats_char[selected_sat]]

    # build dict with [t]elem_channe[l] : telem_channel for user convenience
    telem_char = {f"{col[0]}{col[-1]}": col for col in sat}

    # get channel from user
    selected_channel = get_channel(telem_char)

    # start timer after user input
    start_time = time.time()
    
    # use low voltage channel for bus voltage anomaly detection
    if (selected_channel == 'be'):
        selected_channel = 'le'

    # extract selected channel for convenience
    channel = sat.loc[:,telem_char[selected_channel]]

    # compute limit occurrence and compare against threshold tolerance
    if (selected_channel == 'tp'):
        print("--- anomaly_detect: %s seconds ---" % (time.time() - start_time))
        print("no anomaly condition identified for timestamp")
        return False
    elif (selected_channel == 'gx' or selected_channel == 'gy' or selected_channel == 'gz'):
        limit_occurrence = compute_limit_occurrence(channel, GYRO_SPIN)

        print(f"limit occurrence calculation: {limit_occurrence:.4f}%\nlimit occurrence threshold:   {GYRO_SPIN_LIMIT:.4f}%\n")

        if (limit_occurrence > GYRO_SPIN_LIMIT):
            print("--- anomaly_detect: %s seconds ---" % (time.time() - start_time))
            return True
        else:
            print("--- anomaly_detect: %s seconds ---" % (time.time() - start_time))
            return False
    elif (selected_channel == 'ws' or selected_channel == 'wx' or selected_channel == 'wy' or selected_channel == 'wz'):
        limit_occurrence = compute_limit_occurrence(channel, WHEEL_SATURATION)

        print(f"limit occurrence calculation: {limit_occurrence:.4f}%\nlimit occurrence threshold:   {WHEEL_SATURATION_LIMIT:.4f}%\n")

        if (limit_occurrence > WHEEL_SATURATION_LIMIT):
            print("--- anomaly_detect: %s seconds ---" % (time.time() - start_time))
            return True
        else:
            print("--- anomaly_detect: %s seconds ---" % (time.time() - start_time))
            return False
    elif (selected_channel == 'le' or selected_channel == 'be'):
        limit_occurrence = compute_limit_occurrence(channel, LOW_VOLTAGE)

        print(f"limit occurrence calculation: {limit_occurrence:.4f}%\nlimit occurrence threshold:   {LOW_VOLTAGE_LIMIT:.4f}%\n")

        if (limit_occurrence > LOW_VOLTAGE_LIMIT):
            print("--- anomaly_detect: %s seconds ---" % (time.time() - start_time))
            return True
        else:
            print("--- anomaly_detect: %s seconds ---" % (time.time() - start_time))
            return False
