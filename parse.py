import json
from collections import Counter

with open("grype.json") as f:
    data = json.load(f)

high_count = medium_count = low_count = 0

for item in data["matches"]:
    try:
        score = item["vulnerability"]["cvssV2"]["baseScore"]
        # Low: 0.0-3.9; Medium: 4.0-6.9; High: 7.0-10.0
        if 7.0 <= score <= 10.0:
            high_count += 1
        elif 4.0 <= score <= 6.9:
            medium_count += 1
        else:
            low_count += 1
    except KeyError:
        continue

print(f"High: {high_count}, Medium: {medium_count}, Low: {low_count}")
