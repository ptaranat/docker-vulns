import os
import json
from jsonslicer import JsonSlicer



def crossCheck(data):
    found = 0
    #for each child image
    for child in range(0, len(data)):
        #for each CVE in child image
        for cve in range(0, len(data[child]['cves'])):
            curr_cve_id = data[child]["cves"][cve]["id"]
            data[child]["cves"][cve]["pun"] = "null"
            #check each dependency to look for cve
            for dependency in range(0,len(data[child]["dependencies"])):
                #check each cve in the curr dependency
                for i in range(0, len(data[child]["dependencies"][dependency]['cves'])):
                    parent_cve_id = data[child]["dependencies"][dependency]['cves'][i]['id']
                    if (parent_cve_id == curr_cve_id):
                        #we found it in parent and the child, mark in child as unpatched
                        data[child]["cves"][cve]["pun"] = "unpatched"
                        found = 1
                        break
                if(found):
                    break
            #we've gone through every dependency, comparing child to dependency
            if(not found):
                data[child]["cves"][cve]["pun"] = "new"
            else:
                found = 0

    found = 0
    for child in data:
        for dependency in child["dependencies"]:
            for cve in dependency['cves']:
                cve["pun"] = "null"
                curr_cve_id = cve["id"]
                for child_cve in child["cves"]:
                    if(child_cve["id"] == curr_cve_id):
                        found = 1
                        break
                if(not found):
                    cve["pun"] = "patched"
                else:
                    found = 0
    
    with open("./extracted_v3.json", "w") as f:
        f.write(json.dumps(data, indent=1))
            




    for child in range(0, len(data)):
        #for each CVE in child image
        for cve in range(0, len(data[child]['cves'])):
            curr_cve_id = data[child]["cves"][cve]["id"]
            data[child]["cves"][cve]["pun"] = "null"
            #check each dependency to look for cve
            for dependency in range(0,len(data[child]["dependencies"])):
                #check each cve in the curr dependency
                for i in range(0, len(data[child]["dependencies"][dependency]['cves'])):
                    parent_cve_id = data[child]["dependencies"][dependency]['cves'][i]['id']
                    if (parent_cve_id == curr_cve_id):
                        #we found it in parent and the child, mark in child as unpatched
                        data[child]["cves"][cve]["pun"] = "unpatched"
                        found = 1
                        break
                if(found):
                    break
            #we've gone through every dependency, comparing child to dependency
            if(not found):
                data[child]["cves"][cve]["pun"] = "new"
            else:
                found = 0
    
    
    with open("./extracted_v3.json", "w") as f:
        f.write(json.dumps(data, indent=1))
        






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
            image["name"] = image_name
            image["cves"] = cves
            image["dependencies"] = dependencies
            # image["patched"] =
            # image["unpatched"] =
            # image["new"] =
            images.append(image)
        
    crossCheck(images)

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
