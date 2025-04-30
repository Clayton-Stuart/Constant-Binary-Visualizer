from os import remove, listdir
from os.path import isfile, join, exists, isdir
from re import split
import base64

def decimalToBinary(n):
    return "{0:b}".format(int(n))

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


opts = ['f', 'd']
conf = False
while not conf:
    opt = input("IF YOUR SOURCE IS A DIRECTORY ENTER \"D\" \n IF YOUR SOURCE IS A FILE ENTER \"F\": ").lower()
    if opt in opts:
        conf = True

if opt == 'f':
    conf = False
    while not conf:
        path = input("Enter the path to your source file: ")
        conf = exists(path) * isfile(path)

    conf = False
    while not conf:
        output = input("Enter output directory: ")
        if exists(output) and isdir(output):
            if len(listdir(output)) == 0:
                conf = True
            else:
                print("Directory not empty")
        else:
            print("Directory not found")

    file = open(path, 'r')
    print("Source file opened")
    ls = file.readlines()
    print("Raw source extracted from file")
    string = ""
    for i in range(len(ls)):
        string += str(ls[i])
    print("Created single string: ")
    string = string.replace(".", "")
    print("Sorted strings for decimal points")
    print("Checking if string is numeric")
    if string.isnumeric():
        print("String is numeric")
    else:
        print("String is not numeric")
        print("Press enter to close...", end="")
        input()
        exit()

    print("Writing to output file")
    file_length = 1000000
    files = [string[y - file_length:y] for y in range(file_length, len(string) + file_length, file_length)]
    for i in range(len(files)):
        print("Writing file " + str(i + 1) + "/" + str(len(files)))
        file = open(output + "/" + str(i) + "", 'bw')
        fin_string = ''
        for e in range(len(files[i])):
            fin_string += str(decimalToBinary(files[i][e]))
        file.write(base64.b64encode(bytes(fin_string, 'ascii')))
        file.close()
    print("All files written successfully to directory: \"" + output + "\"")
    input("Press enter to close")




elif opt == 'd':
    
    conf = False
    while not conf:
        print("Files will be read in alphabetical/numerical order. If there are any files that are not meant to be read, remove them from the directory. Any and all files will be interpreted")
        directory = input("Enter input directory (leave blank for current working directory): ")
        conf = isdir(directory)
    print("Confirmed Directory: %s" % directory)
    files = sorted_alphanumeric(listdir(directory))
    conf = False
    while not conf:
        output = input("Enter output directory: ")
        if exists(output) and isdir(output):
            if len(listdir(output)) == 0:
                conf = True
            else:
                print("Directory not empty")
        else:
            print("Directory not found")

    for i in range(len(files)):
        file = open(directory + '/' + files[i], 'r')
        ls = file.readlines()
        file.close()
        for e in range(len(ls)):
            ls[e] = ls[e].strip()
        string = ''
        for e in range(len(ls)):
            string += ls[e]
        string = string.replace(".", "")

        if not string.isnumeric():
            print("File " + str(i + 1) + " is not numeric. (" + files[i] + ")")

        file_length = 1000000
        output_files = [string[y - file_length:y] for y in range(file_length, len(string) + file_length, file_length)]

        print("Processing file " + str(i + 1) + '/' + str(len(files)))
        
        for e in range(len(output_files)):
            print("Writing file " + str(e + 1) + '/' + str(len(output_files)) + 'for file ' + str(i + 1) + '/' + str(len(files)))
            file = open(output + "/" + str(i) + ' - ' + str(e) + '', 'bw')
            fin_string = ''
            for u in range(len(output_files[e])):
                fin_string += str(decimalToBinary(output_files[e][u]))
            file.write(base64.b64encode(bytes(fin_string, 'ascii')))
            file.close()


        