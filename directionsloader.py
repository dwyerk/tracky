import ujson as json
from argparse import ArgumentParser
from datetime import datetime

from elasticsearch import Elasticsearch
import elasticsearch.helpers as helpers
es = Elasticsearch()

index_name = 'queries'
type_name = 'directions'
mapping = {
    "properties": {
        "id": {
            "type": "nested",
            "dynamic": False,
            "properties": {
                "timestamp_usec": {
                    "type": "string",
                    "index": "not_analyzed"
                }
            }
        },
        "timestamp_iso": {
            "type": "date"
        },
        "timestamp": {
            "type": "date"
        },
        "query_text": {
            "type": "string"
        },
        "query_text_not_analyzed": {
            "type": "string",
            "index": "not_analyzed"
        }
    }
}

arg_parser = ArgumentParser()
arg_parser.add_argument("input", help="Input File (JSON)")
args = arg_parser.parse_args()
queries = json.load(open(args.input))

es.indices.delete(index=index_name, ignore=404)
es.indices.create(index=index_name)
es.indices.put_mapping(index=index_name, doc_type=type_name, body=mapping)

actions = []
for i, query in enumerate(queries):
    query['query_text_not_analyzed'] = query['query_text']
    actions.append({
        "_index": index_name,
        "_type": type_name,
        "_id": i,
        "_source": query
    })

helpers.bulk(es, actions)
