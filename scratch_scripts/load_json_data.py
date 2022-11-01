import json
import os

if __name__=="__main__":
    for f in os.listdir("../location_json_files"):
        print(f)

    files_list = os.listdir("../location_json_files")
    for file in files_list:
        file = "location_json_files/"+file
        with open(file, 'r') as f:
            data = json.load(f)
        print(data['location'])

"""
import json
import glob

-------

files_list = glob.glob("location_json_files")
for file in files_lst:
    with open(file, 'r') as f:
        info = json.load(f)
    location = info['location']
    region = info['region']
     
"""