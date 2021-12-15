#Location_Remover.exe
import sys
import os
from directory_management import *

if len(sys.argv) == 1:
    print('Welcome to Location_Remover.exe')
    print('This program will allow you to remove location values from the end of file names')
    print()
    print('HOW TO USE:')
    print(' - Go to File Explorer and select a batch of media files that have a location value in the filename')
    print('   Example: Selecting the photo "2018-12-31_Washington DC,Maryland.jpg"')
    print(' - Drag and Drop the files into this exe file.')
    print(' - The program will then rename all your dropped files to exclude the location values')
    print(' EXAMPLE: Previous Filenames--')
    print('                  20210923-1_Washington DC,Maryland.jpg')
    print('                  20210923-2_Detroit,Michigan.jpg')
    print('                  20210923-3_Chicago,Illinois.jpg')
    print('                  20210923-4_Chicago,Illinois.jpg')
    print('                  20210923-5_Tampa,Florida.jpg')
    print('          New Filenames--')
    print('                  20210923-1.jpg')
    print('                  20210923-2.jpg')
    print('                  20210923-3.jpg')
    print('                  20210923-4.jpg')
    print('                  20210923-5.jpg')
    print('WARNING: THIS PROGRAM WILL DELETE ANY VALUES IN THE FILENAME THAT EXIST AFTER THE "_" CHARACTER')
    print('         TO AVOID ERRORS, MAKE SURE ALL SELECTED FILES FOLLOW THE NAMING FORMAT SHOWN IN THE EXAMPLES ABOVE')
    print('Accidently including files with no location values in their name will not harm the file unless it has an "_" character')
    print('\nTo begin the program, drag/drop the files you wish to rename into the exe file')
    input('Press ENTER to exit')
else:
    print('Renaming Files... Please Wait\n')
    all_files = sys.argv[1:]
    for filepath in all_files:
        new_filepath = filepath[::-1][filepath[::-1].find('_')+1:][::-1]+'.'+get_file_ext(filepath)
        os.rename(filepath, new_filepath)
        print('OLD: ' + filepath)
        print('NEW: ' + new_filepath + '\n')
    print('Renaming Completed')
    input('Press ENTER to exit')
