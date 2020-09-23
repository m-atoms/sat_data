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
import datetime as dt

# directory info
sat_telem_dir = Path('sat_telem/')
sat_orbit_dir = Path('sat_orbit/')
data_viz_dir = Path('sat_data_viz/')
sat_data_viz_dir = os.path.join(data_viz_dir, 'sat')
fleet_data_viz_dir = os.path.join(data_viz_dir, 'fleet')
beta_angles_data_viz_dir = os.path.join(data_viz_dir, 'beta_angles')

# build dict with sat_name : DataFrame pairs
sats = {os.path.splitext(filename)[0]: pd.read_csv(sat_telem_dir/filename) for filename in os.listdir(sat_telem_dir)}

# read fleet orbit beta angles from CSVs and fix data coulmn name
beta_angles = pd.read_csv(sat_orbit_dir/'beta_sun_deg.csv')
beta_angles.rename( columns={'Unnamed: 0':'date'}, inplace=True)

##################################
# Single Sat Full Data
##################################
def plot_sat(sat):
    fig, axs = plt.subplots(3, sharex=True)
    axs[0].set_title(f"{sat.upper()} Telemetry")
    axs[0].set_ylabel("gyro (deg/sec)")
    axs[1].set_ylabel("wheel (rpm)")
    axs[2].set_ylabel("bus voltage and low voltage flag")
    axs[2].set_xlabel("time (hours)")

    timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))
    axs[0].plot(timestamp_hrs, sats[sat].gyro_x, label='gyro_x')
    axs[0].plot(timestamp_hrs, sats[sat].gyro_y, label='gyro_y')
    axs[0].plot(timestamp_hrs, sats[sat].gyro_z, label='gyro_z')
    axs[1].plot(timestamp_hrs, sats[sat].wheel_s, label='wheel_s')
    axs[1].plot(timestamp_hrs, sats[sat].wheel_x, label='wheel_x')
    axs[1].plot(timestamp_hrs, sats[sat].wheel_y, label='wheel_y')
    axs[1].plot(timestamp_hrs, sats[sat].wheel_z, label='wheel_z')

    r ='tab:red'
    b ='tab:blue'
    axs2_y1 = axs[2]
    axs2_y1.plot(timestamp_hrs, sats[sat].bus_voltage, '.', color=r)
    axs2_y1.set_ylim(0, 10)
    axs2_y1.set_ylabel('bus voltage', color=r)
    axs2_y1.tick_params(axis='y', labelcolor=r)

    axs2_y2 = axs[2].twinx()
    axs2_y2.plot(timestamp_hrs, sats[sat].low_voltage, '.', color=b)
    axs2_y2.set_ylim(0, 2)
    axs2_y2.set_ylabel('low voltage flag', color=b)
    axs2_y2.tick_params(axis='y', labelcolor=b)

    axs[0].legend()
    axs[1].legend()

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.savefig(os.path.join(sat_data_viz_dir, f"{sat}.png"))

##################################
# Full Fleet Full Data
##################################
def plot_fleet():
    fig, axs = plt.subplots(3, 7, sharex=True, sharey='row')

    # set title and axis labels
    fig.suptitle("Fleet Telemetry")
    axs[0,0].set_ylabel("gyro (deg/sec)")
    axs[1,0].set_ylabel("wheel (rpm)")
    axs[2,0].set_ylabel("bus voltage and low voltage flag")

    for idx, sat in enumerate(sats):
        # set column titles
        axs[0, idx].set_title(f"{sat.upper()}")

        # convert ms since epoch to hours of data series for legibiltiy
        timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))

        # plot gyros, wheels, voltage info
        axs[0,idx].plot(timestamp_hrs, sats[sat].gyro_x, label='gyro_x')
        axs[0,idx].plot(timestamp_hrs, sats[sat].gyro_y, label='gyro_y')
        axs[0,idx].plot(timestamp_hrs, sats[sat].gyro_z, label='gyro_z')

        axs[1,idx].plot(timestamp_hrs, sats[sat].wheel_s, label='wheel_s')
        axs[1,idx].plot(timestamp_hrs, sats[sat].wheel_x, label='wheel_x')
        axs[1,idx].plot(timestamp_hrs, sats[sat].wheel_y, label='wheel_y')
        axs[1,idx].plot(timestamp_hrs, sats[sat].wheel_z, label='wheel_z')

        axs[2,idx].set_xlabel("time (hours)")
        axs[2,idx].plot(timestamp_hrs, sats[sat].bus_voltage, '.', label='bus_voltage')
        axs[2,idx].plot(timestamp_hrs, sats[sat].low_voltage, '.', label='low_voltage')

    # maximize figure and save to output dir
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.savefig(os.path.join(fleet_data_viz_dir, 'fleet_telem.png'))

