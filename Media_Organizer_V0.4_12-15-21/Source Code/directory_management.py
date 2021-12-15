import os
import sys

## Supported File Types
image = ['jpg', 'jpeg', 'png', 'raw', 'tiff', 'tif']
video = ['mp4', 'mov', 'mpg', 'mpeg', 'wmv', 'mkv', 'h264', 'm4v', 'flv', 'avi', '3gp', '3g2']

def program_path():
    program_path = sys.argv[0]
    if sys.argv[0] == '' and len(sys.argv) > 1:
        program_path = sys.argv[1]
        if not os.path.exists(program_path):
            program_path = os.getcwd()
    return program_path

def fix_path(folder_path):
    fixed_path = folder_path + ''
    if folder_path[-1] != '/' and folder_path[-1] != '\\':
        fixed_path = folder_path + "/"
    return fixed_path

def list_subdir(folder_path):
    folder_path = fix_path(folder_path)
    subdir_list = [folder_path]
    folder_contents = os.listdir(folder_path)
    for item in folder_contents:
        if os.path.isdir(folder_path+item):
            subdir_list += list_subdir(folder_path+item+folder_path[-1])
    return subdir_list

def file_count(folder_list):
    num_files = 0
    supp_files = 0
    for folder in folder_list:
        items = os.listdir(folder)
        for item in items:
            if os.path.isfile(folder+item):
                num_files += 1
                if is_supported(item):
                    supp_files += 1
    return [num_files, supp_files]
    

def get_file_ext(file_name):
    reversed_filename = file_name[::-1]
    file_ext = reversed_filename[:reversed_filename.find('.')][::-1]
    return file_ext

def remove_file_ext(file_name):
    reversed_filename = file_name[::-1]
    new_file_name = reversed_filename[reversed_filename.find('.')+1:][::-1]
    return new_file_name

def is_supported(file_name):
    supported = False
    file_ext = get_file_ext(file_name).lower()
    if file_ext in image+video:
        supported = True
    return supported

def is_video(file_name):
    isVideo = False
    file_ext = get_file_ext(file_name).lower()
    if file_ext in video:
        isVideo = True
    return isVideo

def list_supported_files(folder_path):
    folder_path = fix_path(folder_path)
    subdir_list = os.listdir(folder_path)
    supported_file_list = []
    for item in subdir_list:
        if os.path.isfile(folder_path+item) and is_supported(item):
            supported_file_list.append(item)
    return supported_file_list

def list_unsupported_files(folder_path):
    folder_path = fix_path(folder_path)
    subdir_list = os.listdir(folder_path)
    unsupported_file_list = []
    for item in subdir_list:
        if os.path.isfile(folder_path+item) and not is_supported(item):
            unsupported_file_list.append(item)
    return unsupported_file_list


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

def check_duplicates(folder_path, filename):
    if not os.path.exists(folder_path+filename):
        new_file_name = filename + ''
    else:
        duplicate = 0
        new_file_name = remove_file_ext(filename) +'('+str(duplicate)+').'+get_file_ext(filename)
        while os.path.exists(folder_path+new_file_name):
            duplicate += 1
            new_file_name = new_file_name[::-1][new_file_name[::-1].find('(')+1:][::-1] + '(' + str(duplicate) + ').' + get_file_ext(filename)
    return new_file_name
