from os import listdir, remove, system
from os.path import isfile, exists, isdir
import signal
import re

chars = ["░░░░░", "█████"]
run = False

def signal_handler(x, y):
    global run
    if run:
        z = input('User attempted to cancel operation. Enter \'y\' to confirm and \'n\' to cancel: ').lower()
        if z == 'y':
            run = False

signal.signal(signal.SIGINT, signal_handler)      

def get_int(prompt):
    while True:
        try:
            x = int(input(prompt))
        except:
            pass
        else:
            return x


def save_new(path, image):
    items = path.replace('\\', '/').split('/')
    directory = ''
    for i in range(len(items) - 1):
        directory += items[i]
        directory += '/'
    
    if isdir(directory):
        passed = False
        tracker = 0
        in1 = items[-1]
        while True:
            try:
                file = open(directory + items[-1], 'x')
            except:
                if items[-1].count('.') < 1:
                    print('Please provide a file extension')
                    return 0
                elif items[-1].count('.') > 1:
                    print('File name can only have one period')
                    return 0
                else:
                    items[-1] = in1.split('.')[0] + str(tracker) + '.' + in1.split('.')[1]
                    tracker += 1

            else:
                directory += items[-1]
                file.close()
                passed = True
                break

        if passed:
            file = open(directory, 'w')
            file.write(str(len(image[0])) + '\n')
            file.write(str(len(image)) + '\n')
            for i in range(len(image)):
                for e in range(len(image[i])):
                    file.write(str(image[i][e]))
                file.write('\n')
            file.close()
            return 1


def save_existing(path, image):
    file = open(path, 'w')
    file.write(str(len(image[0])) + '\n')
    file.write(str(len(image)) + '\n')
    for i in range(len(image)):
        for e in range(len(image[i])):
            file.write(str(image[i][e]))
        file.write('\n')
    file.close()


def clear():
    system('cls||clear')


def reverse_list(array):
    to_return = []
    for _ in range(len(array)):
        to_return.append(array.pop())
    return to_return


def print_image(array):
    for i in range(len(array)):
        string = ''
        for e in range(len(array[i])):
            string += chars[int(array[i][e])]
        print(string)
        print(string)


def print_image_numbered(array):
    string = '    '
    for i in range(len(array[0])):
        string += str(i) + '    '
    print(string)
        
    for i in range(len(array)):
        string = ''
        string += str(i) + ' '
        for e in range(len(array[i])):
            string += chars[int(array[i][e])]
        print(string)
        print(string)


