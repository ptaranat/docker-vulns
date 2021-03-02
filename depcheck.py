import os
import json


def findDep(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    image_list = content
    images = []
    cmd = "skopeo inspect docker://docker.io/library/"

    for item in image_list:
        image = {}
        # some images don't have latest tag (elasticsearch)
        with os.popen(cmd + item) as output:
            try:
                data = json.loads(output.read())
                image["name"] = item
                sha = data["Layers"][-1]
                image["sha256"] = sha
                image["layers"] = data["Layers"][:-1]
                image["dependency"] = []
                images.append(image)
            except:
                pass

    for base in images:
        for item in images:
            if base != item:
                if base["sha256"] in item["layers"]:
                    item_name = item["name"]
                    base_name = base["name"]
                    # print(f"{item_name} depends on {base_name}")
                    item["dependency"].append(base_name)
    
    jsondata = {}
    jsondata["images"] = []
    for item in images:
        jsondata["images"].append({
            "name": item["name"],
            "sha256": item["sha256"],
            "layers": item["layers"],
            "dependency": item["dependency"],
        })

    with open("skopeo-data.json", "w") as outfile:
        json.dump(jsondata, outfile)

    # # print images that have dependencies
    # for item in images:
    #     dep = item["dependency"]
    #     if dep:
    #         item_name = item["name"]
    #         print(f"{item_name} dependson {dep}")


if __name__ == "__main__":
    findDep("image_list.txt")