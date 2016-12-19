#INPUT_FILE=~/Downloads/Searches/Searches/2016-04-01\ April\ 2016\ to\ June\ 2016.json

#jq '[.event[].query | select(.query_text | contains("->"))]' "$INPUT_FILE" | python search_parse.py | jq '[.[] | select(.timestamp_iso | contains("2016-04-26"))]'

TERM=$1
jq "[.[] | select(.timestamp_iso | contains(\"$TERM\"))]"
