#INPUT_FILE=~/Downloads/Searches/Searches/2016-04-01\ April\ 2016\ to\ June\ 2016.json
#INPUT_FILE=~/Downloads/Searches/Searches/2016-01-01\ January\ 2016\ to\ March\ 2016.json
#INPUT_FILE=$1

#jq '[.event[].query | select(.query_text | contains("->"))]' "$INPUT_FILE"


jq '[.event[].query | select(.query_text | contains("->"))]' ~/Downloads/Searches/Searches/* | jq -s add
