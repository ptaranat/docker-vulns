from _typeshed import SupportsItemAccess
import os

# loop to get proper input
# loops if:
    # docker not running
    # docker image doesn't exist
    # exit when successfull pull (regardless if already installed)
def pullImages():
        file = open("image_list.txt", "r")
        failed_file = open("failed_images.txt", "w")
        success_file = open("success_images", "w")

        
        images = file.read().split()
        for i in range(0,2):
            exit_code = os.system("docker pull " + images[i])
            if(exit_code != 0):
                failed_file.write("failed to pull image: " + images[i] + "\n")
            exit_code = os.system("docker rmi " + images[i] + "-f")
            if(exit_code != 0):
                failed_file.write("failed to remove image: " + images[i] + "\n")
            success_file.write("pulled and removed: " + images[i] + "\n")
        file.close()
        failed_file.close()
        success_file.close()

if __name__ == '__main__':
    pullImages()