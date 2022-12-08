"""
Copyright 2022 Parker Dunn (pgdunn@bu.edu)

Created 2 Dec 2022

PURPOSE: I have OSM data now, but I need to convert that data into
a useful format for identify features of the road that are useful
for training autonomous driving agents.

GOAL: Generate image masks (e.g., 1000 x 1000 arrays) that identify
whether or region has a particular object or not.

Example: I will start by trying to identify where roads exist within
a bounded region
"""

import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os

import typing
import json

"GOAL 1: Extract features and plot the locations using matplotlib"


def extract_nodes(filename: str) -> pd.DataFrame:
    """
    This method converts the node data in an OSM file (XML-style format)
    into a numpy array.
    This method is designed for `.osm` files that have been processed to
    extract the node objects.
    :param filename: A filename/path for a `.osm` file with node objects
                     (e.g., boston_nodes.osm)
    :return:
    """
    tree = ET.parse(filename)
    root = tree.getroot()

    nodes = []
    for nd in root.findall("node"):
        node = dict()
        # print(nd)  # <Element 'node' at 0x7f2102a583650>
        # print(nd.keys())  # ['id', 'lat', 'lon', 'version', 'timestamp', 'changeset', 'uid', 'user']
        # print(nd.attrib)  # e.g., {'id': '10204470641', 'lat': '42.3652916', 'lon': '-71.1067369', 'version': '1', 'timestamp': '2022-11-20T17:55:54Z', 'changeset': '129165001', 'uid': '8482773', 'user': 'aweech'}
        nd_dict = nd.attrib
        node['id'] = int(nd_dict['id'])
        node['lat'] = float(nd_dict['lat'])
        node['lon'] = float(nd_dict['lon'])
        nodes.append(node)
        # print(node)

    return pd.DataFrame.from_records(nodes)

# REF
# ElementTree --> https://docs.python.org/3/library/xml.etree.elementtree.html
# Element --> https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element