#finds names of all the official docker images and outputs them to a file
import os


def printToFile(my_set):
    file = open("image_list.txt", "w")
    for val in my_set:
        file.write(val + "\n")
    file.close()

def generateList():
     # search through all combination of paris of a->z (duplicate searches do not affect results)
    # initialize new set
    my_set = {}
    my_set = set()
    for i in range(ord('a'), ord('z')+1):
        for j in range(ord('a'), ord('z')+1):
            # print("current search: " + chr(i) + chr(j))
            search_chars = chr(i) + chr(j)
            # command to search, read into "data"
            data = os.popen(
                "docker search --filter is-official=true --format \"{{.Name}}\" " + search_chars).read()
            data = data.split()
            # add new unique elements to set
            my_set.update(data)
            if len(my_set) >= 163:
                printToFile(my_set)
                return

if __name__ == '__main__':
    generateList()

