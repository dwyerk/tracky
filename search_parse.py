import ujson as json
import sys
from datetime import datetime

js = json.load(sys.stdin)

for obj in js:
    obj['timestamp'] = datetime.fromtimestamp(int(obj['id'][0]['timestamp_usec']) / 1000000)
    obj['timestamp_iso'] = obj['timestamp'].isoformat()

js = sorted(js, key=lambda q: q['timestamp'])

print(json.dumps(js, indent=4))
