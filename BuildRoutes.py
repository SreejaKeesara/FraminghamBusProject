"""
CS506 : BuildRoutes
Team : Vidya Akavoor, Lauren DiSalvo, Sreeja Keesara
Description :

Notes : 

November 10, 2018
"""

import pandas as pd
from datetime import datetime, timedelta
import googlemaps
import os


def create_routes(filename, school):
    df = pd.read_excel(filename)
    df.columns = ['school', 'grade', 'res_addr', 'pickup_time', 'pickup_bus', 'pickup_location', 'pickup_stop', 'pickup_stop_desc', 'dropoff_time', 'dropoff_bus', 'dropoff_location', 'dropoff_stop', 'dropoff_stop_desc', 'pickup_dist_from_stop', 'dropoff_dist_from_stop']
    students = df[df['school'] == school]
    students = students.dropna(subset=['pickup_time', 'pickup_stop_desc'])

    buses_for_pickup = set([x for x in list(students['pickup_bus']) if type(x) == str])
    buses_for_dropoff = set([x for x in list(students['dropoff_bus']) if type(x) == str])

    pickup_routes_by_bus = {}
    dropoff_routes_by_bus = {}

    # print('Bus Routes for School Pickup: ', school)
    for bus in buses_for_pickup:
        # print('Bus: ', bus)
        students_to_pickup = students[students['pickup_bus'] == bus]
        stop_dict = {}
        for x in list(students_to_pickup['pickup_time']):
            datetimeTime = datetime.strptime(x, '%I:%M %p').time()
            if datetimeTime not in stop_dict.keys():
                address = students_to_pickup[students_to_pickup['pickup_time'] == x].iloc[0]['pickup_stop_desc']
                stop_dict[datetimeTime] = [address.replace('*', ''), 1]
            else:
                stop_dict[datetimeTime][1] += 1
        # print(stop_dict)
        pickup_routes_by_bus[bus] = stop_dict

    # print('\nBus Routes for School Dropoff: ', school)
    for bus in buses_for_dropoff:
        # print('Bus: ', bus)
        students_to_dropoff = students[students['dropoff_bus'] == bus]
        stop_dict = {}
        for x in list(students_to_dropoff['dropoff_time']):
            datetimeTime = datetime.strptime(x, '%I:%M %p').time()
            if datetimeTime not in stop_dict.keys():
                address = students_to_dropoff[students_to_dropoff['dropoff_time'] == x].iloc[0]['dropoff_stop_desc']
                stop_dict[datetimeTime] = [address.replace('*', ''), 1]
            else:
                stop_dict[datetimeTime][1] += 1
        # print(stop_dict)
        dropoff_routes_by_bus[bus] = stop_dict

    return pickup_routes_by_bus, dropoff_routes_by_bus


def get_coordinates(address):
    key = os.getenv('GOOGLE_MAPS_API_KEY')
    gmaps = googlemaps.Client(key=key)

    # Geocoding an address
    geocode_result = gmaps.geocode(address[0] + ', Framingham, MA')
    try:
        lat = geocode_result[0]['geometry']['location']['lat']
        long = geocode_result[0]['geometry']['location']['lng']
        return lat, long

    except:
        # print("no latitude or longitude return for this address")
        return None, None


def get_distance(stop1_lat, stop1_long, stop2_lat, stop2_long, departure_time):
    key = os.getenv('GOOGLE_MAPS_API_KEY')
    gmaps = googlemaps.Client(key=key)

    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=departure_time.hour, minute=departure_time.minute, second=0, microsecond=0)

    distance_result = gmaps.directions((stop1_lat, stop1_long), (stop2_lat, stop2_long), departure_time=tomorrow)
    return int(distance_result[0]['legs'][0]['steps'][0]['duration']['text'].split()[0])


def time_to_travel(stop1, stop2, departure_time):
    # print("STOP1 =", stop1, "STOP2 =", stop2)
    stop1_lat, stop1_long = get_coordinates(stop1)
    stop2_lat, stop2_long = get_coordinates(stop2)

    if None not in [stop1_lat, stop1_long, stop2_lat, stop2_long]:
        return get_distance(stop1_lat, stop1_long, stop2_lat, stop2_long, departure_time)
    else:
        return None