def image_editor():
    running = True
    while running:
        clear()
        conf = False
        opts = ['0', '1', '2']
        print("""
    1: Create a new image 
    2: Open and edit existing image
    0: Close and return to settings menu
        """)
        while not conf:
            option = input('Option: ')
            conf = option in opts
        if option == '0':
            return 0
        
        elif option == '1':
            save = ''
            image = []
            print('Setup image (note that larger images are harder to find)')
            width = get_int('Enter the width of your image: ')
            height = get_int('Enter the height of your image: ')
            print('Creating pixel array...')
            for _ in range(height):
                image.append([])
            for i in range(len(image)):
                for _ in range(width):
                    image[i].append(0)


            while True: 
                clear()
                print_image_numbered(image)
                print()
                opts2 = ['help', 'pixel', 'size', 'quit', 'save']
                print('Enter command or enter help to see a list of commands')
                conf2 = False
                while not conf2:
                    option2 = input(': ')
                    option2 = option2.lower()
                    conf2 = option2 in opts2
                
                if option2 == 'help':
                    print("""
        \"help\": See this menu again
        \"pixel\": Enter pixel editing mode
        \"size\": Add or delete rows or columns
        \"quit\": Quit the image editor and return to main menu
        \"save\": Save the image to a file
        \"save as\": Save the image as a new file


                    """)
                    input('Press enter to continue...')

                elif option2 == 'pixel':
                    in_pixel = True
                    while in_pixel:
                        clear()
                        print_image_numbered(image)
                        print()
                        point = get_input_coordinates('Enter pixel coordinate to flip (x,y), or enter \'quit\' to exit to editor menu: ')
                        if point == 1:
                            in_pixel = False
                            valid_coord = False
                        elif point == 0:
                            valid_coord = False
                        else:
                            point = list(point)
                            point = reverse_list(point)
                            if point[1] >= len(image[0]) or point[1] >= len(image):
                                valid_coord = False
                            elif point[0] < 0 or point[1] < 0:
                                valid_coord = False
                            else:
                                valid_coord = True
                        
                        if valid_coord:
                            if image[point[0]][point[1]] == 0:
                                image[point[0]][point[1]] = 1
                            else:
                                image[point[0]][point[1]] = 0

                elif option2 == 'size':
                    inSize = True
                    while inSize:
                        clear()
                        print_image_numbered(image)
                        print()
                        print('Enter command or help')
                        option3 = input(': ').lower()
                        if option3 == 'help':
                            print("""
                            insert left: insert a column to the left of a given column
                            insert right: insert a column to the right of a given column
                            insert above: insert a row above a given row
                            insert below: insert a row below a given row

                            del col: delete a given column
                            del row: delete a given row

                            exit: return to the main editor menu

                            help: show this menu again 
                            """)
                            input("Press enter to continue...")
                        
                        elif option3 == 'exit' or option3 == 'quit':
                            inSize = False

                        elif option3 == 'insert left':
                            while True:
                                column = get_int('Enter column number: ')
                                if column >= 0 and column < len(image[0]):
                                    break
                            for i in range(len(image)):
                                image[i].insert(column, 1)
                        
                        elif option3 == 'insert right':
                            while True:
                                column = get_int('Enter column number: ')
                                if column >= 0 and column < len(image[0]):
                                    break
                            if column != len(image[0]) - 1:
                                for i in range(len(image)):
                                    image[i].insert(column + 1, 1)
                            else:
                                for i in range(len(image)):
                                    image[i].append(1)

                        elif option3 == 'insert above':
                            while True:
                                row = get_int('Enter row number: ')
                                if row >= 0 and row < len(image):
                                    break
                            ls = []
                            for i in range(len(image[0])):
                                ls.append(0)
                            image.insert(row, ls)
                        
                        elif option3 == 'insert below':
                            while True:
                                row = get_int('Enter row number: ')
                                if row >= 0 and row < len(image):
                                    break
                            ls = []
                            for i in range(len(image[0])):
                                ls.append(0)
                            image.insert(row + 1, ls)

                        elif option3 == 'del row':
                            if len(image) == 0:
                                print('Image is too small')
                            else:
                                while True:
                                    row = get_int('Enter row number (enter -1 to cancel): ')
                                    if (row >= 0 and row < len(image)) or row == -1:
                                        break
                                if row == -1:
                                    pass
                                else:
                                    del image[row]

                        elif option3 == 'del column':
                            if len(image[0]) == 0:
                                print('Image is too small')
                            else:
                                while True:
                                    row = get_int('Enter column number (enter -1 to cancel): ')
                                    if (row >= 0 and row < len(image[0])) or row == -1:
                                        break
                                if row == -1:
                                    pass
                                else:
                                    for i in image:
                                        del i[row]


                elif option2 == 'save':
                    if save == '':
                        print('Please specify path to save file')
                        while True:
                            path = input('Enter file path: ')
                            check = save_new(path, image)
                            if check == 1:
                                save = path
                                break
                    else:
                        save_existing(save, image)

                elif option2 == 'save as':
                    print('Please specify path to save file')
                    while True:
                        path = input('Enter file path: ')
                        check = save_new(path, image)
                        if check == 1:
                            save = path
                            break

                elif option2 == 'quit':
                    clear()
                    running = False
                    break


        elif option == '2':
            while True:
                path = input('Enter image path: ')
                if check_image_file(path)[1]:
                    save = path
                    break
            image = []
            file = open(path, 'r')
            lines = file.readlines()
            for _ in range(int(lines[1].strip())):
                image.append([])
            del lines[0]
            del lines[0]
            print(lines)
            for i in range(len(image)):
                for e in range(len(lines[i])):
                    if lines[i][e] == '\n':
                        pass
                    else:
                        image[i].append(int(lines[i][e].strip()))

            while True: 
                clear()
                print_image_numbered(image)
                print()
                opts2 = ['help', 'pixel', 'size', 'quit', 'save']
                print('Enter command or enter help to see a list of commands')
                conf2 = False
                while not conf2:
                    option2 = input(': ')
                    option2 = option2.lower()
                    conf2 = option2 in opts2
                
                if option2 == 'help':
                    print("""
        \"help\": See this menu again
        \"pixel\": Enter pixel editing mode
        \"size\": Add or delete rows or columns
        \"quit\": Quit the image editor and return to main menu
        \"save\": Save the image to a file
        \"save as\": Save the image as a new file


                    """)
                    input('Press enter to continue...')

                elif option2 == 'pixel':
                    in_pixel = True
                    while in_pixel:
                        clear()
                        print_image_numbered(image)
                        print()
                        point = get_input_coordinates('Enter pixel coordinate to flip (x,y), or enter \'quit\' to exit to editor menu: ')
                        if point == 1:
                            in_pixel = False
                            valid_coord = False
                        elif point == 0:
                            valid_coord = False
                        else:
                            point = list(point)
                            point = reverse_list(point)
                            if point[1] >= len(image[0]) or point[1] >= len(image):
                                valid_coord = False
                            elif point[0] < 0 or point[1] < 0:
                                valid_coord = False
                            else:
                                valid_coord = True
                        
                        if valid_coord:
                            if image[point[0]][point[1]] == 0:
                                image[point[0]][point[1]] = 1
                            else:
                                image[point[0]][point[1]] = 0

                
                elif option2 == 'size':
                    inSize = True
                    while inSize:
                        clear()
                        print_image_numbered(image)
                        print()
                        print('Enter command or help')
                        option3 = input(': ').lower()
                        if option3 == 'help':
                            print("""
                            insert left: insert a column to the left of a given column
                            insert right: insert a column to the right of a given column
                            insert above: insert a row above a given row
                            insert below: insert a row below a given row

                            del col: delete a given column
                            del row: delete a given row

                            exit: return to the main editor menu

                            help: show this menu again 
                            """)
                            input("Press enter to continue...")
                        
                        elif option3 == 'exit' or option3 == 'quit':
                            inSize = False

                        elif option3 == 'insert left':
                            while True:
                                column = get_int('Enter column number: ')
                                if column >= 0 and column < len(image[0]):
                                    break
                            for i in range(len(image)):
                                image[i].insert(column, 1)
                        
                        elif option3 == 'insert right':
                            while True:
                                column = get_int('Enter column number: ')
                                if column >= 0 and column < len(image[0]):
                                    break
                            if column != len(image[0]) - 1:
                                for i in range(len(image)):
                                    image[i].insert(column + 1, 1)
                            else:
                                for i in range(len(image)):
                                    image[i].append(1)

                        elif option3 == 'insert above':
                            while True:
                                row = get_int('Enter row number: ')
                                if row >= 0 and row < len(image):
                                    break
                            ls = []
                            for i in range(len(image[0])):
                                ls.append(0)
                            image.insert(row, ls)
                        
                        elif option3 == 'insert below':
                            while True:
                                row = get_int('Enter row number: ')
                                if row >= 0 and row < len(image):
                                    break
                            ls = []
                            for i in range(len(image[0])):
                                ls.append(0)
                            image.insert(row + 1, ls)

                        elif option3 == 'del row':
                            if len(image) == 0:
                                print('Image is too small')
                            else:
                                while True:
                                    row = get_int('Enter row number (enter -1 to cancel): ')
                                    if (row >= 0 and row < len(image)) or row == -1:
                                        break
                                if row == -1:
                                    pass
                                else:
                                    del image[row]

                        elif option3 == 'del column':
                            if len(image[0]) == 0:
                                print('Image is too small')
                            else:
                                while True:
                                    row = get_int('Enter column number (enter -1 to cancel): ')
                                    if (row >= 0 and row < len(image[0])) or row == -1:
                                        break
                                if row == -1:
                                    pass
                                else:
                                    for i in image:
                                        del i[row]

                


                elif option2 == 'save':
                    if save == '':
                        print('Please specify path to save file')
                        while True:
                            path = input('Enter file path: ')
                            check = save_new(path, image)
                            if check == 1:
                                save = path
                                break
                    else:
                        save_existing(save, image)

                elif option2 == 'save as':
                    print('Please specify path to save file')
                    while True:
                        path = input('Enter file path: ')
                        check = save_new(path, image)
                        if check == 1:
                            save = path
                            break

                elif option2 == 'quit':
                    clear()
                    running = False
                    break





