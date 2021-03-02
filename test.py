import json

# with open("scan_result") as f:
#     data = json.load(f)
#     print(json.dumps(data, indent=1))

# HR_scan_results_file = open("HR_scan_results.out", "w")


# with open("scan_results.out") as f:
#     data = json.load(f)
#     HR_scan_results_file.write(json.dumps(data, indent=1))

with open("scan_results.out") as f:
    data = json.load(f)
    # print(json.dumps(data, indent=1))
    print(json.dumps(data["archlinux"]["matches"]))