##################################
# Fleet Gyro Data
##################################
def plot_fleet_gyros():
    fig, axs = plt.subplots(3, 7, sharex=True, sharey=True)

    # set title and axis labels
    fig.suptitle("Fleet Gyro Telemetry")
    fig.text(0.04, 0.5, 'gyroscope spin rate (deg/sec)', va='center', rotation='vertical')
    fig.text(0.5, 0.04, 'time (hours)', ha='center')

    axs[0,0].set_ylabel("gyro_x")
    axs[1,0].set_ylabel("gyro_y")
    axs[2,0].set_ylabel("gyro_z")

    for idx, sat in enumerate(sats):
        # set column titles
        axs[0, idx].set_title(f"{sat.upper()}")

        # convert ms since epoch to hours of data series for legibiltiy
        timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))

        # plot gyros
        axs[0,idx].plot(timestamp_hrs, sats[sat].gyro_x)
        axs[1,idx].plot(timestamp_hrs, sats[sat].gyro_y)
        axs[2,idx].plot(timestamp_hrs, sats[sat].gyro_z)

    # maximize figure and save to output dir
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.savefig(os.path.join(fleet_data_viz_dir, 'fleet_gyro_telem.png'))

##################################
# Fleet Reaction Wheel Data
##################################
def plot_fleet_wheels():
    fig, axs = plt.subplots(4, 7, sharex=True, sharey=True)

    # set title and axis labels
    fig.suptitle("Fleet Reaction Wheel Telemetry")
    fig.text(0.04, 0.5, 'reaction wheel spin rate (rpm)', va='center', rotation='vertical')
    fig.text(0.5, 0.04, 'time (hours)', ha='center')
    axs[0,0].set_ylabel("wheel_s")
    axs[1,0].set_ylabel("wheel_x")
    axs[2,0].set_ylabel("wheel_y")
    axs[3,0].set_ylabel("wheel_z")
    
    for idx, sat in enumerate(sats):
        # set column titles
        axs[0, idx].set_title(f"{sat.upper()}")

        # convert ms since epoch to hours of data series for legibiltiy
        timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))

        # plot wheels
        axs[0,idx].plot(timestamp_hrs, sats[sat].wheel_s)
        axs[1,idx].plot(timestamp_hrs, sats[sat].wheel_x)
        axs[2,idx].plot(timestamp_hrs, sats[sat].wheel_y)
        axs[3,idx].plot(timestamp_hrs, sats[sat].wheel_z)

    # maximize figure and save to output dir
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.savefig(os.path.join(fleet_data_viz_dir, 'fleet_wheel_telem.png'))

