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
from matplotlib import pyplot as plt
import os

import typing
import json

"GOAL 1: Extract features and plot the locations using matplotlib"



