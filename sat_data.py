################################################################
#                                                              #
#  Michael Adams - Satellite Fleet Data Analysis Project       #
#                                                              #
################################################################

from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess
import numpy as np

# directory info
sat_telem_dir = Path('sat_telem/')
sat_orbit_dir = Path('sat_orbit/')

# read sat telem from CSVs
alpha = pd.read_csv(sat_telem_dir/'alpha.csv')
bravo = pd.read_csv(sat_telem_dir/'bravo.csv')
charlie = pd.read_csv(sat_telem_dir/'charlie.csv')
delta = pd.read_csv(sat_telem_dir/'delta.csv')
echo = pd.read_csv(sat_telem_dir/'echo.csv')
foxtrot = pd.read_csv(sat_telem_dir/'foxtrot.csv')
golf = pd.read_csv(sat_telem_dir/'golf.csv')

# read fleet orbit beta angles from CSVs and fix data coulmn name
beta_angles = pd.read_csv(sat_orbit_dir/'beta_sun_deg.csv')
beta_angles.rename( columns={'Unnamed: 0':'date'}, inplace=True)

##################################
# Exploratory Analysis
##################################
fig, ax0 = plt.subplots()
ax1 = ax0.twinx()
ax0.set_title("Alpha gyro & reaction wheel overlay")
color0 = 'tab:blue'
color1 = 'tab:orange'
ax0.set_xlabel("time (ms since epoch)")
ax0.set_ylabel("gyro (deg/sec)", color=color0)
ax0.tick_params(axis='y', labelcolor=color0)
ax1.set_ylabel("wheel (rpm)", color=color1)
ax1.tick_params(axis='y', labelcolor=color1)
#ax0.plot(alpha.timestamp, alpha.gyro_x, ',')
ax0.plot(alpha.timestamp, alpha.gyro_x)
ax1.plot(alpha.timestamp, alpha.wheel_x, color='orange')
plt.show()
quit()

fig, axs = plt.subplots(2)
axs[0].set_title("alpha")
axs[0].plot(alpha.timestamp, alpha.gyro_z)
axs[1].set_title("bravo")
axs[1].plot(bravo.timestamp, bravo.gyro_z)
plt.show()

fig, axs = plt.subplots(2)
axs[0].set_title("alpha")
axs[0].plot(alpha.timestamp, alpha.wheel_x)
axs[1].set_title("bravo")
axs[1].plot(bravo.timestamp, bravo.wheel_x)
plt.show()
quit()

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
#testx = alpha.timestamp.to_numpy()#[0::10]
#testz = alpha.gyro_z.to_numpy(dtype=float)#[0::10]
#testx = charlie.timestamp.to_numpy()
#testz = charlie.wheel_x.to_numpy()
#filt = lowess(testz, testx, frac=0.01, missing='drop')
#filt = lowess(testz, testx, missing='drop')
#fix, ax = plt.subplots()
#ax.plot(testx, testz, ',')
#ax.plot(filt[:,0], filt[:,1], 'r-', linewidth=3)
#plt.show()

##################################
# Noise Filtering 
##################################
# spectral analysis of nonuniformly sampled signal
# find difference between time values
# plot histogram of time deltas
# note: manual check shows ~100ms so ~10Hz sample rate
# perform spectral analysis with Lomb-Scargle method

##################################
# Fleet Beta Angles - RIP Delta
##################################
#fig, ax = plt.subplots()
#ax.plot(beta_angles.date, beta_angles.alpha, label='alpha')
#ax.plot(beta_angles.date, beta_angles.bravo, label='bravo')
#ax.plot(beta_angles.date, beta_angles.charlie, label='charlie')
#ax.plot(beta_angles.date, beta_angles.delta, label='delta')
#ax.plot(beta_angles.date, beta_angles.echo, label='echo')
#ax.plot(beta_angles.date, beta_angles.foxtrot, label='foxtrot')
#ax.plot(beta_angles.date, beta_angles.golf, label='golf')
#ax.legend()
#plt.show()

##################################
# Fleet Gyro + Voltage Data
##################################
fig, axs = plt.subplots(4, 7, sharex=True)
fig.suptitle("satellite gyro speeds")
axs[0,0].set_title("alpha")
axs[0,0].set_ylabel("gyro_x")
axs[1,0].set_ylabel("gyro_y")
axs[2,0].set_ylabel("gyro_z")
axs[1,0].sharey(axs[0,0])
axs[2,0].sharey(axs[0,0])
axs[0,0].plot(alpha.timestamp, alpha.gyro_x)
axs[1,0].plot(alpha.timestamp, alpha.gyro_y)
axs[2,0].plot(alpha.timestamp, alpha.gyro_z)
axs[3,0].plot(alpha.timestamp, alpha.bus_voltage)
axs[3,0].plot(alpha.timestamp, alpha.low_voltage)

axs[0,1].set_title("bravo")
axs[0,1].sharey(axs[0,0])
axs[1,1].sharey(axs[0,0])
axs[2,1].sharey(axs[0,0])
axs[0,1].plot(bravo.timestamp, bravo.gyro_x)
axs[1,1].plot(bravo.timestamp, bravo.gyro_y)
axs[2,1].plot(bravo.timestamp, bravo.gyro_z)
axs[3,1].plot(bravo.timestamp, bravo.bus_voltage)
axs[3,1].plot(bravo.timestamp, bravo.low_voltage)

