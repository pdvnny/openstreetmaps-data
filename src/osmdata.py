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
from collections.abc import Sequence

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os

import typing
import json

# -------------- HELPER FUNCTIONS -------------------


def get_bounds(data: np.ndarray) -> Sequence[list]:
    """
    Helper function!
    This method receives lon and lat data as a NumPy array
    and returns reasonable bounds for a plot.
    :param data:
    :return:
    """
    x_bounds = [min(data[:, 0]), max(data[:, 0])]
    x_range = x_bounds[1] - x_bounds[0]
    x_bounds = [x_bounds[0] - (0.005 * x_range),
                x_bounds[1] + (0.005 * x_range)]

    y_bounds = [min(data[:, 1]), max(data[:, 1])]
    y_range = y_bounds[1] - y_bounds[0]
    y_bounds = [y_bounds[0] - (0.005 * y_range),
                y_bounds[1] + (0.005 * y_range)]
    return x_bounds, y_bounds


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


def plot_nodes(df: pd.DataFrame, loc: str) -> None:
    """
    This function plots the locations of nodes extracted from OSM data.
    The nodes should be passed to the function as a Pandas DataFrame
    for now.
    :param df: A DataFrame with 'lat' and 'lon' columns. These columns
    are explicitly referenced to plot the data.
    :param loc: A location used to identify the plot. It will show up in the
    plot name and file name (when the plot is saved)
    :return: None (a graph file is saved instead)
    """
    (x_range, y_range) = get_bounds(df.loc[:, ['lat', 'lon']].to_numpy(dtype=np.float32))

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(f"Nodes extracted from {loc}")
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.plot(df.lat, df.lon, linestyle='', marker='.', markersize=0.25)
    # plt.show()
    plt.savefig(f"sample_data/nodes_in_{loc}.png")


def extract_ways(file: str) -> pd.DataFrame:
    tree = ET.parse(file)
    root = tree.getroot()

    # children = []
    # for child in root:
    #     if child.tag not in children:
    #         children.append(child.tag)
    # print("Children of root: ", children)  # OUTPUT: ['bounds', 'node', 'way', 'relation']

    # count = 0
    # for way in root.findall("way"):
    #     count += 1
    # print(count)  # OUTPUT: 39791  (wow)

    nodes_with_way_id = []

    for way in root.findall("way"):
        # print(way.attrib)  # e.g. {'id': '8096030', 'version': '27', 'timestamp': '2021-03-10T17:40:50Z', 'changeset': '100793537', 'uid': '1824494', 'user': 'EdSS'}
        attribs = way.attrib
        way_id = int(attribs['id'])

        # for child in way:
        #     if child.tag not in way_tags:
        #         way_tags.append(child.tag)
        node_ids = []
        for node in way.findall("nd"):
            # print(node.attrib)  # output is a series of dictionaries like {'ref': '60656559'}
            # node_ids.append(int(node.attrib['ref']))
            nodes_with_way_id.append({'way_id': way_id, 'id': int(node.attrib['ref'])})
        # tags = []
        # for tag in way.findall('tag'):
        #     print(tag.attrib)

    # print("Potential children of ways: ", way_tags)  # OUTPUT: ["nd", "tag']

    return pd.DataFrame.from_records(nodes_with_way_id)

