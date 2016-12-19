import gpxpy
import csv

f = open('me.gpx')
outf = open('links.csv', 'w')
csvout = csv.writer(outf)
gpx = gpxpy.parse(f)
print('parsing tracks')
for track in gpx.tracks:
    for segment in track.segments:
        first = segment.points[0]
        last = segment.points[-1]
        csvout.writerow([
            first.time,
            first.latitude,
            first.longitude,
            last.time,
            last.latitude,
            last.longitude,
            first.time_difference(last)])

outf.close()


