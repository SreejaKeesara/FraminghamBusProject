"""
CS506 : parceExcel
Team : Vidya Akavoor, Lauren DiSalvo, Sreeja Keesara
Description :

Notes : 

October 28, 2018
"""

import xlrd
import os
import googlemaps
import xlwt
from Classes import Bus, School, Student




KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key= KEY)

def format_dictionary(dictionary, dict_type):
    if dict_type == "school":
        for x in dictionary:
            print(x, "  :   ( school_id: ", dictionary[x].school_id, " , longitude: ", dictionary[x].longitude, " , latitude: ", dictionary[x].latitude, ")")

    elif dict_type == "student":
        for x in dictionary:
            print(x, "  :   ( student_id: ", dictionary[x].student_id, " , res_latitude: ", dictionary[x].res_latitude,
                  " , res_longitude: ", dictionary[x].res_longitude, " , res_school: ", format_dictionary(dictionary[x].res_school, "school"),
                  " , stop_latitude: ", dictionary[x].stop_latitude, " , stop_longitude: ", dictionary[x].stop_longitude, ")")


def create_current_routes():
    SCHOOL_ADDRESS_DICT = {"ALT": "115 A St.",  # NEEDS VERIFICATION
                           "BAR": "100 Dudley Rd.",
                           "BRO": "575 Pleasant St.",
                           "CAM": "215 Elm St.",
                           "CHA": "139 Newbury St",  # NEEDS VERIFICATION
                           "DUN": "48 Frost St.",
                           "FHS": "115 A St.",
                           "FUL": "31 Flagg Dr.",
                           "HEM": "729 Water St.",
                           "JUN": "29 Upper Joclyn Ave.",
                           "KNG": "454 Water St.",
                           "MAR": "115 A St.",  # NEEDS VERIFICATION
                           "MCC": "8 Flagg Dr.",
                           "POT": "492 Potter Rd.",
                           "STA": "25 Elm St.",
                           "STB": "115 A St.",  # NEEDS VERIFICATION
                           "WAL": "301 Brook St.",
                           "WIL": "169 Leland St.",
                           }

    school_dict = dict()
    bus_dict = dict()
    student_dict = dict()

    workbook = xlrd.open_workbook('2017-2018 Framingham Bus Data.xlsx')
    sheet = workbook.sheet_by_name('qmf_temp')

    for row in range(1, sheet.nrows):
        school_id = sheet.row(row)[0].value
        if school_id not in school_dict:
            school_address = SCHOOL_ADDRESS_DICT[school_id] + ", Framingham, MA"
            school_geocode = gmaps.geocode(school_address)[0]['geometry']['location']
            school_dict[school_id] = School(school_id, school_geocode['lng'], school_geocode['lat'])

        student_id = row - 1
        if student_id not in student_dict:
            student_address = sheet.row(row)[2].value + ", Framingham, MA"
            student_geocode = gmaps.geocode(student_address)[0]['geometry']['location']
            student_school = school_dict[school_id]
            stop_address = sheet.row(row)[7].value  # used AM stop destination
            stop_geocode = gmaps.geocode(stop_address)[0]['geometry']['location']
            student_dict[student_id] = Student(student_id=student_id, res_latitude=student_geocode['lat'],
                                               res_longitude=student_geocode['lng'], school=student_school,
                                               stop_latitude=stop_geocode['lat'], stop_longitude=stop_geocode['lng'])

        bus_id = sheet.row(row)[4].value
        if bus_id not in bus_dict:
            bus_dict[bus_id] = Bus(bus_id=bus_id)

        format_dictionary(student_dict, "student")


create_current_routes()




