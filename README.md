# docker-vulns #

# EC700 Epoch 1

A vulnerability scanner for docker hub official images.

#### listimages.py
This file is used to "brute force" ```docker search```'s looking for docker hub official images, creating a list of all unique results output into **image_list.txt**. It does this by docker searching every combination of 2 characters (the minimum amount of characters required by docker for a search).

#### depcheck.py

This file takes in the image list retrieved previously and uses **skopeo** to inspect the manifest of all retrieved images, and parses the SHA Layer IDs. By using skopeo, pullin the image locally is not required, thereby speeding up the process of generating dependencies. To generate the dependencies, the layer ids of each image are cross referenced with the final layer of every other image, generating dependencies where there is a match. The results of which child images depend on which parent images are output in JSON format to **skopeo-data.json** and an easier to read **depcheck.txt**

#### pullAndScan.py
This file uses **image_list.txt** to automate a process of pulling each image one by one, scanning each one using **grype** after each pull, storing the results in a JSON, and then subsequently removing the image to save local space before moving on to the next image. In a giveen run, any exceptions cause an output to **failed_file.txt** and moves on. The results of all the scans for each image are stored in **scan_results.json**

#### CVEcrossCheck.py
This file has two functions. The first step is loading the **scan_results.json** and **skopeo-data.json** to extract the information we want and put them togeteher in a single data structure. This includes each image that contains a depdnency (as those are the only ones required for dependecy CVE cross checks in the next step) with its corresponding CVE (ID, artifcat ID, and severity) and an array of its dependent images, each also with a list of the same CVE data for that image. This data can be found in "extracted_data.json" but was further developed in *crossCeck()*. *Crosscheck()* takes this data structure and performs the CVE cross checking of child image to each parent image. For each CVE in each child image, we try to find the same CVE one of the dependencies/parent images to determine if it is Patched, Unpatched, or a New vulnerability (PUN). If the CVE is found in a dependent image, the CVE can be considered "unpatched", as it was introduced in the parent image and has propogated down to the child. If the CVE is found in the child image but not in the parent image, the CVE was introduced in the child and is considered "new". Lastly, the CVEs that are present in the dependent image and not in the child are considered patch. Dependencies that contain "null" refer to ones that have been marked in the child to simplify remarking CVEs. Output is in "extracted_v3.json"

#### parseCVE.py

This file is used to count the number of CVEs from the scan results JSON. It also counts the occurence of packages to find ones that have the most vulnerabilities reported. There are also functions to count and categorize CVEs by severity. Using that categorization, images can be grouped by their most severe vulnerability (e.g. an image with at least one Critical vulnerability is a critical image).

#### parsePUN.py

This function takes as input `extracted_v3.json` from CVEcrossCheck.py, which contains the inheritence pattern of the vulnerability (patched, unpatched, new). The function outputs a count of all patched, unpatched, and new vulnerabilities, and out of those vulnerabilities, the number that is high or critical severity.


