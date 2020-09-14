################################################################
#                                                              #
#  Michael Adams - Satellite Fleet Data Analysis Project       #
#                                                              #
################################################################

import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path
from scipy.fft import fft
from statsmodels.nonparametric.smoothers_lowess import lowess

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


#fig, axs = plt.subplots(3)
#axs[0].plot(alpha.timestamp, alpha.gyro_x, ',')
#axs[1].plot(alpha.timestamp, alpha.gyro_y, ',')
#axs[2].plot(alpha.timestamp, alpha.gyro_z, ',')
#plt.show()

# filter test
#filtered_gyro_z = lowess(alpha.gyro_z, alpha.timestamp, missing='drop', return_sorted=False)
#fig, ax = plt.subplots()
#ax.plot(alpha.timestamp, alpha.gyro_z, '.')
#plt.show()

# single plot - data investigation
fig, ax = plt.subplots()
ax.plot(charlie.timestamp, charlie.wheel_x, '.')
plt.show()

# plot fleet orbit beta angles 
fig, ax = plt.subplots()
ax.plot(beta_angles.date, beta_angles.alpha, label='alpha')
ax.plot(beta_angles.date, beta_angles.bravo, label='bravo')
ax.plot(beta_angles.date, beta_angles.charlie, label='charlie')
ax.plot(beta_angles.date, beta_angles.delta, label='delta')
ax.plot(beta_angles.date, beta_angles.echo, label='echo')
ax.plot(beta_angles.date, beta_angles.foxtrot, label='foxtrot')
ax.plot(beta_angles.date, beta_angles.golf, label='golf')
ax.legend()
plt.show()

# plot fleet gyro data
fig, axs = plt.subplots(3, 7, sharex=True, sharey=True)
fig.suptitle("satellite gyro speeds")
axs[0,0].set_title("alpha")
axs[0,0].set_ylabel("gyro_x")
axs[1,0].set_ylabel("gyro_y")
axs[2,0].set_ylabel("gyro_z")
axs[0,0].plot(alpha.timestamp, alpha.gyro_x)
axs[1,0].plot(alpha.timestamp, alpha.gyro_y)
axs[2,0].plot(alpha.timestamp, alpha.gyro_z)

axs[0,1].set_title("bravo")
axs[0,1].plot(bravo.timestamp, bravo.gyro_x)
axs[1,1].plot(bravo.timestamp, bravo.gyro_y)
axs[2,1].plot(bravo.timestamp, bravo.gyro_z)

axs[0,2].set_title("charlie")
axs[0,2].plot(charlie.timestamp, charlie.gyro_x)
axs[1,2].plot(charlie.timestamp, charlie.gyro_y)
axs[2,2].plot(charlie.timestamp, charlie.gyro_z)

axs[0,3].set_title("delta")
axs[0,3].plot(delta.timestamp, delta.gyro_x)
axs[1,3].plot(delta.timestamp, delta.gyro_y)
axs[2,3].plot(delta.timestamp, delta.gyro_z)

axs[0,4].set_title("echo")
axs[0,4].plot(echo.timestamp, echo.gyro_x)
axs[1,4].plot(echo.timestamp, echo.gyro_y)
axs[2,4].plot(echo.timestamp, echo.gyro_z)

axs[0,5].set_title("foxtrot")
axs[0,5].plot(foxtrot.timestamp, foxtrot.gyro_x)
axs[1,5].plot(foxtrot.timestamp, foxtrot.gyro_y)
axs[2,5].plot(foxtrot.timestamp, foxtrot.gyro_z)

axs[0,6].set_title("golf")
axs[0,6].plot(golf.timestamp, golf.gyro_x)
axs[1,6].plot(golf.timestamp, golf.gyro_y)
axs[2,6].plot(golf.timestamp, golf.gyro_z)
plt.show()

# plot fleet reaction wheel data
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
