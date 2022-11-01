"""
This script should be used to parse XML data and save NumPy matrices that
contain GPS traces.

It is Part 2 & 3 of the process to (1) download, (2) parse/extract traces,
and (3) save trace data as .npy files

"""

import xml.etree.ElementTree as ET
import numpy as np
import glob

"""
You will need:
(1) a "source_gpx_files" folder that contains a folder within it with ".gpx" files.
(2) a "gps_data_by_city" folder where the output ".npy" file can be saved

"""

def parse_gps_traces(traces) -> list:
    tree = ET.parse(traces)
    root = tree.getroot()

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
    print("Part 3: Saving data as numpy files")
    save_array = np.empty(len(traces), object)
    region_data = []
    for i in range(len(traces)):
        new_array = np.array([traces[i]['lon'], traces[i]['lat']])
        # print(new_array.shape)
        region_data.append(new_array)
        # print(f"Length of region data: {len(region_data)}")
    save_array[:] = region_data
    np.save(f"{file_root}/{region}.npy", save_array)


if __name__ == "__main__":
    # First, enter the name of the folder that contains your ".gpx" files
    # e.g., "source_gpx_files/austin" -> location = "austin"
    location = "austin"

    source_files = glob.glob(f"source_gpx_files/{location}/*")
    all_traces = []
    for tr in source_files:
        file_traces = parse_gps_traces(tr)
        for trace in file_traces:
            all_traces.append(trace)
    save_gps_traces("gps_data_by_city", location, all_traces)