def get_input_coordinates(prompt):
    string = input(prompt)
    if string.lower() == 'quit':
        return 1
    to_del = []
    string = list(string)
    allowed = ['1', '2', '3', '4' ,'5', '6' ,'7' ,'8', '9', '0', ',']
    for i in range(len(string)):
        if string[i] not in allowed:
            to_del.append(i)
    to_del = reverse_list(to_del)
    for i in to_del:
        string.pop(i)
    midf_str = ''
    for i in string:
        midf_str += i
    
    sides = midf_str.split(',')
    if len(sides) != 2:
        return 0
    elif sides[0] == '' or sides[1] == '':
        return 0
    else:
        return (int(sides[0]), int(sides[1]))


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


def print_space():
    print('\n\n\n')
    print('================================================================')
    print('\n\n\n')


def print_settings(settings):
    if settings[0] == 'd':
        print('1: Source type (directory)')
    elif settings[0] == 'f':
        print('1: Source type (file)')
    if settings[1] == '':
        print('        No source specified')
    else:
        if settings[0] == 'f' and isfile(settings[1]) and exists(settings[1]):
            print('        ' + settings[1])
        elif settings[0] == 'd' and isdir(settings[1]) and exists(settings[1]):
            print('        ' + settings[1])
        else:
            print('        Invalid source')

    print()
    print('2: Change and configure visualizer operation')
    if settings[2] == 's':
        print('        Searching for an image')
    elif settings[2] == 'v':
        print('        Visualizing binary images')
    elif settings[2] == 'f': 
        print('        Searching for a given line')
    elif settings[2] == 'd':
        print('        Display an image file')
    print()
    print('3: Define and configure output')
    if settings[8] == 'd':
        print('        Display output only')
    elif settings[8] == 'f':
        print('        Send output to file only')
    elif settings[8] == 'b':
        print('        Output both to display and file')
    print()
    print('0: Start operation')
    print();print()


def opt1(settings):
    while True:
        print('1: Change source type')
        if settings[0] == 'd':
            print('        Directory')
        else:
            print('        File')
        print()
        print('2: Change source file or directory')
        if settings[1] == '':
            print('        No source selected')
        elif settings[0] == 'f' and isfile(settings[1]) and exists(settings[1]):
                print('        ' + settings[1])
        elif settings[0] == 'd' and exists(settings[1]) and isdir(settings[1]):
            print('        ' + settings[1])
        else:
            print('        Invalid source')
        print()
        print('0: Done')

        print();print();

        conf = False
        opts = ['1', '2', '0']
        while not conf:
            option = input('option: ').lower()
            if option in opts:
                if option == '0':
                    print_space()
                    return settings

                elif option == '1':
                    print_space()
                    if settings[0] == 'd':
                        settings[0] = 'f'
                    else:
                        settings[0] = 'd'
                    conf = True

                elif option == '2':
                    print_space()
                    while True:
                        if settings[0] == 'd':
                            path = input('Enter input directory or enter 0 to cancel: ')
                            conf2 = exists(path) * isdir(path)
                            if path == '0':
                                conf = True
                                print_space()
                                break
                            if not conf2:
                                print('Invalid path')
                                conf = True
                            else:
                                settings[1] = path
                                conf = True
                                print_space()
                                break

                        if settings[0] == 'f':
                            path = input('Enter input file path or enter 0 to cancel: ')
                            conf2 = exists(path) *isfile(path)
                            if path == '0':
                                conf = True
                                break
                            if not conf2:
                                print('Invalid path')
                                conf = True
                            else:
                                settings[1] = path
                                conf = True
                                break

                            
