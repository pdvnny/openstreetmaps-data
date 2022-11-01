import osmdata as osm
import json

if __name__ == "__main__":
    # GETTING TRACE DATA
    # bounding region that is requested

    # Provide location by assigning a JSON file to this variable
    file = "location_json_files/" + "singapore.json"

    # Loading parameters for the location
    with open(file, 'r') as f:
        info = json.load(f)

    location = info['location']
    print(f"--- Pulling data from {location} ---")
    region = info['region']

    raw_data = osm.get_and_save_gps_traces(region, location)
    traces = osm.parse_gps_traces(raw_data)
    osm.save_gps_traces("gps_data_by_city", location, traces)
