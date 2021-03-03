import os
import json
import csv
from collections import Counter

def countCVE(filename):
    with open(filename, "r") as f:
        data = json.loads(f.read())
        keys = data.keys()
        print("image,num_vulns,")
        for i in keys:
            count = len(data[i]["matches"])
            print(f"{i},{count},")


def countPackages(filename):
    with open(filename, "r") as f:
        data = json.loads(f.read())
        keys = data.keys()
        c = Counter()

        for i in keys:
            matches = data[i]["matches"]
            for m in matches:
                c.update({m["artifact"]["name"] : 1})
        
        with open("pkgcount.csv", "w") as csvfile:
            fieldnames=["Package", "Count"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for key, value in c.items():
                writer.writerow([key]+[value])

def countCritCVE(filename):
    with open(filename, "r") as f:
        data = json.loads(f.read())
        keys = data.keys()
        c = Counter()

        for i in keys:
            matches = data[i]["matches"]
            for m in matches:
                if m["vulnerability"]["severity"] == "High":
                    c.update({m["vulnerability"]["id"] : 1})

        with open("critcount.csv", "w") as csvfile:
            fieldnames=["CVE", "Count"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for key, value in c.items():
                writer.writerow([key]+[value])






if __name__ == '__main__':
    filename = "backup/scan_results.json"
    # countCVE(filename)
    # countPackages(filename)
    countCritCVE(filename)