axs[0,2].set_title("charlie")
axs[0,2].sharey(axs[0,0])
axs[1,2].sharey(axs[0,0])
axs[2,2].sharey(axs[0,0])
axs[0,2].plot(charlie.timestamp, charlie.gyro_x)
axs[1,2].plot(charlie.timestamp, charlie.gyro_y)
axs[2,2].plot(charlie.timestamp, charlie.gyro_z)
axs[3,2].plot(charlie.timestamp, charlie.bus_voltage)
axs[3,2].plot(charlie.timestamp, charlie.low_voltage)

axs[0,3].set_title("delta")
axs[0,3].sharey(axs[0,0])
axs[1,3].sharey(axs[0,0])
axs[2,3].sharey(axs[0,0])
axs[0,3].plot(delta.timestamp, delta.gyro_x)
axs[1,3].plot(delta.timestamp, delta.gyro_y)
axs[2,3].plot(delta.timestamp, delta.gyro_z)
axs[3,3].plot(delta.timestamp, delta.bus_voltage)
axs[3,3].plot(delta.timestamp, delta.low_voltage)

axs[0,4].set_title("echo")
axs[0,4].sharey(axs[0,0])
axs[1,4].sharey(axs[0,0])
axs[2,4].sharey(axs[0,0])
axs[0,4].plot(echo.timestamp, echo.gyro_x)
axs[1,4].plot(echo.timestamp, echo.gyro_y)
axs[2,4].plot(echo.timestamp, echo.gyro_z)
axs[3,4].plot(echo.timestamp, echo.bus_voltage)
axs[3,4].plot(echo.timestamp, echo.low_voltage)

axs[0,5].set_title("foxtrot")
axs[0,5].sharey(axs[0,0])
axs[1,5].sharey(axs[0,0])
axs[2,5].sharey(axs[0,0])
axs[0,5].plot(foxtrot.timestamp, foxtrot.gyro_x)
axs[1,5].plot(foxtrot.timestamp, foxtrot.gyro_y)
axs[2,5].plot(foxtrot.timestamp, foxtrot.gyro_z)
axs[3,5].plot(foxtrot.timestamp, foxtrot.bus_voltage)
axs[3,5].plot(foxtrot.timestamp, foxtrot.low_voltage)

axs[0,6].set_title("golf")
axs[0,6].sharey(axs[0,0])
axs[1,6].sharey(axs[0,0])
axs[2,6].sharey(axs[0,0])
axs[0,6].plot(golf.timestamp, golf.gyro_x)
axs[1,6].plot(golf.timestamp, golf.gyro_y)
axs[2,6].plot(golf.timestamp, golf.gyro_z)
axs[3,6].plot(golf.timestamp, golf.bus_voltage)
axs[3,6].plot(golf.timestamp, golf.low_voltage)
plt.show()

##################################
# Fleet Reaction Wheel Data
##################################
fig, axs = plt.subplots(4, 7, sharex=True, sharey=True)
fig.suptitle("satellite reaction wheel speeds")
axs[0,0].set_title("alpha")
axs[0,0].set_ylabel("wheel_s")
axs[1,0].set_ylabel("wheel_x")
axs[2,0].set_ylabel("wheel_y")
axs[3,0].set_ylabel("wheel_z")
axs[0,0].plot(alpha.timestamp, alpha.wheel_s)
axs[1,0].plot(alpha.timestamp, alpha.wheel_x)
axs[2,0].plot(alpha.timestamp, alpha.wheel_y)
axs[3,0].plot(alpha.timestamp, alpha.wheel_z)

axs[0,1].set_title("bravo")
axs[0,1].plot(bravo.timestamp, bravo.wheel_s)
axs[1,1].plot(bravo.timestamp, bravo.wheel_x)
axs[2,1].plot(bravo.timestamp, bravo.wheel_y)
axs[3,1].plot(bravo.timestamp, bravo.wheel_z)

axs[0,2].set_title("charlie")
axs[0,2].plot(charlie.timestamp, charlie.wheel_s)
axs[1,2].plot(charlie.timestamp, charlie.wheel_x)
axs[2,2].plot(charlie.timestamp, charlie.wheel_y)
axs[3,2].plot(charlie.timestamp, charlie.wheel_z)

axs[0,3].set_title("delta")
axs[0,3].plot(delta.timestamp, delta.wheel_s)
axs[1,3].plot(delta.timestamp, delta.wheel_x)
axs[2,3].plot(delta.timestamp, delta.wheel_y)
axs[3,3].plot(delta.timestamp, delta.wheel_z)

axs[0,4].set_title("echo")
axs[0,4].plot(echo.timestamp, echo.wheel_s)
axs[1,4].plot(echo.timestamp, echo.wheel_x)
axs[2,4].plot(echo.timestamp, echo.wheel_y)
axs[3,4].plot(echo.timestamp, echo.wheel_z)

axs[0,5].set_title("foxtrot")
axs[0,5].plot(foxtrot.timestamp, foxtrot.wheel_s)
axs[1,5].plot(foxtrot.timestamp, foxtrot.wheel_x)
axs[2,5].plot(foxtrot.timestamp, foxtrot.wheel_y)
axs[3,5].plot(foxtrot.timestamp, foxtrot.wheel_z)

axs[0,6].set_title("golf")
axs[0,6].plot(golf.timestamp, golf.wheel_s)
axs[1,6].plot(golf.timestamp, golf.wheel_x)
axs[2,6].plot(golf.timestamp, golf.wheel_y)
axs[3,6].plot(golf.timestamp, golf.wheel_z)
plt.show()
