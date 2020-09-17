################################################################
#                                                              #
#  Michael Adams - Satellite Data Limit Detection              #
#                                                              #
################################################################

import os
from pathlib import Path
import pandas as pd

# limit conditions
WHEEL_SATURATION = 8000
GYRO_SPIN = 2
LOW_VOLTAGE = 1

# directory info
sat_telem_dir = Path('sat_telem/')

# build dict with sat_name : DataFrame pairs
sats = {os.path.splitext(filename)[0]: pd.read_csv(sat_telem_dir/filename) for filename in os.listdir(sat_telem_dir)}

# avg wheel saturation
def wheel_saturation(sat):
    s_size = sats[sat].wheel_s.size
    s_lim = sats[sat].wheel_s[sats[sat].wheel_s >= WHEEL_SATURATION]
    s_lim_size = s_lim.size
    #print(f" S  [size: {s_size}] [lim: {s_lim_size}] [lim%: {s_lim_size / s_size * 100}]")

    x_size = sats[sat].wheel_x.size
    x_lim = sats[sat].wheel_x[sats[sat].wheel_x >= WHEEL_SATURATION]
    x_lim_size = x_lim.size
    #print(f" X  [size: {x_size}] [lim: {x_lim_size}] [lim%: {x_lim_size / x_size * 100}]")

    y_size = sats[sat].wheel_y.size
    y_lim = sats[sat].wheel_y[sats[sat].wheel_y >= WHEEL_SATURATION]
    y_lim_size = y_lim.size
    #print(f" Y  [size: {y_size}] [lim: {y_lim_size}] [lim%: {y_lim_size / y_size * 100}]")

    z_size = sats[sat].wheel_z.size
    z_lim = sats[sat].wheel_z[sats[sat].wheel_z >= WHEEL_SATURATION]
    z_lim_size = z_lim.size
    #print(f" Z  [size: {z_size}] [lim: {z_lim_size}] [lim%: {z_lim_size / z_size * 100}]")

    total_size = s_size + x_size + y_size + z_size
    total_lim = s_lim_size + x_lim_size + y_lim_size + z_lim_size
    avg_lim = total_lim / total_size * 100
    print(f"avg wheel saturation:   {avg_lim:.4f}%")

# avg spin >2% magnitdue
def gyro_spin(sat):
    x_size = sats[sat].wheel_x.size
    x_lim = sats[sat].wheel_x[abs(sats[sat].wheel_x) >= GYRO_SPIN]
    x_lim_size = x_lim.size
    #print(f" X  [size: {x_size}] [lim: {x_lim_size}] [lim%: {x_lim_size / x_size * 100}]")

    y_size = sats[sat].wheel_y.size
    y_lim = sats[sat].wheel_y[abs(sats[sat].wheel_y) >= GYRO_SPIN]
    y_lim_size = y_lim.size
    #print(f" Y  [size: {y_size}] [lim: {y_lim_size}] [lim%: {y_lim_size / y_size * 100}]")

    z_size = sats[sat].wheel_z.size
    z_lim = sats[sat].wheel_z[abs(sats[sat].wheel_z) >= GYRO_SPIN]
    z_lim_size = z_lim.size
    #print(f" Z  [size: {z_size}] [lim: {z_lim_size}] [lim%: {z_lim_size / z_size * 100}]")

    total_size = x_size + y_size + z_size
    total_lim = x_lim_size + y_lim_size + z_lim_size
    avg_lim = total_lim / total_size * 100
    print(f"avg spin >2% magnitude: {avg_lim:.4f}%")

# avg low voltage flag
def low_voltage(sat):
    size = sats[sat].low_voltage.size
    lim = sats[sat].low_voltage[sats[sat].low_voltage == LOW_VOLTAGE]
    lim_size = lim.size
    avg_lim = lim_size / size * 100
    #print(f" LV  [size: {size}] [lim: {lim_size}] [lim%: {lim_size / size * 100}]")
    print(f"avg low voltage flag:   {avg_lim:.4f}%")
    
for sat in sats:
    print(f"\nSatellite: {sat.upper()}")
    wheel_saturation(sat)

    gyro_spin(sat)

    low_voltage(sat)
