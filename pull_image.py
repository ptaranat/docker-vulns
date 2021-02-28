import os

# loop to get proper input
# loops if:
    # docker not running
    # docker image doesn't exist
    # exit when successfull pull (regardless if already installed)
exit_code = -1
while (exit_code != 0):
    image = input("Enter a docker image to comapare with: ")
    exit_code = os.system("docker pull " + image)

