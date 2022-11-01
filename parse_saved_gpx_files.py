import osmdata as osm
import glob
import xml.etree.ElementTree as ET

# This script is used to process gpx files whenever I have a problem
# with the OSM API

if __name__ == "__main__":
    location = "san_francisco"  # this should be the name of a folder with ".gpx" files
    source_files = glob.glob(f"source_gpx_files/{location}/*")
    all_traces = []
    for tr in source_files:
        file_traces = osm.parse_gps_traces(tr, True)
        for trace in file_traces:
            all_traces.append(trace)
    osm.save_gps_traces("gps_data_by_city", location, all_traces)