def opt2(settings):
    while True:
        print('1: Select operation')
        print()
        print('2: Configure operation')
        print()
        print('0: Done')
        print(); print()

        conf = False
        opts = ['1', '2', '0']
        while not conf:
            option = input('option: ').lower()
            if option in opts:
                if option == '0':
                    print_space()
                    return settings
                
                if option == '1':
                    print_space()
                    print('1: Search for an image')
                    print('2: Visualize the binaries')
                    print('3: Search for a given line')
                    print('4: Display an image file')
                    opts2 = ['1', '2', '3', '4']
                    print();print()
                    conf2 = False
                    while not conf2:
                        option2 = input('option: ').lower()
                        conf2 = option2 in opts2
                        if option2 == '1':
                            settings[2] = 's'
                            conf = True
                            print_space()
                        elif option2 == '2':
                            settings[2] = 'v'
                            conf = True
                            print_space()
                        elif option2 == '3':
                            settings[2] = 'f'
                            conf = True
                            print_space()
                        elif option2 == '4':
                            settings[2] = 'd'
                            conf = True
                            print_space()

                elif option == '2':
                    if settings[2] == 's':
                        conf2 = False
                        while not conf2:
                            print_space()
                            if settings[3] == 'n':
                                print('1: Separate image when found (off)')
                            elif settings[3] == 'y':
                                print('1: Separate image when found (on)')
                            print()
                            if settings[4] == '':
                                print('2: Set image file path')
                                print('        No image file selected')
                            else:
                                print('2: Set image file path')
                                print('        ' + settings[4])
                            print('0: Done')
                            print();print()

                            conf3 = False
                            opts3 = ['0', '1', '2']
                            while not conf3:
                                option3 = input('option: ')
                                conf3 = option3 in opts3

                            if option3 == '0':
                                print_space()
                                return settings

                            elif option3 == '1':
                                if settings[3] == 'y':
                                    settings[3] = 'n'
                                elif settings[3] == 'n':
                                    settings[3] = 'y'

                            elif option == '2':
                                print_space()
                                while True:
                                    valid = False
                                    path = input('Enter path or enter \'0\' to cancel: ')
                                    if path == '0':
                                        break
                                    else:
                                        valid = exists(path) * isfile(path)
                                    if valid:
                                        break
                                if valid:
                                    settings[4] = path

                    elif settings[2] == 'v':
                        conf2 = False
                        while not conf2:
                            print_space()
                            print('1: Change how many characters to wrap: ')
                            print('        Currently: ' + str(settings[5]))
                            print()
                            print('0: Done')
                            print();print()

                            conf3 = False
                            opts3 = ['0', '1']
                            while not conf3:
                                option2 = input('option: ')
                                conf3 = option2 in opts3
                            if option2 == '0':
                                conf = True
                                print_space()
                                break
                            elif option2 == '1':
                                print_space()
                                while True:
                                    try: 
                                        x = int(input('Enter characters to wrap: '))
                                    except ValueError:
                                        pass
                                    else:
                                        break
                                settings[5] = x
                                print_space()

                    elif settings[2] == 'f':
                        conf2 = False
                        while not conf2:
                            print_space()
                            if settings[0] == 'f':
                                print('1: Enter line to find')
                            else:
                                print('1: Enter file and line to find')
                            
                            if settings[0] == 'f':
                                print('        Line ' + str(settings[6]))
                            elif settings[0] == 'd':
                                print('        Line ' + str(settings[6]) + '; File ' + str(settings[7]))

                            print()
                            print('2: Change how many characters to wrap: ')
                            print('        Currently: ' + str(settings[5]))
                            print()
                            print('0: Done')
                            print();print()

                            conf3 = False
                            opts3 = ['0', '1', '2']
                            while not conf3:
                                option2 = input('option: ').lower()
                                conf3 = option2 in opts3
                            if option2 == '0':
                                print_space()
                                conf2 = True
                                conf = True
                            elif option2 == '1':
                                print_space()
                                if settings[0] == 'f':
                                    while True:
                                        try: 
                                            x = int(input('Enter line: '))
                                        except ValueError:
                                            pass
                                        else:
                                            if x > 0:
                                                break
                                    settings[6] = x
                                else:
                                    while True:
                                        try: 
                                            x = int(input('Enter line: '))
                                        except ValueError:
                                            pass
                                        else:
                                            if x > 0:
                                                break
                                    settings[6] = x

                                    while True:
                                        try: 
                                            x = int(input('Enter file number as returned: '))
                                        except ValueError:
                                            pass
                                        else:
                                            if x > 0:
                                                break
                                    settings[7] = x
                            
                            elif option2 == '2':
                                print_space()
                                while True:
                                    try: 
                                        x = int(input('Enter characters to wrap'))
                                    except ValueError:
                                        pass
                                    else:
                                        break
                                settings[5] = x

                    elif settings[2] == 'd':
                        conf2 = False
                        while not conf2:
                            print_space()
                            if settings[4] == '':
                                print('1: Set image file path')
                                print('        No image file selected')
                            else:
                                print('1: Set image file path')
                                print('        ' + settings[4])
                            print('0: Done')
                            print();print()

                            conf3 = False
                            opts3 = ['0', '1']
                            while not conf3:
                                option3 = input('option: ')
                                conf3 = option3 in opts3
                            if option3 == '0':
                                print_space()
                                conf = True
                                conf2 = True

                            elif option3 == '1':
                                print_space()
                                while True:
                                    valid = False
                                    path = input('Enter path or enter \'0\' to cancel: ')
                                    if path == '0':
                                        break
                                    else:
                                        valid = exists(path) * isfile(path)
                                    if valid:
                                        break
                                if valid:
                                    settings[4] = path


