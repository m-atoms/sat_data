################################################################
#                                                              #
#  Michael Adams - Satellite Fleet Data Analysis Project       #
#                                                              #
################################################################

import os
from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess
import numpy as np

# directory info
sat_telem_dir = Path('sat_telem/')
sat_orbit_dir = Path('sat_orbit/')

# build dict with sat_name : DataFrame pairs
sats = {os.path.splitext(filename)[0]: pd.read_csv(sat_telem_dir/filename) for filename in os.listdir(sat_telem_dir)}

# read fleet orbit beta angles from CSVs and fix data coulmn name
beta_angles = pd.read_csv(sat_orbit_dir/'beta_sun_deg.csv')
beta_angles.rename( columns={'Unnamed: 0':'date'}, inplace=True)

##################################
# Plot Single Channel
##################################
def plot_channel(sat, channel):
    fig, ax = plt.subplots()
    fig.suptitle(f"{sat}")
    ax.set_ylabel(f"{channel}")
    ax.set_xlabel("time (hours)")
    timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))
    ax.plot(timestamp_hrs, sats[sat].loc[:,channel])

##################################
# Single Sat Full Data Split
##################################
def plot_sat(sat):
    fig, axs = plt.subplots(3, sharex=True)
    fig.suptitle(f"{sat}")
    axs[0].set_ylabel("gyro (deg/sec)")
    axs[1].set_ylabel("wheel (rpm)")
    axs[2].set_ylabel("bus voltage and low voltage flag")
    axs[2].set_xlabel("time (hours)")
    timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))
    axs[0].plot(timestamp_hrs, sats[sat].gyro_x, label='gyro_x')#, ',')
    axs[0].plot(timestamp_hrs, sats[sat].gyro_y, label='gyro_y')#, ',')
    axs[0].plot(timestamp_hrs, sats[sat].gyro_z, label='gyro_z')#, ',')
    axs[1].plot(timestamp_hrs, sats[sat].wheel_s, label='wheel_s')#, ',')
    axs[1].plot(timestamp_hrs, sats[sat].wheel_x, label='wheel_x')#, ',')
    axs[1].plot(timestamp_hrs, sats[sat].wheel_y, label='wheel_y')#, ',')
    axs[1].plot(timestamp_hrs, sats[sat].wheel_z, label='wheel_z')#, ',')
    axs[2].plot(timestamp_hrs, sats[sat].bus_voltage, '.')
    axs[2].plot(timestamp_hrs, sats[sat].low_voltage, '.')
    axs[0].legend()
    axs[1].legend()

##################################
# Fleet Beta Angles - RIP Delta
##################################
def plot_beta_angles():
    fig, ax = plt.subplots()
    [ax.plot(beta_angles.date, beta_angles.loc[:,sat], label=sat) for sat in sats]
    ax.legend()

##################################
# Compare Two Sats
##################################
#fig, axs = plt.subplots(2)
#axs[0].set_title("alpha")
#axs[0].plot(alpha.timestamp, alpha.gyro_z)
#axs[1].set_title("bravo")
#axs[1].plot(bravo.timestamp, bravo.gyro_z)
#plt.show()
#
#fig, axs = plt.subplots(2)
#axs[0].set_title("alpha")
#axs[0].plot(alpha.timestamp, alpha.wheel_x)
#axs[1].set_title("bravo")
#axs[1].plot(bravo.timestamp, bravo.wheel_x)
#plt.show()
#quit()

##################################
# LOWESS Exploration
##################################
# LOWESS Demo
#x = np.random.uniform(low = -2*np.pi, high = 2*np.pi, size=100)
#y = np.sin(x) + np.random.normal(size=len(x))
#z = lowess(y, x, frac=0.01)
#fig, ax = plt.subplots()
#ax.plot(x,y,'.')
#ax.plot(z[:,0], z[:,1], 'r-', linewidth=3)
#plt.show()

# LOWESS Analysis
#testx = sats['alpha'].timestamp.to_numpy()#[0::10]
#testz = sats['alpha'].gyro_z.to_numpy(dtype=float)#[0::10]
#testx = sats['charlie'].timestamp.to_numpy()
#testz = sats['charlie'].wheel_x.to_numpy()
#filt = lowess(testz, testx, frac=0.1, missing='drop')
##filt = lowess(testz, testx, missing='drop')
#fix, ax = plt.subplots()
#ax.plot(testx, testz, '.')
#ax.plot(filt[:,0], filt[:,1], 'r-', linewidth=3)
#plt.show()
#quit()

##################################
# Noise Filtering 
##################################
# spectral analysis of nonuniformly sampled signal
# find difference between time values
# plot histogram of time deltas
# note: manual check shows ~100ms so ~10Hz sample rate
# perform spectral analysis with Lomb-Scargle method

##################################
# Fleet Gyro Data
##################################
def plot_gyros():
    fig, axs = plt.subplots(3, 7, sharex=True, sharey=True)
    fig.suptitle("satellite gyro speeds")
    axs[0,0].set_ylabel("gyro_x")
    axs[1,0].set_ylabel("gyro_y")
    axs[2,0].set_ylabel("gyro_z")

    for idx, sat in enumerate(sats):
        axs[0,idx].set_title(sat)
        axs[0,idx].sharey(axs[0,0])
        axs[1,idx].sharey(axs[0,0])
        axs[2,idx].sharey(axs[0,0])
        axs[2,idx].set_xlabel("time (hours)")
        timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))
        axs[0,idx].plot(timestamp_hrs, sats[sat].gyro_x)
        axs[1,idx].plot(timestamp_hrs, sats[sat].gyro_y)
        axs[2,idx].plot(timestamp_hrs, sats[sat].gyro_z)

##################################
# Fleet Reaction Wheel Data
##################################
def plot_wheels():
    fig, axs = plt.subplots(4, 7, sharex=True, sharey=True)
    fig.suptitle("satellite reaction wheel speeds")
    axs[0,0].set_ylabel("wheel_s")
    axs[1,0].set_ylabel("wheel_x")
    axs[2,0].set_ylabel("wheel_y")
    axs[3,0].set_ylabel("wheel_z")
    
    for idx, sat in enumerate(sats):
        axs[0,idx].set_title(sat)
        axs[3,idx].set_xlabel("time (hours)")
        timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))
        axs[0,idx].plot(timestamp_hrs, sats[sat].wheel_s)
        axs[1,idx].plot(timestamp_hrs, sats[sat].wheel_x)
        axs[2,idx].plot(timestamp_hrs, sats[sat].wheel_y)
        axs[3,idx].plot(timestamp_hrs, sats[sat].wheel_z)

plot_channel('alpha','gyro_z')
plot_channel('alpha','wheel_z')
#plot_sat_split('alpha')
plot_sat('alpha')
#plot_beta_angles()
plot_gyros()
plot_wheels()
#[test_plot(sat) for sat in sats]
plt.show()
quit()
