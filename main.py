from src import osmdata
import json
import glob
import pandas as pd

if __name__ == "__main__":
    # EXTRACTING NODE DATA
    # nodes_df = osmdata.extract_nodes("sample_data/boston_nodes.osm")
    # print(nodes_df.iloc[:5, :])

    # Identifying missing values
    # print("Number of missing values:\n", nodes_df.isna().sum())

    # SAVING NODE DATA
    # Saving the Boston nodes to "csv" file
    # nodes_df.to_csv("sample_data/boston_nodes.csv")
    # osmdata.plot_nodes(nodes_df, "Boston")

    # ----------------------------------- RELOADING NODE DATA -----------------------------------------
    nodes_df = pd.read_csv("sample_data/boston_nodes.csv", index_col=0)
    # print(nodes_df.iloc[:5, :])

    # ----------------------------- Extracting higher order OSM features ------------------------------
    # EXTRACTING ALL WAYS
    # ways_df = osmdata.extract_ways("boston", "sample_data/boston.osm")

    # EXTRACTING WAYS WIHT A SPECIFIC FEATURE
    accepted_values = ["motorway", "trunk", "primary", "secondary", "tertiary", "residential", "motorway_link",
                       "trunk_link", "primary_link", "secondary_link", "tertiary_link", "living_street"]
    ways_df = osmdata.extract_ways_with_tag("sample_data/boston.osm", "highway", accepted_values)

    # print(ways_df.iloc[:5, :])

    # ------------- SAMPLE OF A NEXT STEP: Completing the "way" data by merging with nodes_df -----------
    # print("Number of nodes: ", len(nodes_df))  # 184,675
    # print("Number of nodes in ways: ", len(ways_df))  # 294,715
    # Number of nodes is smaller so some nodes exist in multiple ways

    ways_data = ways_df.merge(nodes_df, on='id', how='left', suffixes=('_l', '_r'))

    # print(ways_data.iloc[:5, :])
    # print("Number of entries in merged data:", len(ways_data))

    # --------------------- Extracting a sample way from "ways_data" -----------------------------------
    # my_way_id = 8096030
    # my_way = ways_data.loc[ways_data.way_id == my_way_id, ["lat", "lon"]]
    # print(my_way.iloc[:10, :])

    # ------------------------------- Plotting the way data -------------------------------------------
    filename = osmdata.plot_ways_with_tag(ways_data, "boston")
