# Extracting/Transforming raw OSM data for Navigation

**GOAL**: Use the OSM data to create BEV masks that identify where objects (e.g., roads, walkways, buildings, etc.) exist on a map.

Parker Dunn (pgdunn@bu.edu)  
Nov 29, 2022

## References

* All OSM data for planet updated and made available weekly [here](https://planet.openstreetmap.org)
  * Endpoint for the `planet-latest.osm.pbf` file is `https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf`
* `osmcovert` tool for converting `.pub` files (common format online) into `.osm` files (format you can work with)
  * [OSM wiki page](https://wiki.openstreetmap.org/wiki/Osmconvert)
  * OH! You can filter by geographic location. [wiki page - 3.2. Applying geographical boarders](https://wiki.openstreetmap.org/wiki/Osmconvert#Applying_Geographical_Borders)
* `osmfilter` tool for filtering ".osm" data
  * [Wiki page](https://wiki.openstreetmap.org/wiki/Osmfilter)

* Heidelberg Institute for Geoinformation Technology creates a database for the OSM data
  * [Starting page](https://heigit.org/a-basic-guide-to-osm-data-filtering/)

## Purpose

* Determine an optimal approach to retrieve and process data OSM data (XML-style files with extension `.osm` that 
  contain nodes, ways, relations, etc).

## Progress




