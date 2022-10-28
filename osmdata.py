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
from matplotlib import pyplot as plt
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


"""
@:author pdvnny (pgd)
@:version 1
@:param traces - a string containing all of the GPS trace data in XML format.

@:return a list of dictionaries, where each dictionary contains information
about one trace in the source data
"""

def parse_gps_traces(traces, file: bool = False) -> list:
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
        trace_name = trace.find('gpxns:name')
        trace_url = trace.find('gpxns:url')
        trkseg_num = 0
        for trkseg in trace.findall('gpxns:trkseg'):
            trace_dict = dict()

            trace_dict["name"] = trace_name.text
            trace_dict["url"] = trace_url.text
            trace_dict['seg_num'] = trkseg_num

            lats = []
            longs = []
            for trkpt in trkseg.findall('gpxns:trkpt'):
                lats.append(trkpt.attrib['lat'])
                longs.append(trkpt.attrib['lon'])

            trace_dict['lon'] = longs
            trace_dict['lat'] = lats
            traces.append(trace_dict)

            trkseg_num += 1
        print(traces[0])
        break
    return traces

