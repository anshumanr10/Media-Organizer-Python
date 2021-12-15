#Location_Adder.exe
import sys
import os
from directory_management import *

if len(sys.argv) == 1:
    print('Welcome to Location_Adder.exe')
    print('This program will allow you to add a location value to the end of file names')
    print()
    print('HOW TO USE:')
    print(' - Go to File Explorer and select a batch of media files that were taken in a specific location')
    print('   Example: Selecting all photos from your "Washington DC Trip" folder')
    print(' - Drag and Drop the files into this exe file.')
    print(' - The program will launch and ask you to enter 2 location values of your choice(city/state, state/country, etc)')
    print('      EXAMPLE:     Choice 1: Washington DC    Choice 2: Maryland')
    print(' - The program will then rename all your dropped files to include the location values you entered')
    print(' EXAMPLE: Previous Filenames--')
    print('                  20210923-1.jpg')
    print('                  20210923-2.jpg')
    print('                  20210923-3.jpg')
    print('                  20210923-4.jpg')
    print('                  20210923-5.jpg')
    print('          New Filenames--')
    print('                  20210923-1_Washington DC,Maryland.jpg')
    print('                  20210923-2_Washington DC,Maryland.jpg')
    print('                  20210923-3_Washington DC,Maryland.jpg')
    print('                  20210923-4_Washington DC,Maryland.jpg')
    print('                  20210923-5_Washington DC,Maryland.jpg')
    print('\nTo begin the program, drag/drop the files you wish to rename into the exe file')
    input('Press ENTER to exit')
else:
    print('Welcome to Location_Adder.exe')
    print('This program will allow you to add a location value to the end of file names')    
    print()
    print('You have selected ', len(sys.argv)-1, ' files to be renamed')

    value1 = input('What is the first location value to add (EX: city)?: ')
    value2 = input('What is the second location value to add (EX: state)?: ')

    print('This is how your files will look after renaming:')
    print('      Before: file-name.ext        After: file-name_'+value1+','+value2+'.ext')
    print('Warning: ALL selected files will be renamed. This action cannot be undone')
    input('Press ENTER to continue\n')

    all_files = sys.argv[1:]
    for filepath in all_files:
        new_filepath = remove_file_ext(filepath)
        new_filepath = new_filepath+'_'+value1+','+value2+'.'+get_file_ext(filepath)
        os.rename(filepath, new_filepath)
        print('OLD: ' + filepath)
        print('NEW: ' + new_filepath + '\n')
    print('Renaming Completed')
    input('Press ENTER to exit')
