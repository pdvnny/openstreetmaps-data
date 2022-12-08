from src import osmdata
import json
import glob

if __name__ == "__main__":
    nodes_df = osmdata.extract_nodes("sample_data/boston_nodes.osm")
    print(nodes_df.iloc[:5, :])