def opt3(settings):
    while True:
        print('1: Change output type')
        if settings[8] == 'd':
            print('        Display output only')
        elif settings[8] == 'f':
            print('        Send output to file only')
        elif settings[8] == 'b':
            print('        Output both to display and file')
        print()
        if settings[8] != 'd':
            print('2: Set output path')
            print()
        print('0: Done')
        conf = False
        opt = ['0', '1']
        if settings[8] != 'd':
            opt.append('2')
        while not conf:
            option = input('option: ').lower()
            conf = option in opt
        if option == '0':
            print_space()
            return settings

        if option == '1':
            print_space()
            print('1: Output to display only')
            print('2: Output to file only')
            print('3: Output to both file and display')
            print()
            conf2 = False
            opts2 = ['1', '2', '3']
            while not conf2:
                option2 = input('option: ').lower()
                conf2 = option2 in opts2
            if option2 == '1':
                settings[8] = 'd'
            elif option2 == '2':
                settings[8] = 'f'
            elif option2 == '3':
                settings[8] = 'b'
            print_space()

        elif option == '2':
            print_space()
            disallowed = ['/', '\\', ':', '*', '?', '\"', '<', '>', '|']
            forbidden_names = ['con', 'aux', 'prn', 'nul', 'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9', 'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9']
            conf3 = False
            passed = True
            while not conf3:
                path = input('Enter file path or enter \'0\' to cancel: ')
                if path == '0':
                    break
                print(path)
                conf4 = False
                while not conf4:
                    confirm = input('Is this correct? (y/n): ').lower()
                    if confirm == 'y':
                        conf4 = True


                        if exists(path) and isfile(path):
                            print('File already exists')
                        elif isdir(path):
                            try:
                                if exists(path + "93ijh 8cqj30c-c3_3jc9j43qjcj39q"):
                                    redundancy = True
                                file_test = open(path + '93ijh 8cqj30c-c3_3jc9j43qjcj39q', 'a')
                                file_test.close()
                            except:
                                print('Directory is invalid')
                            else:
                                if not redundancy:
                                    remove(path + '93ijh 8cqj30c-c3_3jc9j43qjcj39q')
                                conf3 = True
                        else:
                            try:
                                file_test = open(path, 'a')
                                file_test.close()
                            except:
                                print('Path is invalid')
                            else:
                                remove(path)
                                conf3 = True


                    elif confirm == 'n':
                        conf4 = True
                
                settings[9] = path

            print_space()


def check_image_file(path):
    if not exists(path):
        return ('Invalid image file path - File does not exist', False)

    if not isfile(path):
        return ('Invalid image file path - Path is not a file', False)

    file = open(path, 'r')
    ls = file.readlines()
    file.close()
    try:
        y = int(ls[0])
    except (ValueError, IndexError):
        return ('Invalid image file - Invalid width', False)
    try:
        x = int(ls[1])
    except (ValueError, IndexError):
        return ('Invalid image file - Invalid height', False)
    
    del ls[0]
    del ls[0]

    if ls[-1] == '\n':
        del ls[-1]

    if len(ls) != x:
        return ('Invalid image file - Height of image does not match given lines', False)

    for i in range(len(ls)):
        if len(ls[i].strip()) != y:
            return ('Invalid image file - Line ' + str(i) + ' does not match given width', False)

    return('', True)


def begin(settings):
    options = ['0', '1', '2', '3', '9']
    while True:
        print_settings(settings)
        print()
        print()
        print('9: Create and edit image files')

        conf = False
        while not conf:
            option = input('option: ')
            conf = option in options

        if option == '1':
            print_space()
            settings = opt1(settings)
        
        elif option == '2':
            print_space()
            settings = opt2(settings)

        elif option == '3':
            print_space()
            settings = opt3(settings)

        elif option == '9':
            image_editor()

        elif option == '0':
            valid = True
            issues = []
            if settings[0] == 'd' and settings[2] != 'd':
                if isdir(settings[1]) and exists(settings[1]):
                    valid = valid * True
                else:
                    issues.append('Invalid directory path')
            if settings[0] == 'f' and settings[2] != 'd':
                if isfile(settings[1]) and exists(settings[1]):
                    valid = valid * True
                else:
                    issues.append('Invalid file path')

            if settings[2] == 's':
                confirm = check_image_file(settings[4])
                valid = valid * confirm[1]
                if not confirm[1]:
                    issues.append(confirm[0])

            if settings[8] == 'f' or settings[8] == 'b':
                if settings[9] != '':
                    pass
                else:
                    issues.append('Invalid output path')
            
            if settings[2] == 'd':
                confirm = check_image_file(settings[4])
                valid = valid * confirm[1]
                if not confirm[1]:
                    issues.append(confirm[0])

            if valid:
                return settings

            else:
                print_space()
                print("Current issues: ")
                for i in issues:
                    print('        ' + i)
                input("Press enter to continue...")
                print_space()


def visualize_display(path, itype, width):
    if itype == 'f':
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
            file_length = width
            pre_ls = pre_ls[0].strip()
            fin_ls = [pre_ls[y - file_length:y] for y in range(file_length, len(pre_ls) + file_length, file_length)]
            print("File parsed successfully")
            for i in range(len(fin_ls)):
                string = ''
                for e in range(len(fin_ls[i])):
                    string += chars[int(fin_ls[i][e])]
                
                if i % 3 == 0:
                    print(string)
                    print(string, end='')
                    input()
                else:
                    print(string)
                    print(string)

    if itype == 'd':
        conf = False
        opt = 'v'
        if opt == 'v':
            file_names = sorted_alphanumeric(listdir(path))

            file = open(path + "/" + file_names[0], 'r')
            ls = file.readlines()
            ls = ls[0].strip()
            file.close()
            del file
            file_length = width

            for i in range(len(file_names)):
                lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
                del ls
                for e in range(len(lines) - 61):
                    string = ''
                    for j in range(len(lines[e])):
                        string += chars[int(lines[e][j])]
                    if e % 3 == 0:
                        print(string)
                        print(string, end='')
                        input()
                    else:
                        print(string)
                        print(string)
                    
                    file = open(path + '/' + file_names[i + 1], 'r')
                    ls = file.readlines()
                    ls = lines[-1] + ls[0].strip()
                    del file


