import osmdata as osm

if __name__ == "__main__":
    # bounding region that is requested
    left = -71.0546
    bottom = 42.3326
    right = -71.0238
    top = 42.3608
    region = [left, bottom, right, top]
    data = osm.get_gps_traces(region)
    print(data[:100])

    # Write returned data to a file
    FILENAME = "all_gps_traces_from_seaport.gpx"
    with open(FILENAME, 'w') as f:
        f.write(data)