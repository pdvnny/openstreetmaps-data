"""
Copyright 2022 pgdunn@bu.edu

@author parker dunn
@created 28 Oct 2022

PURPOSE:
This file is a collection of methods for retrieving data from
OpenStreetMaps
"""

import requests
import xml.etree.ElementTree as ET
import numpy as np
from matplotlib import pyplot as plt
import os

import typing
import json

# installing new packages in PyCharm
# # https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html


<<<<<<< Updated upstream:osmdata.py
# ---------------------- FILTERING AND PROCESSING `.OSM` DATA -------------------------

def region_filter(loc_file: str, data_file: str) -> None:
    """
    @author pdvnny (pgdunn@bu.edu)

    :param loc_file: The name of the `json` file with bounds that define the region. The path of this loc_file
                     is assumed to be "location_json_files/*loc_file*"
    :param data_file: The name of the data file that is being filtered.
    :return: A list containing the OSM data in specified region
    """
    file = "location_json_files/"+loc_file
    with open(file, 'r') as f:
        info = json.load(f)

    location = info['location']
    bounds = info['region']
    print(bounds)

    return None


# -------------------------- WORKING WITH GPS TRACES --------------------------------
=======
def get_gps_traces(bounds_lst: list, location: str):
    """
    @author pdvnny (pgd)
    @version 1

    @param bounds_lst: a list containing float/int values that
    define the region where we want to extract GPS traces.
>>>>>>> Stashed changes:src/gps_traces.py

    @param location: a name for the file that is created by this
    method

<<<<<<< Updated upstream:osmdata.py
def get_gps_traces(bounds_lst: list, location: str):
    """
    @author pdvnny (pgd)
    @version 1

    @param bounds_lst: a list containing float/int values that
    define the region where we want to extract GPS traces.

=======
>>>>>>> Stashed changes:src/gps_traces.py
    @return Either None or string of gps trace data
    """
    print("--- Part 1: Getting GPS traces ---")
    bounds_lst_str = [str(b) for b in bounds_lst]
    data = ""
    if len(bounds_lst) < 4:
        Exception("Insufficient region bounds provided.\nYou must provide N, S, E, and W bounds.")
        return None

    bounds = ",".join(bounds_lst_str)
    url = "https://api.openstreetmap.org/"
    endpoint = f"{url}api/0.6/trackpoints?bbox={bounds}"

    print("Starting while loop")
    page = 0
    while True:
        request_page = f"&page={page}"
        response = requests.get(endpoint + request_page)
        new_data = response.text
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
                with open("../gps_data_by_city/regions_downloaded.txt", 'a') as f:
                    f.write(location)
            break
    data += "</gpx>"
    # with open("gps_data_by_city/temp.gpx", 'w') as f:
    #     f.write(data)
    return data


def get_and_save_gps_traces(bounds_lst: list, location: str, start: int = 0):
    # print("Part 1: Getting GPS traces ---")
    if (not os.path.exists("source_gpx_files/"+location)):
        os.mkdir("source_gpx_files/"+location)

    bounds_lst_str = [str(b) for b in bounds_lst]
    data = ""
    if len(bounds_lst) < 4:
        Exception("Insufficient region bounds provided.\nYou must provide N, S, E, and W bounds.")
        return None

    bounds = ",".join(bounds_lst_str)
    url = "https://api.openstreetmap.org/"
    endpoint = f"{url}api/0.6/trackpoints?bbox={bounds}"

    # print("Starting while loop")
    page = start
    while True:
        try:
            request_page = f"&page={page}"
            response = requests.get(endpoint + request_page)
            new_data = response.text
            with open(f"source_gpx_files/{location}/page{page}.gpx", 'w') as f:
                f.write(new_data)
        except:
            print("Lost connection")
            print(f"Reached page {page-1}")
            break

        # Kill fetching data conditions
        if len(new_data.split('\n')) > 4:  # and page < (start + 150):
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
                with open("../gps_data_by_city/regions_downloaded.txt", 'a') as f:
                    f.write(location)
            break
    data += "</gpx>"
    return data


def parse_gps_traces(traces, file: bool = False) -> list:
    """
    @:author pdvnny (pgd)
    @:version 1
    @:param traces - a string containing all GPS trace data in XML format.

    @:return a list of dictionaries, where each dictionary contains information
    about one trace in the source data
    """
    # print("Part 2: Parsing information from GPS traces")
    if file:
        tree = ET.parse(traces)
        root = tree.getroot()
    else:
        root = ET.fromstring(traces)
        # root = tree.getroot() -- don't have to do this with when working from string

    # Namespace for gps trace data
    namespace = {'gpxns': 'http://www.topografix.com/GPX/1/0'}

    traces = []
    for trace in root.findall('gpxns:trk', namespace):
        trace_name = trace.find('gpxns:name', namespace)
        name = trace_name.text if trace_name is not None else "Untitled"
        trace_url = trace.find('gpxns:url', namespace)
        url = trace_url.text if trace_url is not None else "No URL provided"

        trkseg_num = 0
        for trkseg in trace.findall('gpxns:trkseg', namespace):
            trace_dict = dict()
            trace_dict["name"] = name
            trace_dict["url"] = url
            trace_dict['seg_num'] = trkseg_num

            lats = []
            longs = []
            for trkpt in trkseg.findall('gpxns:trkpt', namespace):
                lats.append(trkpt.attrib['lat'])
                longs.append(trkpt.attrib['lon'])

            trace_dict['lon'] = [float(lon) for lon in longs]
            trace_dict['lat'] = [float(lat) for lat in lats]
            traces.append(trace_dict)

            trkseg_num += 1
    return traces


def save_gps_traces(file_root: str, region: str, traces: list) -> None:
    """
    :param file_root: This is a string representing where the data should be stored
    :param region: This will be used for the filename
    :param traces: This is a list of dictionaries containing information about GPS traces
    :return:
    """
    # print("Part 3: Saving data as numpy files")
    save_array = np.empty(len(traces), object)
    region_data = []
    for i in range(len(traces)):
        new_array = np.array([traces[i]['lon'], traces[i]['lat']])
        # print(new_array.shape)
        region_data.append(new_array)
        # print(f"Length of region data: {len(region_data)}")
        """
        if i == 0:
            region_data = np.array([traces[i]['lon'], traces[i]['lat']])
            print(region_data.shape)
            print(region_data)
        else:
            print(traces[i]['lon'])
            print(traces[i]['lat'])
            new_array = np.array([traces[i]['lon'], traces[i]['lat']])
            region_data = np.concatenate((region_data, new_array))
            print(region_data.shape)
        """
    save_array[:] = region_data
    np.save(f"{file_root}/{region}.npy", save_array)


def pull_gps_traces(file_root: str, location: str, region: list):
    """
    :param file_root:
    :param location:
    :param region:
    :return None - saves GPS trace data to files
    """
    # CALLING THREE FUNCTIONS TO GET, PARSE, AND SAVE
    raw_data = get_gps_traces(region, location)
    traces = parse_gps_traces(raw_data)
    save_gps_traces(file_root, location, traces)


def plot_traces(trace_dicts: list, region: list) -> None:
    """
    @:author pdvnny (pgd)
    @:version 1

    @:param "trace_dicts" - dictionaries containing information
    about every GPS trace from a region
    @:param "region" - a list of the boundary for the region being plotted

    This method plots all GPS traces from a region on a single plot
    """
    print("`plot_traces` has not been completed yet.")
