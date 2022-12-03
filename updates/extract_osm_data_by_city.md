# Information about Extracting OSM data from Planet OSM File

Parker Dunn (pgdunn@bu.edu)  
Nov 29, 2022

## References

* All OSM data for planet updated and made available weekly [here](https://planet.openstreetmap.org)
  * Endpoint for the `planet-latest.osm.pbf` file is `https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf`

* `osmfilter` tool for filtering ".osm" data
  * [Wiki page](https://wiki.openstreetmap.org/wiki/Osmfilter)

* `osmconvert` tool for converting compressed OSM data (`.pbf`) to other formats (that are more usable I think - e.g.
  , `.o5m` and `.osm`)
  * [Wiki page](https://wiki.openstreetmap.org/wiki/Osmconvert)
  * This tool actually has an option to filter by location! (see: 
    [/osmconvert#Clipping_based_on_Longitude_and_Latitude](https://wiki.openstreetmap.org/wiki/Osmconvert#Clipping_based_on_Longitude_and_Latitude))

* Heidelberg Institute for Geoinformation Technology creates a database for the OSM data
  * [Starting page](https://heigit.org/a-basic-guide-to-osm-data-filtering/)

## Purpose

Rather than querying the OSM API, and potentially waiting a long time for data, it looks like there are tools 
available to filter the planet OSM data.

## Using `osmconvert` to Extract OSM data from Specific Locations by Coordinates

You can easily get a compiled program that does conversion of OSM data files (`.pbf`, `.osm`, `.o5m`). I don't know 
if there is a purpose for each of the formats, especially `o5m`, but it seems that most large files like ["Planet 
OSM"](https://planet.openstreetmap.org) come as `.pbf` which appears to be a compressed file format.

There seems to be three options for getting OSM data:
1. Visit the OpenStreetMaps website and select extract for a region (the "by hand" option) ... less than ideal
2. Query an OSM API for region specific data ... automated but not extremely reliable in my opinion.
3. Download a large file once, and extract the data that you want.

The `osmconvert` program helps with the **third option**.

### First, download and compile the `osmconvert` executable

The `osmconvert` tool is actually just a C program provided [here](http://m.m.i24.cc/osmconvert.c). On the Wiki page 
(above), there are binaries provided and a handful of approaches for downloading and compiling the executable.

It's not particularly hard, so here is what I did:
1. Downloaded the C program `osmconvert.c` from this link: http://m.m.i24.cc/osmconvert.c --> `wget -O osmconvert.c 
   http://m.m.i24.cc/osmconvert.c`
2. Compiled the code using `gcc` (or you could use `cc`): `gcc osmconvert.c -lz -O3 -o osmconvert`

### Next, `osmconvert` is available, and you can process `.pbf` files from OpenStreetMaps

1. Get the latest file with the planet's OSM data (this step takes a while since the compressed file is 66 GB or 
   something like that. Run `wget https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf`

2. Convert the compressed file format to a usable format: `osmconvert planet-latest.osm.pbf -o=planet-latest.o5m`

*WARNING: I believe this takes a bit of time. I think it was 5 - 20 minutes, but I did not keep track of exactly how 
long.*  

This step is not absolutely necessary. I'm pretty sure you can convert directly from `.pbf` to `.osm` and filter for 
a specific location at the same time. The process was pretty slow though. I'm not sure how long it would have taken 
to finish. I believe the creator listed on the Wiki page how long the conversion from `.pbf` to `.o5m` would take, 
and it was only a couple minutes, so it felt like a good intermediate step to take.  

3. Convert the `o5m` file to `osm` and filter for a specific location. The location you want is provided as a 
   lon/lat bounding box. The values below (listed after the `-b` are specific to the region that you want to 
   extract: Boston in this example).

To get the data for Boston: `osmconvert planet-latest.o5m -b=-71.1128,42.3394,-71.0400,42.3707 -o=boston.osm`