##################################
# Fleet Voltage Data
##################################
def plot_fleet_voltages():
    fig, axs = plt.subplots(7, 1, sharex=True, sharey=True)

    # set title and axis labels
    fig.suptitle("Fleet Voltage Telemetry")
    fig.text(0.04, 0.5, 'bus voltage (blue) and low voltage flag (orange)', va='center', rotation='vertical')
    fig.text(0.5, 0.04, 'time (hours)', ha='center')
    
    for idx, sat in enumerate(sats):
        # set column titles
        axs[idx].set_title(f"{sat.upper()}")

        # convert ms since epoch to hours of data series for legibiltiy
        timestamp_hrs = sats[sat].timestamp.apply(lambda x: ((x - sats[sat].timestamp[0])/ (1000 * 3600)))

        # plot wheels
        axs[idx].plot(timestamp_hrs, sats[sat].bus_voltage, '.', label='bus_voltage')
        axs[idx].plot(timestamp_hrs, sats[sat].low_voltage, '.', label='low_voltage')

    # maximize figure and save to output dir
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.savefig(os.path.join(fleet_data_viz_dir, 'fleet_voltage_telem.png'))

##################################
# Fleet Beta Angles
##################################
def plot_beta_angles():
    fig, ax = plt.subplots()
    markers = ['s', 10, 'x', '<', 11, '.', '|']
    [ax.plot(pd.to_datetime(beta_angles.date), beta_angles.loc[:,sat], label=sat, marker=markers[idx]) for idx, sat in enumerate(sats)]
    ax.set_title("Fleet Beta Angles")
    ax.set_xlabel("date (yyyy-mm)")
    ax.set_ylabel("beta angle (deg)")
    ax.legend()

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.savefig(os.path.join(beta_angles_data_viz_dir, 'fleet_beta_angles.png'))

####################################################################
####################################################################
####### Supplemental Data Exploration Not Included in Output #######
####################################################################
####################################################################

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
# Moving Average 
##################################
def wheel_filter():
    # note: nans make normal sliding window ineffective
    #       interpolate and slide window
    #       too simplified - data not good fit for these approaches
    z = sats['alpha'].wheel_z
    itrp = z.interpolate('index').rolling(5).mean()
    roll = z.rolling(3).apply(np.nanmean)

    fig, ax = plt.subplots()
    ax.plot(sats['alpha'].timestamp, z)
    ax.plot(sats['alpha'].timestamp, itrp, '.')
    ax.plot(sats['alpha'].timestamp, roll)
    #ax.plot(np.convolve(z, np.ones((10,))/10, mode='valid'), '.')

def gyro_filter():
    # note: reduce noise around baseline but trim spikes
    z = sats['alpha'].gyro_z
    rolling = z.interpolate('index').rolling(10).mean()

    fig, ax = plt.subplots()
    ax.plot(range(0,sats['alpha'].gyro_z.size) , sats['alpha'].gyro_z)
    ax.plot(range(0,sats['alpha'].gyro_z.size), rolling, '.')
    ax.plot(np.convolve(z, np.ones((30,))/30, mode='valid'), '.')

##################################
# LOWESS Exploration
##################################
def plot_lowess():
    # note: at frac > 0.01 lowess cant keep up with data spikes
    #       but at low frac values introduces erroneous spikes
    #       does not seem to be a good fit, also very computationally heavy
    testx = sats['alpha'].timestamp.to_numpy()
    testz = sats['alpha'].gyro_z.to_numpy(dtype=float)
    #testx = sats['charlie'].timestamp.to_numpy()
    #testz = sats['charlie'].wheel_x.to_numpy()
    filt = lowess(testz, testx, frac=0.1, missing='drop')
    fix, ax = plt.subplots()
    ax.plot(testx, testz, '.')
    ax.plot(filt[:,0], filt[:,1], 'r-', linewidth=3)

##################################
# Noise Filtering 
##################################
# spectral analysis of nonuniformly sampled signal
# find difference between time values
# plot histogram of time deltas
# note: manual check shows ~100ms so ~10Hz sample rate
# perform spectral analysis with Lomb-Scargle method

# execute all plotting operations
#plot_beta_angles()
#[plot_sat(sat) for sat in sats]
#plot_fleet()
#plot_fleet_gyros()
#plot_fleet_wheels()
#plot_fleet_voltages()
