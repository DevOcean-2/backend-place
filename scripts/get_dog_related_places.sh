#!/bin/bash

REST_API_KEY=""
LATITUDE=37.40270870047064
LONGITUDE=127.10332989692688
RADIUS=20000
QUERY="강아지"

echo "{" > temp.json
echo "\"documents\": [" >> temp.json

for PAGE in $(seq 1 45); do
    RESPONSE=$(curl -s -G "https://dapi.kakao.com/v2/local/search/keyword.json?x=$LONGITUDE&y=$LATITUDE&radius=$RADIUS&page=$PAGE" \
        -H "Authorization: KakaoAK $REST_API_KEY" \
        --data-urlencode "query=$QUERY")

    echo "$RESPONSE" | jq -c '.documents[]' | sed 's/^/,/' >> temp.json
done
sed -i '' '3s/^,//' temp.json

echo "]" >> temp.json
echo "}" >> temp.json

cat temp.json | jq '.documents | unique_by(.id) | sort_by(.category_name)' > place.json
rm temp.json
