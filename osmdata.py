"""
Copyright 2022 pgdunn@bu.edu

@author parker dunn
@created 28 Oct 2022

PURPOSE:
This file is a collection of methods for retrieving data from
OpenStreetMaps
"""

import requests
# installing new packages in PyCharm
# # https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html

"""
@author pdvnny (pgd)
@version 1

@param bounds_lst: a list containing float/int values that
define the region where we want to extract GPS traces.

@return Either None or string of gps trace data
"""

def get_gps_traces(bounds_lst: list):
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
        request_page = f"&page={page}"
        response = requests.get(endpoint+request_page)
        new_data = response.text
        if len(new_data.split('\n')) > 4:
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
            break
    return data
