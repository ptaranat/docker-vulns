import json
import os
from pprint import pprint
from termcolor import cprint


# with open("scan_result") as f:
#     data = json.load(f)
#     print(json.dumps(data, indent=1))

# HR_scan_results_file = open("HR_scan_results.out", "w")


# with open("scan_results.out") as f:
#     data = json.load(f)
#     HR_scan_results_file.write(json.dumps(data, indent=1))

with open("HR_scan_results.out.out") as f:
    data = json.load(f)
    # print(json.dumps(data, indent=1))
    print(json.dumps(data["archlinux"]))

# results = {}

# try:
#     data = os.popen(
#     "grype glassfish -o json").read()
#     results['hello'] = json.loads(data)
#     #remove the image
# except:
#     cprint("Exception on: glassfish", 'grey', 'on_red')
#     pass

# print(results)
