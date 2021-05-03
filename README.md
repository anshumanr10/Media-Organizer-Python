# Media-Organizer-Python
## Program: Media_Organizer
## Purpose: CLI that allows you to sort photos/videos in a folder by date and location using metadata stored in media file. Currently in development with limited functionality.
## Owner: Anshuman Ranjan
## Contact: anshumanr10@gmail.com

## Purpose: To recursively scan a user-provided directory, find supported media files, extract their metadata,
##          rename the file based on the metadata, and sort the file by date and location taken into folders

## Software Used:
#	- Exiftool by Phil Harvey : https://exiftool.org/
#	- Google Maps Reverse-Geocoding API

## Supported File Types
#	image = ['tiff', 'tif', 'jpeg', 'jpg', 'png', 'raw']
#	video = ['3g2', '3gp', 'avi', 'flv', 'h264', 'm4v', 'mkv', 'mov', 'mp4', 'mpg', 'mpeg', 'wmv']



Instructions on use: 

- Double Click on "Media_Organizer" shortcut (The EXE file is located in "-/dist/Media_Organizer/Media_Organizer.exe")

- Enter the path of the directory where all your media is stored
	- SAFEST METHOD: go to File Explorer, navigate to intended directory, and copy the directory path from the PATH bar.
	  Then, right click in the Command Prompt. The copied PATH should paste itself.

- Enter the path of the directory where you want the sorted media files to be saved.
	- If you leave this field blank, the program will create a folder call Renamed_Files inside the folder
	  you specified in the previous question
	- If you enter a path that doesn't exist, the program will attempt to create that path by itself (May cause program to crash)
	- SAFEST METHOD: Enter a path that already exists or leave the field blank

- Specify if you want the program to look in subdirectories, or just the directory you entered in the previous question (ENTER y OR n)

- Specify if you want the media files to be sorted recursively or linearly.
	- Recursive:
				DD --> Files
			 MM --> DD --> Files
		YYYY --> MM --> DD --> Files
			 MM --> DD --> Files
				DD --> Files
 
	- Linear:
		
		YYYY/MM/DD --> Files
		YYYY/MM/DD --> Files
		YYYY/MM/DD --> Files


DISCLAIMERS: 
- If you need to run the program on the same directory twice (only should be done if program failed the first time),
  make sure the folder "Renamed_Files" does not still exist from the first time the program was run. It should be deleted.
  Failiure to do so should NOT affect the program adversly, but it WILL increase the run time of the program SIGNIFICANTLY
  due to reduntant scanning of the Renamed_Files folder.
