import os
import json
import csv
from collections import Counter

def countPUN(filename):
    with open(filename, "r") as f:
        data = json.loads(f.read())
        c = Counter()
        high = Counter()
        for item in data:
            for entry in item["cves"]:
                pun = entry["pun"]
                severity = entry["severity"]
                c.update({pun : 1})
                if severity in ["Critical", "High"]:
                    high.update({pun : 1})
 

        print(f"Count of severity {c}")
        print(f"Crit+High Type {high}")

        # for i in keys:
        #     matches = data[i]["matches"]
        #     for m in matches:
        #         if m["vulnerability"]["severity"] == "High":
        #             c.update({m["vulnerability"]["id"] : 1})

        # with open("critcount.csv", "w") as csvfile:
        #     fieldnames=["CVE", "Count"]
        #     writer = csv.writer(csvfile)
        #     writer.writerow(fieldnames)
        #     for key, value in c.items():
        #         writer.writerow([key]+[value])

if __name__ == '__main__':
    filename = "backup/extracted_v2.json"
    countPUN(filename)