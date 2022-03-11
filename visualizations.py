
# Source: https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london
london_map = gpd.read_file("statistical-gis-boundaries-london/ESRI/LSOA_2011_London_gen_MHW.shp")
london_map = london_map.to_crs("EPSG:4326")


'''
Visualization showing each station as a black dot with a 0.5km radius around it in red
'''
# zip x and y coordinates into single feature
geometry = [Point(xy) for xy in zip(stations['lon'], stations['lat'])]
# create GeoPandas dataframe
geo_df = gpd.GeoDataFrame(stations,
    crs = "EPSG:4326", # lat /lon
    geometry = geometry)

fig, ax = plt.subplots(figsize=(15,15)) # create figure and axes, assign to subplot
london_map.plot(ax=ax, alpha=0.4,color="grey") # add .shp mapfile to axes
geo_df.plot(column="Network", ax=ax,alpha=0.2, legend=True, markersize=150, color="red")
geo_df.plot(column="Network", ax=ax,alpha=1, legend=True, markersize=.75, color="black")

plt.title("EV chargers in London", fontsize=15,fontweight="bold")
plt.show()


'''
Visualization of each charger by type
'''
stations_and_type = pd.merge(good_sockets, stations, on="Station_ID", how="left")
slow = ['TYPE_1', 'TYPE_2', 'THREE_PIN_SQUARE']
fast = ['DC_COMBO_TYPE_2', 'CCS', 'CHADEMO', 'TYPE_2_FAST']

# Creates a T/F column for if it is fast or not


fast_chagers_only = stations_and_type[stations_and_type['Type'].isin(fast)]
slow_chargers_only = stations_and_type[stations_and_type['Type'].isin(slow)]

# zip x and y coordinates into single feature
geometry = [Point(xy) for xy in zip(slow_chargers_only['lon'], slow_chargers_only['lat'])]
# create GeoPandas dataframe
slow_geo_df = gpd.GeoDataFrame(slow_chargers_only,
    crs = "EPSG:4326", # lat /lon
    geometry = geometry)


# zip x and y coordinates into single feature
geometry = [Point(xy) for xy in zip(fast_chagers_only['lon'], fast_chagers_only['lat'])]
# create GeoPandas dataframe
fast_geo_df = gpd.GeoDataFrame(fast_chagers_only,
    crs = "EPSG:4326", # lat /lon
    geometry = geometry)


fig, ax = plt.subplots(figsize=(15,15)) # create figure and axes, assign to subplot
london_map.plot(ax=ax, alpha=0.4,color="grey") # add .shp mapfile to axes
slow_geo_df.plot(column="Socket_ID", ax=ax, alpha=.3, legend=True, markersize=20, color="yellow")
fast_geo_df.plot(column="Socket_ID", ax=ax, alpha=1, legend=True, markersize=3, color="purple")

legend()
plt.title("EV chargers in London", fontsize=15,fontweight="bold")
plt.show()



'''
Visualization utilization
'''
# zip x and y coordinates into single feature
geometry = [Point(xy) for xy in zip(avg_hours_per_station['lon'], avg_hours_per_station['lat'])]
# create GeoPandas dataframe
geo_df = gpd.GeoDataFrame(avg_hours_per_station,
    crs = "EPSG:4326", # lat /lon
    geometry = geometry)

fig, ax = plt.subplots(figsize=(15,15)) # create figure and axes, assign to subplot
london_map.plot(ax=ax, alpha=0.4,color="grey") # add .shp mapfile to axes
geo_df.plot(column="Duration_hours", ax=ax,alpha=0.1, legend=True, markersize=1.5*geo_df['Duration_hours'], color="red")
geo_df.plot(column="Duration_hours", ax=ax,alpha=1, legend=True, markersize=1, color="black")

plt.title("EV chargers in London", fontsize=15,fontweight="bold")
plt.show()



