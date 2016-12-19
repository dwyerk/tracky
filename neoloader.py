from py2neo import Graph, Node, Relationship
import csv
import geohash
import requests

gaz_fmt = "http://gaz.thehumangeo.com/gaz/coordinates2place/?latitude={latitude}&longitude={longitude}"
def gaz_it_up(geo_hash):
    lat, lon = geohash.decode(geo_hash)
    response = requests.get(gaz_fmt.format(latitude=lat, longitude=lon)).json()
    return response

graph = Graph('http://neo4j:location@localhost:7474/db/data/')
#graph.cypher.execute("MATCH(n:Geohash) DETACH DELETE n")
graph.delete_all()
geohash_label = "Geohash"
try:
    graph.schema.create_uniqueness_constraint(geohash_label, "name")
except Exception:
    pass

### dedupe the links so that two points that are near each other are resolved to the same point. use geohash?

inf = open('links.csv')
hashes = {}
for i, row in enumerate(csv.reader(inf)):
    first_hash = geohash.encode(float(row[1]), float(row[2]), 6)
    last_hash = geohash.encode(float(row[4]), float(row[5]), 6)
    if first_hash != last_hash: # it would be better to eliminate these by duration instead
        hashes.setdefault(first_hash, []).append(last_hash)

for src_geohash, destinations in hashes.items():
    source = Node(geohash_label, name=src_geohash)
    print("creating {} with {} destinations".format(src_geohash, len(destinations)))
    #graph.merge_one(geohash_label, source)
    matches = list(graph.find(geohash_label, property_key="name", property_value=src_geohash))
    if matches:
        source = matches[0]
    else:
        geo = gaz_it_up(src_geohash)
        source.properties["admin1"] = geo["admin1"]
        source.properties["admin2"] = geo["admin2"]
        source.properties["asciiname"] = geo["asciiname"]
        source.properties["geoname"] = geo["name"]
        graph.create(source)

    for dest in destinations:
        print("dest=",dest)
        destination = Node(geohash_label, name=dest)
        #graph.merge_one(geohash_label, destination)
        matches = list(graph.find(geohash_label, property_key="name", property_value=dest))
        if matches:
            destination = matches[0]
        else:
            geo = gaz_it_up(dest)
            destination.properties["admin1"] = geo["admin1"]
            destination.properties["admin2"] = geo["admin2"]
            destination.properties["asciiname"] = geo["asciiname"]
            destination.properties["geoname"] = geo["name"]
            graph.create(destination)
        graph.create(Relationship(source, "track_to", destination))

#for record in graph.cypher.execute("MATCH (p:Point) RETURN p"):
#    print('record:', record)

