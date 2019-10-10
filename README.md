# tracky

This project started out as a talk I gave at a company hackathon. During the hackathon I cobbled together some scripts
to index my location history as capture by Google and showed that Google doesn't have to try hard to know everything
about my life, based on location history alone.

If you want to index your own data, first download your Google Location History from Takeout. Choose location
history and search history.

# elasticsearch indexing

Choose one of the following ingest methods.

## The logstash Way

Just unzip your Google Takeout in the root of this repository, run `docker-compose up`, and logstash will take care of the rest.
You'll know it's working because the fans on your laptop will hit max RPM in a minute or so. This can take a bit of time,
but you can watch the progress in kibana.

## The Python Way
esloader.py - contains a mapping for location history entries and indexes location history json

## Index your google maps direction requests
directionsloader.py - contains a mapping for search history and indexes search history json
- First trim your search history with a jq command like this: `jq '[.event[].query | select(.query_text | contains("->"))]'`

# Kibana

Load up Kibana to explore your history at: http://localhost:5601

You will need to create at least one index pattern. For this data, it makes sense to start with `history*`.

# Extra stuff
Useful utility if you need your history in XML:
https://github.com/Scarygami/location-history-json-converter/commits/master/location_history_json_converter.py

`python location_history_json_converter.py -f gpxtracks -o me.gpx Takeout/Location\ History/LocationHistory.json`
