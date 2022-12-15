# Process for Extracting and Storing Information from `.osm` Files

I am extracting and reformating the data so that I can manipulate the information and generate new data.

Parker Dunn (pgdunn@bu.edu)  
Dec 14, 2022

## References


## To Do

- [ ] I extracted the nodes, but need to backtrack and make updates
    - [ ] Extract and store `tag` information (I did not extract any 'metadata' type information yet)

- [ ] I am skipping extracting `tag`s from the `<way>` objects as well. There are many data points to extract. I'll 
  try to sort out what I need later.

e.g., A `way` from near Fenway
```python
  {'k': 'addr:city', 'v': 'Boston'}
  {'k': 'addr:housenumber', 'v': '4'}
  {'k': 'addr:postcode', 'v': '02115'}
  {'k': 'addr:state', 'v': 'MA'}
  {'k': 'addr:street', 'v': 'Jersey Street'}
  {'k': 'architect', 'v': 'James E. McLaughlin'}
  {'k': 'capacity', 'v': '37755'}
  {'k': 'email', 'v': 'events@redsox.com'}
  {'k': 'layer', 'v': '0'}
  {'k': 'leisure', 'v': 'stadium'}
  {'k': 'material', 'v': 'brick'}
  {'k': 'name', 'v': 'Fenway Park'}
  {'k': 'operator', 'v': 'Fenway Sports Group;Boston Red Sox'}
  {'k': 'phone', 'v': '+1-877-733-7699'}
  {'k': 'phone:mnemonic', 'v': '+1-877-REDSOX-9'}
  {'k': 'smoking', 'v': 'no'}
  {'k': 'sport', 'v': 'baseball'}
  {'k': 'start_date', 'v': '1912-04-20'}
  {'k': 'website', 'v': 'https://www.mlb.com/redsox/ballpark'}
  {'k': 'wikidata', 'v': 'Q49136'}
  {'k': 'wikipedia', 'v': 'en:Fenway Park'}
```