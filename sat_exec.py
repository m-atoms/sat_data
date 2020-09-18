################################################################
#                                                              #
#  Michael Adams - Satellite Analysis Exec                     #
#                                                              #
################################################################

# directory info
sat_telem_dir = Path('sat_telem/')
sat_orbit_dir = Path('sat_orbit/')

# build dict with sat_name : DataFrame pairs
sats = {os.path.splitext(filename)[0]: pd.read_csv(sat_telem_dir/filename) for filename in os.listdir(sat_telem_dir)}

# read fleet orbit beta angles from CSVs and fix data coulmn name
beta_angles = pd.read_csv(sat_orbit_dir/'beta_sun_deg.csv')
beta_angles.rename( columns={'Unnamed: 0':'date'}, inplace=True)

sat_data()

sat_limit()

sat_anomaly()
