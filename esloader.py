import ujson as json
from argparse import ArgumentParser
from datetime import datetime

from elasticsearch import Elasticsearch
import elasticsearch.helpers as helpers
es = Elasticsearch()

index_name = 'history'
type_name = 'location'
mapping = {
    "properties": {
        'accuracy': {
            "type": "integer"
        },
        "activitys": {
            "type": "nested",
            "dynamic": False,
            "properties": {
                "activities": {
                    "type": "nested",
                    "dynamic": False,
                    "properties": {
                        "confidence": {
                            "type": "integer"
                        },
                        "type": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "timestampMs": {
                    "type": "string",
                    "index": "not_analyzed"
                }
            }
        },
        "point": {
            "type": "geo_point"
        },
        'latitude': {
            "type": "double"
        },
        'latitudeE7': {
            "type": "double"
        },
        'longitude': {
            "type": "double"
        },
        'longitudeE7': {
            "type": "double"
        },
        'timestamp': {
            "type": "date"
        },
        'timestampMs': {
            "type": "string",
            "index": "not_analyzed"
        }
    }
}

arg_parser = ArgumentParser()
arg_parser.add_argument("input", help="Input File (JSON)")
args = arg_parser.parse_args()
locations = json.load(open(args.input))['locations']

es.indices.delete(index=index_name, ignore=404)
es.indices.create(index=index_name)
es.indices.put_mapping(index=index_name, doc_type=type_name, body=mapping)

actions = []
for i, location in enumerate(locations):
    location["timestamp"] = datetime.fromtimestamp(int(location["timestampMs"]) / 1000)
    location["latitude"] = location['latitudeE7'] / 10000000
    location["longitude"] = location['longitudeE7'] / 10000000
    location["point"] = [location["longitude"], location["latitude"]]
    #es.index(index=index_name, doc_type=type_name, id=i, body=location)
    actions.append({
        "_index": index_name,
        "_type": type_name,
        "_id": i,
        "_source": location
    })

helpers.bulk(es, actions)
