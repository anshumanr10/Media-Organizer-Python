#!/usr/bin/python3
import shutil
import sys
import os
from directory_management import *
from metadata_extraction import *
from datetime import datetime

def reset_requests():
    requests_file = open(os.path.dirname(program_path())+'/requests.txt', 'r')
    requests_file.readline()
    month = int(requests_file.readline())
    year = int(requests_file.readline())
    requests_file.close()
    if year < datetime.now().year or month < datetime.now().month:
        requests_file = open(os.path.dirname(program_path())+'/requests.txt', 'w')
        requests_file.write('0\n')
        requests_file.write(str(datetime.now().month)+'\n')
        requests_file.write(str(datetime.now().year))
        requests_file.close()
        print('The request counter has been reset for this month. You have 39000 requests available again')

def get_requests():
    requests_file = open(os.path.dirname(program_path())+'/requests.txt', 'r')
    requests_sent = int(requests_file.readline())
    requests_file.close()
    if requests_sent > 39000:
        print('\n\nERROR:--- Cannot send more requests to GMaps API without incurring costs this month.')
        print('The request counter will reset next month, try running Part 2 then')
        input('Press ENTER to exit this program')
        sys.exit()
    elif requests_sent + file_data[1] > 39000:
        print('\n\nERROR:--- Number of supported files you are trying to rename might exceed the 39000 request/month limit.')
        print('You can only rename ' + str(39000-requests_sent) + ' more files this month')
        print('Try selecting a lower number of files, or wait till next month')
        input('Press ENTER to exit this program')
        sys.exit()
    else:
        print(str(requests_sent) + ' requests have been made this month, ' + str(39000-requests_sent) + ' requests remaining for use')
    return requests_sent

def set_requests(requests_used):
    requests_file = open(os.path.dirname(program_path())+'/requests.txt', 'r')
    current_requests = int(requests_file.readline())
    requests_file.close()
    requests_file = open(os.path.dirname(program_path())+'/requests.txt', 'w')
    requests_file.write(str(current_requests+requests_used)+'\n')
    requests_file.write(str(datetime.now().month)+'\n')
    requests_file.write(str(datetime.now().year))
    requests_file.close()

print('Media_Organizer_V0.3')
print('For instructions, supported file types, and current issues, refer to the README.txt file')
print('\n\nThis program runs in two seperate parts:')
print(' Part 1: Program will copy all the files, and sort/rename them using their date taken')
print(' Part 2: Program will scan all the files and rename them to include location taken')
print(' WARNING: Part 2 of the program is limited to scanning/renaming 39,000 files/month.')
print('          Only run Part 2 on files you WANT to keep\n')

#sys.argv only works if program is double clicked or program path is included as argument, this code checks for those conditions
if program_path() == '':
    print('Error: Program invoked from Terminal or some unknown source, you must either double click the executable itself,')
    print('       or pass the program\'s path as an argument when invoking from another source.')
    print(' EX: How to invoke from command line:--')
    print('     C:\\Users\\username> Media_Organizer "path/to/Media_Organizer.exe"')
    print('Refer to README for more details')
    input('Press ENTER to exit this program')
    sys.exit()

user_input = input('What part of the program do you want to run? (1 or 2): ')

if user_input == '1':
    user_input = input('Enter PATH to directory you want to sort: ')
    main_dir = fix_path(user_input)

    user_input = input('Enter PATH to directory you want sorted files to go (Leave blank to auto-create): ')
    if user_input == '':
        user_input = main_dir + 'Renamed_Files' + main_dir[-1]
    target_dir = fix_path(user_input)

    all_folders = [main_dir]
    user_input = input('Organize subdirectories? (y or n): ')
    if user_input.lower() == 'y':
        all_folders = list_subdir(main_dir)
        
    print('-----------------------------------------------------------------------------------')
    print('Performing System Checks...')

    file_data = file_count(all_folders)

    print('Discovered '+str(len(all_folders))+' folders and '+str(file_data[0])+' files in selected directory')
    print(str(file_data[1])+' of these files are supported media files and the program will attempt to sort them, the rest will be placed in a folder labeled "not_sorted"')

    if not os.path.exists(fix_path(os.path.dirname(program_path()))+'exiftool.exe'):
        print('\n\nERROR:--- exiftool.exe is missing. it must be in same directory as this executable in order for the program to work')
        input('Press ENTER to exit this program')
        sys.exit()
    else:
        print('exiftool.exe successfully located')
    input('Press ENTER to begin program')
    print('\n-----------------------------------------------------------------------------------\n')

    #Will create destination folder, and rename/copy all files to that folder
    create_folder(target_dir)
    create_folder(target_dir+'not_sorted/')
    create_folder(target_dir+'Videos/')
    
    files_scanned = 0
    files_supported = 0
    files_sorted = 0
    for folder in all_folders:
        print('SCANNING FOLDER: ' + folder + '\n')
        supp_files = list_supported_files(folder)
        unsupp_files = list_unsupported_files(folder)
        failed = 0
        for file in supp_files:
            print('Accessing: ' + file)
            exif = get_exif(folder+file)
            date_taken = get_datetime(exif)

            #Creating new name for file and copying
            if len(date_taken) > 0 and date_taken[0] != '0000':
                new_file_name = str(date_taken[0])+str(date_taken[1])+str(date_taken[2])+'-'+str(date_taken[3])+str(date_taken[4])+str(date_taken[5])+'.'+get_file_ext(file)
            else:
                failed += 1
                new_file_name = file + ''
            print('Copying        ' +folder+file)
            shutil.copy(folder+file, target_dir+new_file_name)

            #Creating new folder for file and moving it
            new_target_dir = target_dir + ''
            if len(date_taken) == 0 or date_taken[0] == '0000':
                new_target_dir += 'not_sorted/'
            else:
                if is_video(new_file_name):
                    new_target_dir += 'Videos/'
                new_target_dir += date_taken[0]+'-'+date_taken[1]+'-'+date_taken[2]+'/'
                create_folder(new_target_dir)
            final_file_name = check_duplicates(new_target_dir, new_file_name)
            print('Moving to      ' + new_target_dir)
            shutil.move(target_dir+new_file_name, new_target_dir+final_file_name)
            print('New Name       ' + final_file_name + '\n')

        not_supp_dir = target_dir+'not_supported'+target_dir[-1]
        create_folder(not_supp_dir)
        for file in unsupp_files:
            final_file_name = check_duplicates(not_supp_dir, file)
            shutil.copy(folder+file, not_supp_dir+final_file_name)
            
        print('\nSupported Files Found: ' + str(len(supp_files)) + '/' + str(len(supp_files)+len(unsupp_files)))
        print('Supported Files w/o Date/Time: ' + str(failed) + '\n')
        files_scanned += len(supp_files)+len(unsupp_files)
        files_supported += len(supp_files)
        files_sorted += len(supp_files)-failed
        
    print('\n-----------------------------------------------------------------------------------\n')
    print('SORTING COMPLETED---- Results:')
    print('                             ' + str(files_scanned) + ' files were scanned')
    print('                             ' + str(files_supported) + ' files were supported by this program')
    print('                             ' + str(files_sorted) + ' files were successfully sorted into folders')
    print()
    input('Press ENTER to end program')
    