def visualize_file(path, itype, width, output):
    if itype == 'f':
        file = open(path, 'r')
        pre_ls = file.readlines()
        file.close()
        if len(pre_ls) > 1:
            print("File has new lines")
            input("Press enter to close...")
            exit()
        print("File loaded")
        if isdir(output):
            output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
        else:
            output_file = open(output, 'a', encoding="utf-8")
        opt = 'v'

        if opt == 'v':
            file_length = width
            pre_ls = pre_ls[0].strip()
            fin_ls = [pre_ls[y - file_length:y] for y in range(file_length, len(pre_ls) + file_length, file_length)]
            print("File parsed successfully")
            for i in range(len(fin_ls)):
                string = ''
                for e in range(len(fin_ls[i])):
                    string += chars[int(fin_ls[i][e])]
                
                if i % 3 == 0:
                    output_file.write(string + "\n")
                    output_file.write(string + "\n")
                else:
                    output_file.write(string + "\n")
                    output_file.write(string + "\n")

        output_file.close()

    if itype == 'd':  
        file_names = sorted_alphanumeric(listdir(path))
        for i in range(len(file_names)):
            file = open(path + '/' + file_names[i], 'r')
            pre_ls = file.readlines()
            file.close()
            if isdir(output):
                output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
            else:
                output_file = open(output, 'a', encoding="utf-8")
            opt = 'v'

            if opt == 'v':
                file_length = width
                pre_ls = pre_ls[0].strip()
                fin_ls = [pre_ls[y - file_length:y] for y in range(file_length, len(pre_ls) + file_length, file_length)]
                for j in range(len(fin_ls)):
                    string = ''
                    for e in range(len(fin_ls[j])):
                        string += chars[int(fin_ls[j][e])]
                    
                    if j % 3 == 0:
                        output_file.write(string + "\n")
                        output_file.write(string + "\n")
                    else:
                        output_file.write(string + "\n")
                        output_file.write(string + "\n")

            output_file.close()
            print('Processed file ' + str(i + 1) + '/' + str(len(file_names)))


def visualize_both(path, itype, width, output):
    if itype == 'f':
        file = open(path, 'r')
        pre_ls = file.readlines()
        file.close()
        if len(pre_ls) > 1:
            print("File has new lines")
            input("Press enter to close...")
            exit()
        print("File loaded")
        if isdir(output):
            output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
        else:
            output_file = open(output, 'a', encoding="utf-8")
        opt = 'v'

        if opt == 'v':
            file_length = width
            pre_ls = pre_ls[0].strip()
            fin_ls = [pre_ls[y - file_length:y] for y in range(file_length, len(pre_ls) + file_length, file_length)]
            print("File parsed successfully")
            for i in range(len(fin_ls)):
                string = ''
                for e in range(len(fin_ls[i])):
                    string += chars[int(fin_ls[i][e])]
                
                if i % 3 == 0:
                    output_file.write(string + "\n")
                    output_file.write(string + "\n")
                    print(string)
                    print(string, end='')
                    input()

                else:
                    output_file.write(string + "\n")
                    output_file.write(string + "\n")
                    print(string)
                    print(string)

        output_file.close()

    if itype == 'd':  
        file_names = sorted_alphanumeric(listdir(path))
        for i in range(len(file_names)):
            file = open(path + '/' + file_names[i], 'r')
            pre_ls = file.readlines()
            file.close()
            if isdir(output):
                output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
            else:
                output_file = open(output, 'a', encoding="utf-8")
            opt = 'v'

            if opt == 'v':
                file_length = width
                pre_ls = pre_ls[0].strip()
                fin_ls = [pre_ls[y - file_length:y] for y in range(file_length, len(pre_ls) + file_length, file_length)]
                for j in range(len(fin_ls)):
                    string = ''
                    for e in range(len(fin_ls[j])):
                        string += chars[int(fin_ls[j][e])]
                    
                    if j % 3 == 0:
                        output_file.write(string + "\n")
                        output_file.write(string + "\n")
                        print(string)
                        print(string, end='')
                        input()
                    else:
                        output_file.write(string + "\n")
                        output_file.write(string + "\n")
                        print(string)
                        print(string)

            output_file.close()
            print('Processed file ' + str(i + 1) + '/' + str(len(file_names)))


def search_display(path, itype, image, opt):
    if itype == 'f':
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
        print("Image: ")
        for i in range(height):
            string = ''
            for e in range(len(s_lines[i])):
                string += chars[int(s_lines[i][e])]
            print(string)
            print(string)
        input('\nPress enter to continue...')

        file = open(path, 'r')
        ls = file.readlines()
        ls = ls[0].strip()
        file.close()
        del file
        file_length = width

        lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
        del ls
        for e in range(len(lines) - 35):
            if s_lines[0] == lines[e]:
                valid = True
                for j in range(height):
                    valid = valid * (s_lines[j] == lines[e + j])

                if valid:
                    print("Found at line " + str(e))
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


        
        

    # ===========================================================================
    if itype == 'd':
        directory = path
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
            for e in range(len(lines) - 35):
                if s_lines[0] == lines[e]:
                    valid = True
                    for j in range(height):
                        valid = valid * (s_lines[j] == lines[e + j])

                    if valid:
                        print("Found at line " + str(e) + " in file " + file_names[i] + '\n' + 'file index ' + str(i) + '\n\n')

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

                
            print("Reading file " + str(i + 1) + "/" + str(len(file_names)))
            print(file_names[i + 1])
            file = open(directory + '/' + file_names[i + 1], 'r')
            ls = file.readlines()
            ls = lines[-1] + ls[0].strip()


