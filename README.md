###### Program: Media_Organizer (Version 0.4) Updated: 12/15/2021
###### Owner: Anshuman Ranjan
###### Contact: anshumanr10@gmail.com

WARNINGS:
- DO NOT MODIFY/CHANGE exiftool.exe or requests.txt. Doing so will break the program
- PROGRAM IS NOT GUARENTEED TO BE STABLE: Has been developed as a side project for personal use.
	It has undergone very basic testing and its results should be checked for bugs.
- Part 2 has some limitations, details included in "Instructions on use"

### Purpose: To recursively scan a user-provided directory, find supported media files, extract their metadata,
###          rename the file based on the metadata, and sort the file by date and location taken into folders

### Software Used:
###	- Exiftool by Phil Harvey : https://exiftool.org/
###	- Google Maps Reverse-Geocoding API

### Supported File Types
###	image = ['jpg', 'jpeg', 'png', 'raw', 'tiff', 'tif']
###	video = ['mp4', 'mov', 'mpg', 'mpeg', 'wmv', 'mkv', 'h264', 'm4v', 'flv', 'avi', '3gp', '3g2']


*Instructions on use:* 

- Double Click on Media_Organizer.exe

- Media_Organizer has two components:
	- Part 1: Copy, rename and sort files based on their date taken
	- Part 2: Rename files to include their location taken

- Follow the on-screen instructions to sort your files. Any questions/ideas on what to include in these directions,
  contact me through my email.

- Part 2 can only rename a maximum of 39000 files/month, since each attempt to rename a file can cost up to 2 requests
  to the GMaps API server and GMaps only allows 40k requests per month for free. Ideally, the program will only request the location
  for files that contain coordinates, and each file will only require 1 request, but there are cases where files may contain inaccurate
  coordinates or coordinates that dont point to an exact formatted address. In these situations, 2 requests may be sent to either
  get a less accurate name, or simply to determine that the coordinates are incorrect
	- Example: Due to smartphone's GPS error, a jpg's coordinates may point to a random location in the Pacific Ocean
	- IF YOU HAVE DOWNLOADED THIS PROGRAM FROM GITHUB: Please be courteous and only use Part 2 on <100 files for testing purposes
	  or use your own API key for everyday use.
