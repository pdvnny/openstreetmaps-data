from src import osmdata
import json
import glob

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon

if __name__ == "__main__":
    # ----------------------------------- RELOADING NODE DATA -----------------------------------------
    nodes_df = pd.read_csv("sample_data/boston_nodes.csv", index_col=0)

    # __________________________________ LOADING WAYS DATA --------------------------------------------
    ways_df = osmdata.extract_ways("boston", "sample_data/boston.osm")
    # Columns: "way_id" and "id"

    # ----------------------------- Extracting higher order OSM features ------------------------------
    # EXTRACTING RELATIONS WITH A SPECIFIC FEATURE
    relations_df = osmdata.extract_relations_with_tag("sample_data/boston.osm", "building")
    # Columns: "rel_id", "way_id", "node_id"
    # (only one of "way_id" or "node_id" has a valid entry in each row)

    # ---------------------------- Preparation of relations_df --------------------------------------
    # drop entries in `relations_df` without a "way_id"
    drop_filter = (relations_df.way_id != 0)
    relations_df = relations_df.loc[drop_filter, ["rel_id", "way_id"]]

    # --------------------------- MERGE: relations_df -> ways_df -> nodes_df --------------------------
    # print(nodes_df.dtypes)
    # print(ways_df.dtypes)   # All ID columns were of type "int64"

    data_df = (relations_df
               .merge(ways_df, how='inner', on='way_id')
               .merge(nodes_df, how='inner', on='id')
               )
    # Example: # ways_data = ways_df.merge(nodes_df, on='id', how='left', suffixes=('_l', '_r'))

    # debugging
    # data_df = relations_df.merge(ways_df, how='inner', on='way_id')
    # realized I probably need to swtich "left" to "inner"

    # print(data_df.iloc[:10, :])

    # -------------------------- SELECT 4 RELATIONS TO PLOT ------------------------------------------
    rel_opts = data_df.rel_id.unique()
    # print(rel_opts)
    rel_filter = [True if i in rel_opts[:4] else False for i in data_df.rel_id]
    # print(len(data_df.loc[rel_filter, :]))
    data_df = data_df.loc[rel_filter, :]

    # ---------------------------- PLOT WAYS VS RELATIONS ------------------------------------------
    def prep_data_for_plotting(data: pd.DataFrame, relation_id: int):
        """
        *To be filled in later...*
        :param data:
        :param relation_id:
        :return:
        """
        relation_filter = data.rel_id == relation_id
        rel_data = data.loc[relation_filter, :]

        rel_data_np = rel_data.loc[:, ["lat", "lon"]].to_numpy()
        # print("rel_data_np:", rel_data_np.shape)  # Example: (97,2)

        way_data_list = []
        for way in rel_data.way_id.unique():
            way_filter = rel_data.way_id == way
            way_data_np = rel_data.loc[way_filter, ["lat", "lon"]].to_numpy()
            # print("way_data_np:", way_data_np.shape)
            # Examples:
            # (87, 2)
            # (5, 2)
            # (5, 2)
            way_data_list.append(way_data_np)

        return rel_data_np, way_data_list

    # PLOT SETUP
    fig = plt.figure(constrained_layout=True, figsize=(10, 16))  # Helpful: https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
    # grid = plt.GridSpec(4, 2, hspace=0.8)
    sub_figs = fig.subfigures(4, 1, hspace=0.05)

    # --- OLD APPROACH ---
    # fig, ax = plt.subplots(4, 2, sharey='row', figsize=(8, 14))
    # axes = ax.flatten()

    for plot_num, relation in enumerate(data_df.rel_id.unique()):
        # PREPARE DATA
        rel_plot_data, way_plot_data = prep_data_for_plotting(data_df, relation)

        # PREPARE STYLE/FORMATTING
        x_range, y_range = osmdata.get_bounds(rel_plot_data)
        colors = osmdata.get_color_options()
        color = iter(colors)

        # CALCULATE SUBPLOT INDICES FOR THE DATA
        plot_loc_rel, plot_loc_ways = plot_num * 2, plot_num * 2 + 1

        # GRAP CURRENT FIGURE AND CREATE AXES
        # Helpful ref: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subfigures.html#sphx-glr-gallery-subplots-axes-and-figures-subfigures-py
        (nodes_plot, ways_plot) = sub_figs[plot_num].subplots(1, 2, sharey=True)
        # Debugging
        # sub_figs[plot_num].set_facecolor('0.75')

        sub_figs[plot_num].suptitle(f"Relation #{relation}")

        # ADD THE NODES DATA
        nodes_plot.set_ylabel("Latitude")
        nodes_plot.set_xlabel("Longitude")
        # nodes_plot.set_title("All nodes in the relation")
        nodes_plot.set_xlim(x_range)
        nodes_plot.set_ylim(y_range)
        nodes_plot.plot(rel_plot_data[:, 0], rel_plot_data[:, 1], color="#000000", marker=".", linestyle="")

        # ADD THE WAY DATA
        ways_plot.set_xlabel("Longitude")
        ways_plot.set_xlim(x_range)
        for way in way_plot_data:
            way_obj = Polygon(way, closed=True, alpha=0.4, facecolor=next(color), edgecolor="#000000")
            ways_plot.add_patch(way_obj)

    fig.suptitle("Comparing raw node data with higher-order way and relation data", fontsize='xx-large')
    plt.show()
    fig.savefig("images/relation_components_visualization.png")

    # REFORMATTING THIS CODE FOR A NEW PLOT FORMAT
    #     axes[plot_loc_rel].set_ylabel("Latitude")
    #     # ADD THE RELATION DATA
    #     axes[plot_loc_rel].set_xlabel("Longitude")
    #     axes[plot_loc_rel].set_xlim(x_range)
    #     axes[plot_loc_rel].set_ylim(y_range)
    #     # axes[plot_loc_rel].grid(visible=True)
    #     axes[plot_loc_rel].plot(rel_plot_data[:, 0], rel_plot_data[:, 1], color="#000000", marker=".", linestyle="")
    #
    #     # ADD THE WAY DATA
    #     axes[plot_loc_ways].set_xlabel("Longitude")
    #     axes[plot_loc_ways].set_xlim(x_range)
    #     # axes[plot_loc_ways].grid(visible=True)
    #     for way in way_plot_data:
    #         # axes[plot_loc_ways].plot(way[:, 0], way[:, 1], color=next(color), marker=".", linestyle="-")
    #         way_obj = Polygon(way, closed=True, alpha=0.4, facecolor=next(color), edgecolor="#000000")
    #         axes[plot_loc_ways].add_patch(way_obj)
    #         # Refs
    #         # (1) https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.add_patch.html
    #         # (2) https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Polygon.html
    #
    #     # FINAL FORMATTING
    #     plt.subplots_adjust(hspace=0.8)

# More refs:
# (1) https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html