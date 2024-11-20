#!/bin/bash

REST_API_KEY=""
LATITUDE=37.40270870047064
LONGITUDE=127.10332989692688
RADIUS=20000
QUERY="강아지 미용"

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

# place.json 생성 후, Python 스크립트를 실행하여 영업시간 정보를 추가
cat temp.json | jq '.documents | unique_by(.id) | sort_by(.category_name)' > place.json
rm temp.json

# 이미지 및 영업시간 정보를 가져오는 Python 스크립트 실행 코드
python3 ./fetch_opening_hours.py