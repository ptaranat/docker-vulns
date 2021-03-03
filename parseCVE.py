import os
import json

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
        for i in keys:
            matches = data[i]["matches"]
            for m in matches:
                print(m["artifact"]["name"])



if __name__ == '__main__':
    # countCVE()
    countPackages()