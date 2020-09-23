################################################################
#                                                              #
#  Michael Adams - sat_data Directory Organization             #
#                                                              #
################################################################
import os
from pathlib import Path

sat_telem_dir = Path('sat_telem/')
sat_orbit_dir = Path('sat_orbit/')
data_viz_dir = Path('sat_data_viz/')
sat_data_viz_dir = os.path.join(data_viz_dir, 'sat')
fleet_data_viz_dir = os.path.join(data_viz_dir, 'fleet')
beta_angles_data_viz_dir = os.path.join(data_viz_dir, 'beta_angles')