def search_file(path, itype, image, opt, output):
    
    if itype == 'f':
        if isdir(output):
            output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
        else:
            output_file = open(output, 'a', encoding="utf-8")
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
        print("Image: ")
        for i in range(height):
            string = ''
            for e in range(len(s_lines[i])):
                string += chars[int(s_lines[i][e])]
            print(string)
            print(string)
        input('\nPress enter to continue...')

        file = open(path, 'r')
        ls = file.readlines()
        ls = ls[0].strip()
        file.close()
        del file
        file_length = width

        lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
        del ls
        for e in range(len(lines) - 35):
            if isdir(output):
                output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
            else:
                output_file = open(output, 'a', encoding="utf-8")
            if s_lines[0] == lines[e]:
                valid = True
                for j in range(height):
                    valid = valid * (s_lines[j] == lines[e + j])

                if valid:
                    output_file.write("Found at line " + str(e))
                    g = e - 2
                    for r in range(height + 4):
                        strs = ''
                        for s in range(width):
                            strs += chars[int(lines[g][s])]
                        g += 1
                        output_file.write(strs)
                        output_file.write('\n')
                        output_file.write(strs)
                        output_file.write('\n')
                        if r == 1 and sep:
                            output_file.write('\n')
                        if r == height + 1 and sep:
                            output_file.write('\n')
                        output_file.write('\n')
                        output_file.write('\n')
        output_file.close()


        
        

    # ===========================================================================
    if itype == 'd':
        
        directory = path
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
            if isdir(output):
                output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
            else:
                output_file = open(output, 'a', encoding="utf-8")
            lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
            del ls
            for e in range(len(lines) - 35):
                if s_lines[0] == lines[e]:
                    valid = True
                    for j in range(height):
                        valid = valid * (s_lines[j] == lines[e + j])

                    if valid:
                        output_file.write("Found at line " + str(e) + " in file " + file_names[i] + '\n' + 'file index ' + str(i) + '\n\n')
                        g = e - 2
                        for r in range(height + 4):
                            strs = ''
                            for s in range(width):
                                strs += chars[int(lines[g][s])]
                            g += 1
                            output_file.write(strs)
                            output_file.write('\n')
                            output_file.write(strs)
                            output_file.write('\n')

                            if r == 1 and sep:
                                output_file.write('\n')
                            if r == height + 1 and sep:
                                output_file.write('\n')
                        output_file.write('\n')
                        output_file.write('\n')

            output_file.close()

            
                                

                   

                
            print("Reading file " + str(i + 1) + "/" + str(len(file_names)))
            print(file_names[i + 1])
            file = open(directory + '/' + file_names[i + 1], 'r')
            ls = file.readlines()
            ls = lines[-1] + ls[0].strip()


def search_both(path, itype, image, opt, output):
    
    if itype == 'f':
        
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
        print("Image: ")
        for i in range(height):
            string = ''
            for e in range(len(s_lines[i])):
                string += chars[int(s_lines[i][e])]
            print(string)
            print(string)
        input('\nPress enter to continue...')

        file = open(path, 'r')
        ls = file.readlines()
        ls = ls[0].strip()
        file.close()
        del file
        file_length = width

        lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
        del ls
        for e in range(len(lines) - 35):
            if s_lines[0] == lines[e]:
                valid = True
                for j in range(height):
                    valid = valid * (s_lines[j] == lines[e + j])

                if valid:
                    if isdir(output):
                        output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
                    else:
                        output_file = open(output, 'a', encoding="utf-8")
                    output_file.write("Found at line " + str(e))
                    print("Found at line " + str(e))
                    g = e - 2
                    for r in range(height + 4):
                        strs = ''
                        for s in range(width):
                            strs += chars[int(lines[g][s])]
                        g += 1
                        print(strs)
                        print(strs)
                        output_file.write(strs)
                        output_file.write('\n')
                        output_file.write(strs)
                        output_file.write('\n')
                        if r == 1 and sep:
                            output_file.write('\n')
                        if r == height + 1 and sep:
                            output_file.write('\n')
                            print()
                        output_file.write('\n')
                        output_file.write('\n')
                        print()
                        print()
                        input('Press enter to continue... ')
                        print('\n\n\n\n')
                    output_file.close()


        
        

    # ===========================================================================
    if itype == 'd':
        
        directory = path
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
            for e in range(len(lines) - 35):
                if s_lines[0] == lines[e]:
                    valid = True
                    for j in range(height):
                        valid = valid * (s_lines[j] == lines[e + j])

                    if valid:
                        if isdir(output):
                            output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
                        else:
                            output_file = open(output, 'a', encoding="utf-8")
                        output_file.write("Found at line " + str(e) + " in file " + file_names[i] + '\n' + 'file index ' + str(i) + '\n\n')
                        print("Found at line " + str(e) + " in file " + file_names[i] + '\n' + 'file index ' + str(i) + '\n\n')
                        g = e - 2
                        for r in range(height + 4):
                            strs = ''
                            for s in range(width):
                                strs += chars[int(lines[g][s])]
                            g += 1
                            print(strs)
                            print(strs)
                            output_file.write(strs)
                            output_file.write('\n')
                            output_file.write(strs)
                            output_file.write('\n')

                            if r == 1 and sep:
                                print()
                                output_file.write('\n')
                            if r == height + 1 and sep:
                                output_file.write('\n')
                                print()
                        output_file.write('\n')
                        output_file.write('\n')
                        print()
                        print()
                        input('Press enter to continue...')
                        print('\n\n\n\n')

                        output_file.close()

            
                                

                   

                
            print("Reading file " + str(i + 1) + "/" + str(len(file_names)))
            print(file_names[i + 1])
            file = open(directory + '/' + file_names[i + 1], 'r')
            ls = file.readlines()
            ls = lines[-1] + ls[0].strip()


def locate_display(path, itype, width, line, file = 0):
    if itype == 'f':
        input_file = open(path, 'r')
        ls = input_file.readlines()
        ls = ls[0].strip()
        file_length = width
        input_file.close()
        lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
        print(len(lines))
        for i in range(line - 3, len(lines)):
            string = ''
            for e in range(len(lines[i])):
                string += chars[int(lines[i][e])]
            if i % 1 == 0:
                print(string + "        Line: " + str(i))
                print(string, end='')
                input()
            else:
                print(string + "        Line: " + str(i))
                print(string)
        
    if itype == 'd':
        file_names = sorted_alphanumeric(listdir(path))
        for i in range(file):
            del file_names[0]

        for j in range(len(file_names)):
            input_file = open(path + '/' + file_names[j], 'r')
            ls = input_file.readlines()
            ls = ls[0].strip()
            file_length = width
            input_file.close()
            lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
            print(len(lines))
            for i in range(line - 3, len(lines)):
                string = ''
                for e in range(len(lines[i])):
                    string += chars[int(lines[i][e])]
                if i % 1 == 0:
                    print(string + "        Line: " + str(i) + ', File: ' + file_names[j])
                    print(string, end='')
                    input()
                else:
                    print(string + "        Line: " + str(i) + ', File: ' + file_names[j])
                    print(string)


