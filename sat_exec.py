################################################################
#                                                              #
#  Michael Adams - Satellite Analysis Exec                     #
#                                                              #
################################################################

import os
import time
from pathlib import Path
import pandas as pd
from sat_data_org import sat_telem_dir, sat_orbit_dir
from sat_data import sat_data
from sat_limit import sat_limit
from sat_anomaly import sat_anomaly

##################################
# Read Satellite Data from CSVs
##################################
# build dict with sat_name : DataFrame pairs
sats = {os.path.splitext(filename)[0]: pd.read_csv(sat_telem_dir/filename) for filename in os.listdir(sat_telem_dir)}

# read fleet orbit beta angles from CSVs and fix data coulmn name
beta_angles = pd.read_csv(sat_orbit_dir/'beta_sun_deg.csv')
beta_angles.rename( columns={'Unnamed: 0':'date'}, inplace=True)

##################################
# Create Plots
##################################
sat_data(sats, beta_angles)

##################################
# Compute Limit Conditions
##################################
start_time = time.time()
sat_limit(sats)
print("--- sat_limit: %s seconds ---" % (time.time() - start_time))

##################################
# Check for Anomalies
##################################
anomaly_detected = sat_anomaly(sats)
print(f"ANOMALY DETECTION: {anomaly_detected}")
