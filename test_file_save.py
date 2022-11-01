import osmdata as osm

if __name__ == "__main__":
    traces = osm.parse_gps_traces("gps_data_by_city/temp.gpx", True)
    osm.save_gps_traces("gps_data_by_city", "pittsburgh", traces)
