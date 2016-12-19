# tracky

First, download your Google Location History from Takeout. Choose location
history and search history.

# elasticsearch indexing

esloader.py - contains a mapping for location history entries and indexes location history json

directionsloader.py - contains a mapping for search history and indexes search history json
- First trim your search history with a jq command like this: `jq '[.event[].query | select(.query_text | contains("->"))]'`

# neo4j links:
Then, download this utility:
https://github.com/Scarygami/location-history-json-converter/commits/master/location_history_json_converter.py

Then, convert the location history from json to xml:

python location_history_json_converter.py -f gpxtracks -o me.gpx Takeout/Location\ History/LocationHistory.json

Then, run tracky.py

