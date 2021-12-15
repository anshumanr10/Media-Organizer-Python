import os
import sys
import googlemaps
from directory_management import *

## Requires: exiftool.exe exists
## Returns:  A dictionary containing file ExifData
def get_exif(file_path):
    exiftool_path = fix_path(os.path.dirname(program_path()))
    terminal_call = '"' + exiftool_path + '"exiftool "' + file_path + '"' #Tested on Windows Only
    exif_list = os.popen(terminal_call).readlines()
    exif_dictionary = {}
    for line in exif_list:
        semicolon = line.find(':')
        spaces = line.find('  ')
        if spaces == -1:
            key = line[:semicolon]
        else:
            key = line[:spaces]
        value = line[semicolon+2:]
        exif_dictionary[key]=value
    return exif_dictionary

## Returns: A list containing date/time (Empty list if no DateTime data found)
def get_datetime(exif_dictionary):
    datetime = ''
    try:
        datetime = exif_dictionary['Create Date']
        print('DateTime Information PASSED')
    except:
        print('No DateTime data found')
    datetime_list = []
    if datetime != '':
        datetime_list += [datetime[0:4]]
        datetime_list += [datetime[5:7]]
        datetime_list += [datetime[8:10]]
        datetime_list += [datetime[11:13]]
        datetime_list += [datetime[14:16]]
        datetime_list += [datetime[17:19]]
    return datetime_list


def parse_dms(dms_str):
    dms_list = []
    temp_dms_str = dms_str + ''
    dms_list += [temp_dms_str[:temp_dms_str.find(' ')]]
    temp_dms_str = temp_dms_str[temp_dms_str.find('g')+2:]
    dms_list += [temp_dms_str[:temp_dms_str.find('\'')]]
    temp_dms_str = temp_dms_str[temp_dms_str.find(' ')+1:]
    dms_list += [temp_dms_str[:temp_dms_str.find('"')]]
    dms_list += [temp_dms_str[-2]]
    return dms_list
## Returns: A tuple containing coordinates (360,360: if not GPS Data found)
##          Tuple is used because googlemaps api requires tuple parameter
def get_coordinates(exif_dictionary):
    lat_dms = ''
    long_dms = ''
    try:
        lat_dms = exif_dictionary['GPS Latitude']
        long_dms = exif_dictionary['GPS Longitude']
        print('GPS Coordinates PASSED')
    except:
        print('No GPS data found')
    lat = 360
    long = 360
    if lat_dms != '':
        lat_list = parse_dms(lat_dms)
        long_list = parse_dms(long_dms)
        print('DMS-- Latitude: ' + str(lat_list) + '    Longitude: ' + str(long_list))
        lat = float(lat_list[0]) + float(lat_list[1])/60.0 + float(lat_list[2])/3600.0
        long = float(long_list[0]) + float(long_list[1])/60.0 + float(long_list[2])/3600.0
        if lat_list[3] in ['S','W']:
            lat = -1 * lat
        if long_list[3] in ['S','W']:
            long = -1 * long
    return (round(lat,5), round(long,5))


def reverse_geocode(coordinates, api_key, requests_sent):
    gmaps = googlemaps.Client(key=api_key)
    address = []
    city_list = gmaps.reverse_geocode(coordinates, '|locality')
    requests_sent[0] += 1
    if len(city_list) == 0:
        print('Unable to locate city, attempting second request with less accuracy...')
        city_list = gmaps.reverse_geocode(coordinates, '|administrative_area_level_1')
        requests_sent[0] += 1
    if len(city_list) == 0:
        print('Coordinates INACCURATE (GMaps API Failed)')
    else:
        address_str = city_list[0]['formatted_address']
        while address_str.find(', ') > -1:
            address += [address_str[0:address_str.find(', ')]]
            address_str = address_str[address_str.find(', ')+2:]
        address += [address_str]
    return address
