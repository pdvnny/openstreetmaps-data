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
    x_bounds = [x_bounds[0] - (0.01 * x_range),
                x_bounds[1] + (0.01 * x_range)]

    y_bounds = [min(data[:, 1]), max(data[:, 1])]
    y_range = y_bounds[1] - y_bounds[0]
    y_bounds = [y_bounds[0] - (0.01 * y_range),
                y_bounds[1] + (0.01 * y_range)]
    return x_bounds, y_bounds


def get_color_options() -> Sequence[str]:
    color_options = ["#BE33FF",  # (1) violet
                    "#F60614",  # (2) red
                    "#108516",  # (3) forest green
                    "#FFA500",  # (4) orange
                    "#721A1A",  # (5) maroon
                    "#FF00FF",  # (6) magenta
                    "#76D77A",  # (7) pastel/light green
                    "#96C3E6",  # (8) pastel dark blue
                    "#CFD33C",  # (9) golden rod
                    "#CCCCFF",  # (10) pastel/light purple
                    "#99A3A4",  # (11) grey
                    "#F7DC6F",  # (12) light yellow
                    "#008080",  # (13) teal
                    "#BF5700",  # (14) burnt orange
                    "#96E6E6",  # (15) pastel/light SKY blue
                    "#000000",  # (16) black
                    "#808000",  # (17) olive
                    "#2300ff",  # (18) blue
                    "#00FF00",  # (19) lime
                    "#000080",  # (20) navy blue
                    "#FA8072",  # (21) salmon
                    "#40E0D0",  # (22) light green/blue
                    "#F5A2D0",  # (23) light pink
                    "#F5CFA2",  # (24) light orange
                    "#27AE60",  # (25) normal green - name that I made up
                    "#1D7A74"   # (26) dark teal
                    ]
    return color_options


# ------------- FUNCTIONS FOR WORKING WITH OSM DATA -------------


"GOAL 1: Extract features and plot the locations using matplotlib"


