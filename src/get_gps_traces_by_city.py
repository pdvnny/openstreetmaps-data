"""
This script should be used to download and save GPS traces.

It is Part 1 of the process to (1) download, (2) parse/extract locations,
and (3) save trace data as .npy files

It works best (assuming there is space to save extra files) to save each GPS
trace file that is retrieved form the OSM API. This is because you can only
retrieve one page (of many) at a time. Each page only contains 5000 lines
at most, but a region may contain well over 100,000 lines of data.

"""
import os
import requests

def get_and_save_gps_traces(bounds_lst: list, location: str):
    os.mkdir("source_gpx_files/"+location)

    bounds_lst_str = [str(b) for b in bounds_lst]
    data = ""
    if len(bounds_lst) < 4:
        Exception("Insufficient region bounds provided.\nYou must provide N, S, E, and W bounds.")
        return None

    bounds = ",".join(bounds_lst_str)
    url = "https://api.openstreetmap.org/"
    endpoint = f"{url}api/0.6/trackpoints?bbox={bounds}"

    page = 0
    while True:
        try:
            request_page = f"&page={page}"
            response = requests.get(endpoint + request_page)
            new_data = response.text
            with open(f"source_gpx_files/{location}/page{page}", 'w') as f:
                f.write(new_data)
        except ConnectionError:
            print("Lost connection")
            print(f"Reached page {page-1}")
            break

        # Kill fetching data conditions
        if len(new_data.split('\n')) > 4 and page < 150:
            print(f"Found page {page}")
            # Accumulating the data
            if page == 0:
                loc = new_data.find("</gpx>")
                data += new_data[:loc]
            else:
                loc_start = new_data.find("<trk>")
                loc_end = new_data.find("</gpx>")
                data += new_data[loc_start:loc_end]
            page += 1
        else:
            if page < 150:
                with open("gps_data_by_city/regions_downloaded.txt", 'a') as f:
                    f.write(location)
            break
    data += "</gpx>"
    return data


" Before running, create a folder for the retrieved data -> source_gpx_files"


if __name__ == "__main__":
    # First, enter the name of the city/area that you are extracting data from
    # This is just used to create a folder where information is saved
    location = "austin"

    # Second, provide N, S, E, W bounds for the region
    region = [-97.8259, 30.2348, -97.6801, 30.3080]

    raw_xml_data = get_and_save_gps_traces(region, location)
    # Each page retrieved is saved in "source_gpx_files/*location variable*/"
