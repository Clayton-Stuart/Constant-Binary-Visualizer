from os import listdir
from os.path import isfile, exists, isdir
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

chars = ["░░░░", "████"]

opts = ['f', 'd']
conf = False
while not conf:
    opt = input("IF YOUR SOURCE IS A DIRECTORY ENTER \"D\" \n IF YOUR SOURCE IS A FILE ENTER \"F\": ").lower()
    conf = opt in opts 

if opt == 'f':
    conf = False
    while not conf:
        path = input("Enter source file path: ")
        conf = isfile(path) * exists(path)
    file = open(path, 'r')
    pre_ls = file.readlines()
    file.close()
    if len(pre_ls) > 1:
        print("File has new lines")
        input("Press enter to close...")
        exit()
    print("File loaded")

    opt = 'v'

    if opt == 'v':
        file_length = int(input("Enter amount of characters to wrap: "))
        pre_ls = pre_ls[0].strip()
        fin_ls = [pre_ls[y - file_length:y] for y in range(file_length, len(pre_ls) + file_length, file_length)]
        print("File parsed successfully")
        for i in range(len(fin_ls)):
            string = ''
            for e in range(len(fin_ls[i])):
                string += chars[int(fin_ls[i][e])]
            
            if i % 2 == 0:
                print(string)
                print(string, end='')
                input()
            else:
                print(string)
                print(string)

elif opt == 'd':
    conf = False
    while not conf:
        print("Files will be read in alphabetical and numerical order")
        print("All files will be interpreted regardless of name")
        directory = input("Enter input directory: ")
        conf = exists(directory) * isdir(directory)

    conf = False
    opts = ['s', 'v']
    while not conf:
        print("Enter \'s\' to search using a given image. Enter \'v\' to visualize your constant: ", end='')
        opt = input().lower()
        conf = opt in opts

    if opt == 'v':
        file_names = sorted_alphanumeric(listdir(directory))

        file = open(directory + "/" + file_names[0], 'r')
        ls = file.readlines()
        ls = ls[0].strip()
        file.close()
        del file
        file_length = int(input("Enter how many characters to wrap: "))

        for i in range(len(file_names)):
            lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
            del ls
            for e in range(len(lines) - 1):
                string = ''
                for j in range(len(lines[e])):
                    string += chars[int(lines[e][j])]
                if i % 2 == 0:
                    print(string)
                    print(string, end='')
                    input()
                else:
                    print(string)
                    print(string)
                if len(lines) - e == 30:
                    file = open(directory + '/' + file_names[i + 1], 'r')
                if len(lines) - e == 25:
                    ls = file.readlines()
                if len(lines) - e == 20:
                    ls = lines[-1] + ls[0].strip()
                    del file
    if opt == 's':
        conf = False
        while not conf:
            image = input("Enter image file to search for: ")
            conf = isfile(image) * exists(image)
        
        conf = False
        opts = ['y', 'n']
        while not conf:
            print('Separate image when found?')
            opt = input("Enter \'y\' for yes, enter \'n\' for no: ").lower()
            conf = opt in opts

        if opt == 'y':
            sep = True
        else:
            sep = False

        file = open(image, 'r')
        width = int(file.readline())
        height = int(file.readline())
        s_lines = []
        for _ in range(height):
            s_lines.append(file.readline().strip())

        if height > 90:
            print("Image height cannot be greater than 90")
            input("Press any key to close")
            exit()


        print("Image: ")
        for i in range(height):
            string = ''
            for e in range(len(s_lines[i])):
                string += chars[int(s_lines[i][e])]
            print(string)
            print(string)
        input('\nPress enter to continue...')

        file_names = sorted_alphanumeric(listdir(directory))
        file = open(directory + "/" + file_names[0], 'r')
        ls = file.readlines()
        ls = ls[0].strip()
        file.close()
        del file
        file_length = width
        for i in range(len(file_names) - 1):
            lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
            del ls
            for e in range(len(lines) - 1):
                if s_lines[0] == lines[e]:
                    valid = True
                    for j in range(height):
                        valid = valid * (s_lines[j] == lines[e + j])

                    if valid:
                        print("Found at line " + str(e) + " in file " + file_names[i] + '\n\n')
                        g = e - 2
                        for r in range(height + 4):
                            strs = ''
                            for s in range(width):
                                strs += chars[int(lines[g][s])]
                            g += 1
                            print(strs)
                            print(strs)
                            if r == 1 and sep:
                                print()
                            if r == height + 1 and sep:
                                print()
                        print()
                        print()

                        input('Press enter to continue... ')
                        print('\n\n\n\n')

                if len(lines) - e == 101:
                    print("Reading file " + str(i + 1) + "/" + str(len(file_names)))
                    print(file_names[i + 1])
                    file = open(directory + '/' + file_names[i + 1], 'r')
                    ls = file.readlines()
                    ls = lines[-1] + ls[0].strip()
                    del file
                    break
        
        lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
        del ls
        for e in range(len(lines) - 1):
            if s_lines[0] == lines[e]:
                valid = True
                for j in range(height):
                    valid = valid * (s_lines[j] == lines[e + j])

                if valid:
                    print("Found at line " + str(e) + " in file " + file_names[i] + '\n\n')
                    g = e - 2
                    for r in range(height + 4):
                        strs = ''
                        for s in range(width):
                            strs += chars[int(lines[g][s])]
                        g += 1
                        print(strs)
                        print(strs)
                        if r == 1 and sep:
                            print()
                        if r == height + 1 and sep:
                            print()
                    print()
                    print()

                    input('Press enter to continue... ')
                    print('\n\n\n\n')



   