def locate_file(path, itype, width, line, output, file = 0):
    if isdir(output):
        output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
    else:
        output_file = open(output, 'a', encoding="utf-8")
    if itype == 'f':
        input_file = open(path, 'r')
        ls = input_file.readlines()
        ls = ls[0].strip()
        file_length = width
        input_file.close()
        lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
        for i in range(line - 3, len(lines)):
            string = ''
            for e in range(len(lines[i])):
                string += chars[int(lines[i][e])]
            if i % 1 == 0:
                output_file.write(string + "        Line: " + str(i) + '\n')
                output_file.write(string + '\n')
            else:
                output_file.write(string + "        Line: " + str(i) + '\n')
                output_file.write(string + '\n')

    if itype == 'd':
        file_names = sorted_alphanumeric(listdir(path))
        for i in range(file):
            del file_names[0]

        for j in range(len(file_names)):
            input_file = open(path + '/' + file_names[j], 'r')
            ls = input_file.readlines()
            ls = ls[0].strip()
            file_length = width
            input_file.close()
            lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
            for i in range(line - 3, len(lines)):
                string = ''
                for e in range(len(lines[i])):
                    string += chars[int(lines[i][e])]
                if i % 1 == 0:
                    output_file.write(string + "        Line: " + str(i) + ', File: ' + file_names[j] + '\n')
                    output_file.write(string + '\n')
                else:
                    output_file.write(string + "        Line: " + str(i) + ', File: ' + file_names[j] + '\n')
                    output_file.write(string + '\n')


def locate_both(path, itype, width, line, output, file = 0):
    if isdir(output):
        output_file = open(output + '/' + 'visualized output.txt', 'a', encoding="utf-8")
    else:
        output_file = open(output, 'a', encoding="utf-8")
    if itype == 'f':
        input_file = open(path, 'r')
        ls = input_file.readlines()
        ls = ls[0].strip()
        file_length = width
        input_file.close()
        lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
        for i in range(line - 3, len(lines)):
            string = ''
            for e in range(len(lines[i])):
                string += chars[int(lines[i][e])]
            if i % 1 == 0:
                output_file.write(string + "        Line: " + str(i) + '\n')
                output_file.write(string + '\n')
                print(string + "        Line: " + str(i) + '\n')
                print(string + '\n', end='')
                input()
            else:
                output_file.write(string + "        Line: " + str(i) + '\n')
                output_file.write(string + '\n')
                print(string + "        Line: " + str(i) + '\n')
                print(string + '\n')

    if itype == 'd':
        file_names = sorted_alphanumeric(listdir(path))
        for i in range(file):
            del file_names[0]

        for j in range(len(file_names)):
            input_file = open(path + '/' + file_names[j], 'r')
            ls = input_file.readlines()
            ls = ls[0].strip()
            file_length = width
            input_file.close()
            lines = [ls[y - file_length:y] for y in range(file_length, len(ls) + file_length, file_length)]
            for i in range(line - 3, len(lines)):
                string = ''
                for e in range(len(lines[i])):
                    string += chars[int(lines[i][e])]
                if i % 1 == 0:
                    output_file.write(string + "        Line: " + str(i) + ', File: ' + file_names[j] + '\n')
                    output_file.write(string + '\n')
                    print(string + "        Line: " + str(i) + ', File: ' + file_names[j] + '\n')
                    print(string + '\n', end='')
                    input()
                else:
                    output_file.write(string + "        Line: " + str(i) + ', File: ' + file_names[j] + '\n')
                    output_file.write(string + '\n')
                    print(string + "        Line: " + str(i) + ', File: ' + file_names[j] + '\n')
                    print(string + '\n')


def display_image(image):
    file = open(image, 'r')
    width = int(file.readline())
    height = int(file.readline())
    s_lines = []
    for _ in range(height):
        s_lines.append(file.readline().strip())
    print("Image: ")
    for i in range(height):
        string = ''
        for e in range(len(s_lines[i])):
            string += chars[int(s_lines[i][e])]
        print(string)
        print(string)


settings = ['d', '', 's', 'n', '', 8, 1, 1, 'd', '']


while True:
    settings = begin(settings)
    if settings[2] == 'v':
        if settings[8] == 'd':
            visualize_display(settings[1], settings[0], settings[5])
        if settings[8] == 'f':
            visualize_file(settings[1], settings[0], settings[5], settings[9])
        if settings[8] == 'b':
            visualize_both(settings[1], settings[0], settings[5], settings[9])
    if settings[2] == 's':
        if settings[8] == 'd':
            search_display(settings[1], settings[0], settings[4], settings[3])
        if settings[8] == 'f':
            search_file(settings[1], settings[0], settings[4], settings[3], settings[9])
        if settings[8] == 'b':
            search_both(settings[1], settings[0], settings[4], settings[3], settings[9])
    if settings[2] == 'f':
        if settings[8] == 'd':
            locate_display(settings[1], settings[0], settings[5], settings[6], file = settings[7])
        if settings[8] == 'f':
            locate_file(settings[1], settings[0], settings[5], settings[6], settings[9], file = settings[7])
        if settings[8] == 'b':
            locate_display(settings[1], settings[0], settings[5], settings[6], file = settings[7])
    if settings[2] == 'd':
        display_image(settings[4])
        input('Press enter to restart...')
        print_space()



# 6 is line 7 is file

