from src import gps_traces as osm
import json
import glob

if __name__ == "__main__":
    # GETTING TRACE DATA
    # bounding region that is requested

    # Provide location by assigning a JSON file to this variable
    file = "location_json_files/" + "miami.json"

    # Loading parameters for the location
    with open(file, 'r') as f:
        info = json.load(f)

    location = info['location']
    print(f"--- Pulling data from {location} ---")
    region = info['region']

    # Part 1 - Get
    raw_data = osm.get_and_save_gps_traces(region, location, 181)

    # Part 2 - parse/extract
    source_files = glob.glob(f"source_gpx_files/{location}/*")
    all_traces = []
    for tr in source_files:
        file_traces = osm.parse_gps_traces(tr, True)
        for trace in file_traces:
            all_traces.append(trace)

    # Part 3 - Save traces data in one file
    osm.save_gps_traces("gps_data_by_city", location, all_traces)