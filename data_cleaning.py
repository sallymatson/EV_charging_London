import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import re


'''
STATIONS DATASET
'''
stations = pd.read_csv('StationsData/Stations.csv', names=['Station_ID', 'lat', 'lon', 'Network', 'Postcode'])

# For the network, take the first three letters:
stations['Network'] = stations['Network'].str.slice(0, 3)

# For the neighbhorhood, use the first half of the postcode:
stations['Neighborhood'] = stations['Postcode'].str.split(" ", expand=True)[0]

def add_zone(x):
    return re.findall('([a-zA-Z]+)', x)[0]

stations['Zone'] = stations['Neighborhood'].apply(lambda x: add_zone(x))

# Keep only the useful columns
stations = stations[['Station_ID', 'lat', 'lon', 'Network', 'Neighborhood']]

# Find stations outside of London proper, and get rid of them from the dataset
geographical_outliers = stations.loc[(stations['lat'] < 51.3) | (stations['lat'] > 51.7) | (stations['lon'] < -0.5)]
stations = pd.concat([geographical_outliers, stations]).drop_duplicates(keep=False)


'''
SOCKETS DATASET
'''
sockets = pd.read_csv('StationsData/Sockets.csv', names=['Socket_ID', 'Type', 'Power', 'Station_ID'])

# Sockets that ID is not in station data (these have stations which are outliers)
unknown_sockets = sockets[~sockets['Station_ID'].isin(stations['Station_ID'])]

# Keep only the useful sockets
good_sockets = pd.concat([sockets, unknown_sockets]).drop_duplicates(keep=False)


'''
SOCKET STATUS
'''
status = pd.read_csv('StationsData/SocketStatus.csv', parse_dates=[[1, 2]], dayfirst=True)

# Remove entries where status is not in the list of good sockets:
status_unknown_socket = status[~status['Socket_ID'].isin(good_sockets['Socket_ID'])]
# Get them out of the dataset
status = pd.concat([status, status_unknown_socket]).drop_duplicates(keep=False)

# The sockets with less than 5 records:
status_with_good_socket = (status.groupby('Socket_ID').count()['Status']>=5)
good_status = status[status['Socket_ID'].isin(status_with_good_socket[status_with_good_socket].index)]
good_status = good_status[good_status['Status'].isin([0, 1])]

charging_sessions = pd.DataFrame(columns=['Socket_ID', 'In', 'Out'])

for socket in good_sockets['Socket_ID']: # Go through the sockets one by one
    # All of the statuses for a given socket (should be chronological order)
    list_of_status = good_status.loc[(status['Socket_ID'] == socket)].reset_index()
    i = 0
    while i < len(list_of_status): # Loop through the statuses
        current_entry = list_of_status.iloc[i, :]
        if current_entry['Status'] == 0:
            # Charging session starts
            TIME_IN = current_entry['Date_Time']
            # Find the end:
            i = i+1
            if i == len(list_of_status):
                break
            current_entry = list_of_status.iloc[i, :]
            if current_entry['Status'] == 1:
                # Charging session ends
                TIME_OUT = current_entry['Date_Time']
                charging_sessions.loc[len(charging_sessions)] = {'Socket_ID': socket, 'In': TIME_IN, 'Out': TIME_OUT}
        i = i+1

charging_sessions['Duration'] = charging_sessions['Out'] - invalid_sessions['In']
charging_sessions['Duration_hours'] = charging_sessions['Duration'].dt.total_seconds()/3600


hours_per_socket = charging_sessions.groupby('Socket_ID').sum()
hours_per_socket = pd.merge(hours_per_socket, good_sockets, on='Socket_ID', how='left')
avg_hours_per_station = hours_per_socket.groupby('Station_ID').mean()['Duration_hours']
avg_hours_per_station = pd.merge(avg_hours_per_station, stations, on='Station_ID', how='left')

