import os
import json
import csv
from collections import Counter

def countCVE():
    with open("backup/scan_results.json", "r") as f:
        data = json.loads(f.read())
        keys = data.keys()
        print("image,num_vulns,")
        for i in keys:
            count = len(data[i]["matches"])
            print(f"{i},{count},")


def countPackages():
    with open("backup/scan_results.json", "r") as f:
        data = json.loads(f.read())
        keys = data.keys()
        pkg_count = Counter()

        for i in keys:
            matches = data[i]["matches"]
            for m in matches:
                pkg_count.update({m["artifact"]["name"] : 1})
        
        with open("pkgcount.csv", "w") as csvfile:
            fieldnames=["Package", "Count"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for key, value in pkg_count.items():
                writer.writerow([key]+[value])



if __name__ == '__main__':
    # countCVE()
    countPackages()