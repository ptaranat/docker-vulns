import os
import json
from jsonslicer import JsonSlicer


def generateData():
    with open("./outputs/scan_results.json") as f:
        cve_json = json.load(f)

    # ?print(cve_json["geonetwork"]["matches"][2]['vulnerability']['id'])
    # with open("image_list.txt", "r") as f:
    #     images = f.read().split()

    # with open("./outputs/HR_scan_results.json") as data:
    #     print(JsonSlicer(data, ('geonetwork', None), path_mode='map_keys'))

    with open("./outputs/skopeo-data.json", "r") as f:
        skopeo_json = json.load(f)

    images = []

    # loop through images in skopeo_json
    for i in range(0, len(skopeo_json['images'])):
        image = {}
        image_name = skopeo_json['images'][i]['name']
        # only if the image is dependent on another image(s), cross-reference
        if len(skopeo_json['images'][i]['dependency']) > 0:
            # find parents and child, and store CVEs of both
            # store parent(s) data for each dependency
            dependencies = []
            for j in range(0, len(skopeo_json['images'][i]['dependency'])):
                dependency = {}
                dependency["name"] = skopeo_json['images'][i]['dependency'][j]
                # extract important data
                cves = []
                for k in range(0, len(cve_json[dependency["name"]]["matches"])):
                    cve = {}
                    cve["id"] = cve_json[dependency["name"]]["matches"][k]['vulnerability']['id']
                    cve["severity"] = cve_json[dependency["name"]]["matches"][k]['vulnerability']['severity']
                    cve["artifact"] = cve_json[dependency["name"]]["matches"][k]['artifact']['name']
                    cves.append(cve)
                dependency["cves"] = cves
                dependencies.append(dependency)

            # store child's cve data
            cves = []
            for k in range(0, len(cve_json[image_name]["matches"])):
                cve = {}
                cve["id"] = cve_json[image_name]["matches"][k]['vulnerability']['id']
                cve["severity"] = cve_json[image_name]["matches"][k]['vulnerability']['severity']
                cve["artifact"] = cve_json[image_name]["matches"][k]['artifact']['name']
                cves.append(cve)
            
            #! Cross reference here and output data
            image["cves"] = cves
            image["name"] = image_name
            image["dependencies"] = dependencies
            # image["patched"] =
            # image["unpatched"] =
            # image["new"] =
            images.append(image)

    print(json.dumps(images, indent=1))
    # print(len(images))

    #
    #
    # with open("./outputs/scan_results.json") as data:
    # for cve in JsonSlicer(data)
    # print(len(keys))
    # # print(dependencies.keys())
    # print(len(dependencies['images']))
if __name__ == "__main__":
    generateData()
