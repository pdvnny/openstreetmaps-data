from src import gps_traces as osm
import json
import glob

if __name__ == "__main__":
    # GETTING TRACE DATA
    # bounding region that is requested

    """
    # HERE IS WHERE YOU ENTER THE BOUNDS FOR ANY REGION WHERE YOU WANT TO COLLECT DATA
    left = -80.0396
    bottom = 40.3758
    right = -79.9708
    top = 40.4988
    region = [left, bottom, right, top]

    # THIS IS NEEDED TO NAME THE FILE
    # Enter a descriptive region name for the file
    location = "pittsburgh"
    """
    files_list = glob.glob("location_json_files/*")
    for file in files_list:
        print(file)
        with open(file, 'r') as f:
            info = json.load(f)
        location = info['location']
        region = info['region']
        osm.pull_gps_traces("../gps_data_by_city", location, region)