def extract_nodes(filename: str) -> pd.DataFrame:
    """
    This method converts the node data in an OSM file (XML-style format)
    into a Pandas DataFrame containing "id", "lat", and "lon" of the node.

    This method is designed for `.osm` files that have been processed to
    extract the node objects.

    :param filename: A filename/path for a `.osm` file with node objects
                     (e.g., boston_nodes.osm)
    :return: If the file exists, a pandas DataFrame with rows for each Node in the provided file.
             If the file DOES NOT exist, then None.
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


def extract_ways(loc_dir: str, file: str) -> pd.DataFrame:
    """
    This method loads a ".osm" file provided as an input and extracts information
    about the way objects in the file. The contributing nodes are returned as a
    DataFrame so that they can be merged with the node location data. The **way tags**
    are also extracted and saved in a JSON file.

    :param loc_dir: The city name tha identifies the subdirectory where this data comes from
    :param file: The path to a file containing OSM "way" objects (XML-style)
    :return: a DataFrame with three columns (for now): "way_id" and "id".
            "way_id" is an identifier for the particular way
            "id" is an identifier of a node that is a member of the way since
            a way is a higher order object composed of nodes.
    """
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
        tags = dict()
        for tag in way.findall('tag'):
            key = tag.attrib['k']
            value = tag.attrib['v']
            tags[key] = value

        if len(tags) != 0 and not os.path.isdir(f"sample_data/{loc_dir}_ways"):
            os.mkdir(f"sample_data/{loc_dir}_ways")

        # way_attributes_file = f"sample_data/{loc_dir}_ways/way_{way_id}.json"
        # with open(way_attributes_file, 'w') as wf:
        #     json.dump(tags, wf)

    # print("Potential children of ways: ", way_tags)  # OUTPUT: ["nd", "tag']

    return pd.DataFrame.from_records(nodes_with_way_id)


def extract_ways_with_tag(file: str, target_tag: str, values: Sequence[str]) -> pd.DataFrame:
    """
    To be continued...

    :param file: The path to a file containing OSM "way" objects (XML-style)
    :param tag:
    :param values:
    :return: a DataFrame with three columns: "way_id", "id" (i.e., node_id), and
            the tag provided.
            "way_id" is an identifier for the particular way
            "id" is an identifier of a node that is a member of the way since
            a way is a higher order object composed of nodes.
            The final column will list the value associated with the tag provided.
            e.g., If we are looking for ways with the tag "highway", the column
            would be "highway" and the values for each row will be one of the options
            in "values"
    """
    tree = ET.parse(file)
    root = tree.getroot()

    nodes_with_way_id = []

    for way in root.findall("way"):
        # RETRIEVE THE WAY ID
        attribs = way.attrib
        way_id = int(attribs['id'])

        # RETRIEVE THE ATTRIBUTES OF THIS WAY
        tags = dict()
        for tag in way.findall('tag'):
            key = tag.attrib['k']
            value = tag.attrib['v']
            tags[key] = value

        # RETRIEVE ALL NODE IDS THAT ARE PART OF THE WAY
        # IF IT CONTAINS THE REQUESTED TAG
        value = tags.get(target_tag)    # "tags.get(tag)" -> the tag value if it exists or None if the tag does not exist
        if value is not None and value in values:
            for node in way.findall("nd"):
                new_entry = {'way_id': way_id, 'id': int(node.attrib['ref']), target_tag: value}
                nodes_with_way_id.append(new_entry)

        # end of for loop
    return pd.DataFrame.from_records(nodes_with_way_id)


def plot_ways(df: pd.DataFrame, loc: str) -> str:
    """
    This method plots the way data from an OSM data file with multiple colors. Although,
    there is repetition of the colors in the plot.

    :param df: (CONFIGURATION OF INPUT DATA MAY CHANGE) This is a DataFrame
                containing "node" and "way" data created by performing
                a left join on (1) a DataFrame with "way" data and (2) a DataFrame
                with "node" data.
    :param loc: A location used to identify the plot. It will show up in the
    plot name and file name (when the plot is saved)
    :return: A string containing plot file name
    """
    colors = get_color_options()
    (x_range, y_range) = get_bounds(df.loc[:, ["lon", "lat"]].to_numpy(dtype=np.float32))

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_title(f"Ways in {loc} (from {loc}.osm)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)

    color_counter = 0
    plotted_counter = 0
    for way in df.way_id.unique():  # iterate through all the way ids
        way_filter = (df.way_id == way)
        x = df.loc[way_filter, "lon"].tolist()
        y = df.loc[way_filter, "lat"].tolist()
        # print(type(x), x)
        # print(type(y), y)
        ax.plot(x, y, color=colors[color_counter])
        color_counter += 1
        plotted_counter += 1
        if color_counter >= len(colors):
            color_counter = 0
        if plotted_counter > 10000:
            break
    # plt.show()
    fname = f"sample_data/{loc}_ways_1000.png"
    plt.savefig(fname)
    return fname


def plot_ways_with_tag(df: pd.DataFrame, loc: str) -> str:
    """
    This method plots the way data FOR A SPECIFIC TAG (e.g, the way tagged
    with "highway") from an OSM data file

    :param df: (CONFIGURATION OF INPUT DATA MAY CHANGE) This is a DataFrame
                containing "node" and "way" data created by performing
                a left join on (1) a DataFrame with "way" data and (2) a DataFrame
                with "node" data.
    :param loc: A location used to identify the plot. It will show up in the
    plot name and file name (when the plot is saved)
    :return: A string containing plot file name
    """
    colors = get_color_options()
    (x_range, y_range) = get_bounds(df.loc[:, ["lon", "lat"]].to_numpy(dtype=np.float32))

    color_opts = {
        "motorway": colors[0],
        "trunk": colors[1],
        "primary": colors[2],
        "secondary": colors[3],
        "tertiary": colors[4],
        "residential": colors[5],
        "motorway_link": colors[6],
        "trunk_link": colors[6],
        "primary_link": colors[6],
        "secondary_link": colors[6],
        "tertiary_link": colors[6],
        "living_street": colors[7]
    }

    # Finds the name of the attribute being plotted
    cols = df.columns  # This probably isn't reliable
    tag = None
    for col in cols:
        if col not in ["way_id", "id", "lat", "lon"]:
            tag = col
    # print(tag)

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_title(f"Ways with '{tag}' tag in {loc} (from {loc}.osm)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)

    for way in df.way_id.unique():  # iterate through all the way ids
        way_filter = (df.way_id == way)
        tag_value = df.loc[way_filter, tag].unique()[-1]
        print(tag_value)
        x = df.loc[way_filter, "lon"].tolist()
        y = df.loc[way_filter, "lat"].tolist()
        ax.plot(x, y, color=color_opts[tag_value])

    fname = f"sample_data/{loc}_ways_with_tag_{tag}.png"
    plt.savefig(fname)
    return fname


def extract_relations(loc_dir: str, file: str) -> pd.DataFrame:
    """
    This method loads a ".osm" file provided as an input and extracts information
    about the relations in the file. The contributing nodes are returned as a
    DataFrame so that they can be merged with the node location data.

    :param loc_dir: The city name that identifies the subdirectory where this data comes from
    :param file: The path to a file containing OSM "relations" (XML-style)
    :return: a DataFrame with two columns (for now): "rel_id" and "id".
            "rel_id" is an identifier for the particular relation
            "id" is an identifier of a node that is a member of the way since
            a way is a higher order object composed of nodes.
    """
    tree = ET.parse(file)
    root = tree.getroot()

    # count = 0
    # for rel in root.findall("relation"):
    #     count += 1
    # print(f"Number of relations: {count}")   # OUTPUT: 1867

    members_and_rel_id = []

    # Debugging
    counter = 0
    # all_tags = set()

    for rel in root.findall("relation"):
        # print(rel.attrib)
        # e.g.
        # {'id': '38047', 'version': '11', 'timestamp': '2021-08-21T03:36:20Z',
        # 'changeset': '110011439', 'uid': '7470367', 'user': 'JesseFTW'}
        attribs = rel.attrib
        rel_id = int(attribs['id'])

        # rel_tags = set()

        # This loop style could work.
        # `child.tag` can be used to identify nodes vs. tags
        # A condition would be needed to check which one I am dealing with
        # but it would only require one iteration through the data instead of two
        # for child in rel:
        #     print(child)
        #     # e.g., <Element 'member' at 0x0000013A5885710>
        #     # e.g., <Element 'tag' at 0x000001B16E5F63E0>
        #     print(child.attrib)
        #     # e.g., Member: {'type': 'node', 'ref': '61317423', 'role': 'via'}
        #     # e.g., Member: {'type': 'way', 'ref': 115591269', 'role': 'from'}
        #     # e.g., Member: {'type': 'way', 'ref': '426580269', 'role': 'to'}
        #     # e.g., Tag: {'k': 'addr:housenumber', 'v': '4'}
        #    # NOTE: `child.tag` returns 'tag' and 'nd'

        # for tag in rel.findall('tag'):
        #     tag_dict = tag.attrib
        #     rel_tags.add(tag_dict['k'])
        #     all_tags.add(tag_dict['k'])

        # counter += 1
        # if counter > 10:
        #     break

        for member in rel.findall("member"):
            member_dict = member.attrib
            if member_dict['type'] == 'way':
                members_and_rel_id.append({'rel_id': rel_id,
                                           'way_id': int(member_dict['ref']),
                                           'node_id': 0
                                           })
            else:
                members_and_rel_id.append({'rel_id': rel_id,
                                           'way_id': 0,
                                           'node_id': int(member_dict['ref'])
                                           })

    # print("The tags in all relations from this file: ")
    # with open("sample_data/boston_relation_tags.txt", 'a') as f:
    #     for tag in all_tags:
    #         print(tag)
    #         f.write(tag)
    #         f.write("\n")
    # print("length of records:", len(members_and_rel_id))
    return pd.DataFrame.from_records(members_and_rel_id)


def extract_relations_with_tag(file: str, target_tag: str) -> pd.DataFrame:
    """
    This method extracts the nodes and ways (by ID) associated with relations
    containing the "target_tag" (e.g., a relation may contain a tag element with
    the key "building").
    This function finds all matching relations and returns a DataFrame
    containing information about the relations.

    :param file: The path to the file containing OSM data (XML-format)
    :param target_tag: A tag that all extracted relations should have.
    :return: A DataFrame
    IF there are relations with the "target_tag", then there will be a row for each
    member of the relation. Rows for nodes have a valid node ID and a way ID of 0.
    Rows for ways have a valid way ID and a node ID of 0.

    IF there are NO relations with the "target_tag", then the returned dataframe
    is empty.
    """
    tree = ET.parse(file)
    root = tree.getroot()

    members_and_rel_id = []
    for rel in root.findall("relation"):
        attribs = rel.attrib
        rel_id = int(attribs['id'])

        rel_tags = set()
        for tag in rel.findall("tag"):
            tag_dict = tag.attrib
            rel_tags.add(tag_dict['k'])

        if target_tag in rel_tags:
            for member in rel.findall("member"):
                member_dict = member.attrib
                if member_dict['type'] == 'way':
                    members_and_rel_id.append({'rel_id': rel_id,
                                               'way_id': int(member_dict['ref']),
                                               'node_id': 0
                                               })
                else:
                    members_and_rel_id.append({'rel_id': rel_id,
                                               'way_id': 0,
                                               'node_id': int(member_dict['ref'])
                                               })
    return pd.DataFrame.from_records(members_and_rel_id)