def get_time_between_stops(time1, time2):
    datetime1 = datetime.combine(datetime.today(), time1)
    datetime2 = datetime.combine(datetime.today(), time2)

    difference = datetime2 - datetime1
    return int(difference.total_seconds()/60)


def analyze_bus_route(bus_route_dict):
    stops_in_order = sorted(bus_route_dict.keys())
    number_of_stops = len(stops_in_order)

    problematic_stops = []

    for stop in range(number_of_stops):
        if stop != number_of_stops - 1:
            # print("stop ", stops_in_order[stop])
            # print("next stop ", stops_in_order[stop + 1])
            # print(bus_route_dict[stops_in_order[stop]])
            travel_time = time_to_travel(bus_route_dict[stops_in_order[stop]][0], bus_route_dict[stops_in_order[stop + 1]][0], stops_in_order[stop])
            num_students = (bus_route_dict[stops_in_order[stop]][1])/3
            student_times = (num_students * 15.0) // 60
            if travel_time != None:
                travel_time += student_times
            time_between_stops = get_time_between_stops(stops_in_order[stop], stops_in_order[stop+1])
            if travel_time != None and travel_time > time_between_stops:
                # print("problematic - time given to travel between ", bus_route_dict[stops_in_order[stop]], " and ", bus_route_dict[stops_in_order[stop + 1]] + " is ", time_between_stops, " but it takes longer - ", travel_time)
                problematic_stops.append((stops_in_order[stop], bus_route_dict[stops_in_order[stop]], stops_in_order[stop + 1], bus_route_dict[stops_in_order[stop + 1]], travel_time, time_between_stops))
    return problematic_stops


school_time = {"ALT": ["09:20", "09:30", "00:00", "#afd073"],
                   "BAR": ["08:50", "09:05", "15:05", "#fca8e0"],
                   "BRO": ["09:00", "09:15", "15:15", "#8a266c"],
                   "CAM": ["07:55", "08:15", "14:25", "#2c83c0"],
                   "CHA": ["08:00", "08:30", "15:30", "#f2b53b"],
                   "DUN": ["08:50", "09:05", "15:05", "#0479f7"],
                   "FHS": ["07:00", "07:25", "13:55", "#2d9155"],
                   "FUL": ["07:55", "08:15", "14:25", "#d0274a"],
                   "HEM": ["09:00", "09:15", "15:15", "#1eadb4"],
                   "JUN": ["00:00", "00:00", "00:00", "#7bff72"],  # NEEDS VERIFICATION
                   "KNG": ["09:10", "09:25", "15:25", "#2b2f0b"],
                   "MAR": ["07:18", "07:20", "13:45", "#148230"],
                   "MCC": ["08:00", "08:15", "14:15", "#daab99"],
                   "POT": ["09:00", "09:15", "15:15", "#cf7df9"],
                   "STA": ["08:50", "09:05", "15:05", "#c01372"],
                   "STB": ["00:00", "00:00", "00:00", "#c7bce5"],  # NEEDS VERIFICATION
                   "WAL": ["07:55", "08:15", "14:25", "#3817d2"],
                   "WIL": ["08:50", "09:05", "15:05", "#09c904"]
                   }

for school in school_time.keys():
    print("\n\nAnalyzing routes for school ", school)
    pickup, dropoff = create_routes('2017-2018 Framingham Bus Data.xlsx', school)

    print("Pickup Problem Stops")
    problem_pickup_stops_by_bus = {}
    for bus_route in pickup.keys():
        # print("bus ", bus_route)
        problematic_stops = analyze_bus_route(pickup[bus_route])
        if problematic_stops != []:
            problem_pickup_stops_by_bus[bus_route] = problematic_stops

    print(problem_pickup_stops_by_bus)

    print("\nDropoff Problem Stops")
    problem_dropoff_stops_by_bus = {}
    for bus_route in dropoff.keys():
        # print("bus ", bus_route)
        problematic_stops = analyze_bus_route(dropoff[bus_route])
        if problematic_stops != []:
            problem_dropoff_stops_by_bus[bus_route] = problematic_stops

    print(problem_dropoff_stops_by_bus)

# key = os.getenv('GOOGLE_MAPS_API_KEY')
# gmaps = googlemaps.Client(key=key)

# # Geocoding an address
# geocode_result = gmaps.geocode('Winthrop St & Bethany Rd, Framingham, MA')
# print(geocode_result)

# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)
# print(directions_result)