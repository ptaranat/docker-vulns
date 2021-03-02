#pulls from a a file with a list of all the official images, scans them,
#then dumps the CVE results corresponding to the image to a scan_results
import os
from termcolor import cprint
import json
from pprint import pprint

# loop to get proper input
# loops if:
    # docker not running
    # docker image doesn't exist
    # exit when successfull pull (regardless if already installed)
def pullImages():
        file = open("image_list.txt", "r")
        failed_file = open("failed_images.txt", "w")
        scan_results_file = open("scan_results.out", "w")
        HR_scan_results_file = open("HR_scan_results.out", "w")
        images = file.read().split()
        results = {}
        for i in range(0,81):
            #pull the image
            cprint("Pulling: " + images[i], 'grey', 'on_blue')
            exit_code = os.system("docker pull " + images[i])
            if(exit_code != 0):
                cprint("Failed to pull: " + images[i], 'grey', 'on_red')
                failed_file.write("failed to pull image: " + images[i] + "\n")
                failure = 1   
            
            #scan the image
            cprint("Scanning: " + images[i], 'grey', 'on_blue')
            data = os.popen(
                "grype " + images[i] +" -o json").read()
            results[images[i]] = json.loads(data)
            

            #remove the image
            cprint("Removing: " + images[i], 'grey', 'on_blue')
            exit_code = os.system("docker rmi " + images[i] + " -f")
            if(exit_code != 0):
                cprint("Failed to remove: " + images[i], 'grey', 'on_red')
                failed_file.write("failed to remove image: " + images[i] + "\n")
                failure = 1
            
            # check success
            # if(not failure):
            #     success_file.write("pulled and removed: " + images[i] + "\n")
            # failure = 0

        scan_results_file.write(json.dumps(results))
        HR_scan_results_file.write(json.dumps(results, indent=1))
        file.close()
        failed_file.close()
        success_file.close()
        scan_results_file.close()
        HR_scan_results_file.close()

if __name__ == '__main__':
    pullImages()