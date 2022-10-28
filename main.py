import osmdata as osm
import os

# TODO Pull new updates from dev branch to main branch

if __name__ == "__main__":
    # GETTING TRACE DATA
    # bounding region that is requested
    left = -71.0546
    bottom = 42.3326
    right = -71.0238
    top = 42.3608
    region = [left, bottom, right, top]
    """
    data = osm.get_gps_traces(region)
    print(data[:100])

    # Write returned data to a file
    FILENAME = "all_gps_traces_from_seaport.gpx"
    with open(FILENAME, 'w') as f:
        f.write(data)
    """
    # PARSING & PLOTTING THE DATA
    # print(os.listdir())
    traces = osm.parse_gps_traces('all_gps_traces_from_seaport.gpx', True)
    print(f"Found {len(traces)} GPS traces")
    osm.plot_traces(traces, region)