elif user_input == '2':
    print('Warning: This part of the program will NOT create a copy of your files, it will simply rename the files which contain GPS data')
    print('File data will not get damaged, but the filenames may have location values appended to them')
    user_input = input('Enter PATH to directory you want files renamed?: ')
    main_dir = fix_path(user_input)
    
    user_input = input('Rename files in subdirectories? (y or n): ')
    if user_input.lower() == 'y':
        all_folders = list_subdir(main_dir)
    else:
        all_folders = [main_dir]

    print('-----------------------------------------------------------------------------------')
    print('Performing System Checks...')

    file_data = file_count(all_folders)
    print('Discovered '+str(len(all_folders))+' folders and '+str(file_data[0])+' files in selected directory')
    print(str(file_data[1])+' of these files are supported media files and the program will attempt to rename them, the rest will remain unchanged')

    if not os.path.exists(fix_path(os.path.dirname(program_path()))+'exiftool.exe'):
        print('\n\nERROR:--- exiftool.exe is missing. it must be in same directory as this executable in order for the program to work')
        input('Press ENTER to exit this program')
        sys.exit()
    else:
        print('exiftool.exe successfully located')

    if not os.path.exists(fix_path(os.path.dirname(program_path()))+'requests.txt'):
        print('\n\nERROR:--- requests.txt is missing. it must be in same directory as this executable in order for the program to work')
        input('Press ENTER to exit this program')
        sys.exit()
    else:
        print('requests.txt successfully located')
    reset_requests()
    get_requests()
    
    input('Press ENTER to begin program')
    print('\n-----------------------------------------------------------------------------------\n')
    
    requests_sent = [0]
    files_scanned = 0
    files_supported = 0
    files_renamed = 0
    for folder in all_folders:
        print('SCANNING FOLDER: ' + folder + '\n')
        supp_files = list_supported_files(folder)
        unsupp_files = list_unsupported_files(folder)
        failed = 0
        for file in supp_files:
            print('Accessing: ' + file)
            exif = get_exif(folder+file)
            coordinates = get_coordinates(exif)
            if coordinates != (360,360):
                address = reverse_geocode(coordinates, 'AIzaSyDyrDVTVT-Ob5a74eFi3Q3C8v01scogTlU', requests_sent)
                print('Address Recieved: ' + str(address))
                if address != []:
                    if len(address) == 1:
                        new_file_name = remove_file_ext(file)+'_'+address[0]+'.'+get_file_ext(file)
                    else:
                        new_file_name = remove_file_ext(file)+'_'+address[0]+','+address[1]+'.'+get_file_ext(file)
                else:
                    failed += 1
                    new_file_name = file + ''
                print('Renaming       ' +folder+file)
                print('New Name       ' +new_file_name + '\n')
                os.rename(folder+file, folder+new_file_name)
            else:
                failed += 1
        print('\nSupported Files Found: ' + str(len(supp_files)) + '/' + str(len(supp_files)+len(unsupp_files)))
        print('Supported Files with no GPS data: ' + str(failed) + '\n\n')
        files_scanned += len(supp_files)+len(unsupp_files)
        files_supported += len(supp_files)
        files_renamed += len(supp_files)-failed

    set_requests(requests_sent[0])
    print('\n-----------------------------------------------------------------------------------\n')
    print('RENAMING COMPLETED---- Results:')
    print('                             ' + str(files_scanned) + ' files were scanned')
    print('                             ' + str(files_supported) + ' files were supported by this program')
    print('                             ' + str(files_renamed) + ' files were successfully renamed')
    print('                             ' + str(requests_sent[0]) + ' requests were sent to GMaps API')
    print('    You can view the total number of requests sent this month in the first line of requests.txt')
    print()
    input('Press ENTER to end program')
else:
    print('Incorrect input, try again')


