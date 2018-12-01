import pandas as pd
import os
import googlemaps
from datetime import datetime
import matplotlib.ticker as tkr
from gmplot import gmplot

import numpy as np
import matplotlib.pyplot as plt

# pickup histograms with earliest stops highlighted
def get_coordinates(address):
    gmaps = googlemaps.Client(key="AIzaSyCdchjzjhJmNJeycoTjdcGprfmiaFhlhR4")

    # Geocoding an address
    try:
        geocode_result = gmaps.geocode(address + ', Framingham, MA')
        lat = geocode_result[0]['geometry']['location']['lat']
        long = geocode_result[0]['geometry']['location']['lng']
        return lat, long

    except:
        pass

    try:
        geocode_result = gmaps.geocode(address)
        lat = geocode_result[0]['geometry']['location']['lat']
        long = geocode_result[0]['geometry']['location']['lng']
        return lat, long

    except:
        print("no latitude or longitude return for this address: ", address)
        return None, None


def school_histogram(filename):
    key = os.getenv('GOOGLE_MAPS_API_KEY')
    df = pd.read_excel(filename)

    df.columns = ['school', 'grade', 'res_addr', 'pickup_time', 'pickup_bus', 'pickup_location', 'pickup_stop',
                  'pickup_stop_desc', 'dropoff_time', 'dropoff_bus', 'dropoff_location', 'dropoff_stop',
                  'dropoff_stop_desx', 'pickup_dist_from_stop', 'dropoff_dist_from_stop']

    # School: [Drop Off, Start Time, End Time]
    school_time = {"ALT": ["09:20", "09:30", "14:15", "115 A St."],
                   "BAR": ["08:50", "09:05", "15:05", "100 Dudley Rd."],
                   "BRO": ["09:00", "09:15", "15:15", "575 Pleasant St."],
                   "CAM": ["07:55", "08:15", "14:25", "215 Elm St."],
                   "CHA": ["08:00", "08:30", "15:30", "139 Newbury St"],
                   "DUN": ["08:50", "09:05", "15:05", "48 Frost St."],
                   "FHS": ["07:00", "07:25", "13:55", "115 A St."],
                   "FUL": ["07:55", "08:15", "14:25", "31 Flagg Dr."],
                   "HEM": ["09:00", "09:15", "15:15", "729 Water St."],
                   "JUN": ["00:00", "00:00", "00:00", "29 Upper Joclyn Ave."],  # NEEDS VERIFICATION
                   "KNG": ["09:10", "09:25", "15:25", "454 Water St."],
                   "MAR": ["07:18", "07:20", "13:45", "273 Union Ave."],
                   "MCC": ["08:00", "08:15", "14:15", "8 Flagg Dr."],
                   "POT": ["09:00", "09:15", "15:15", "492 Potter Rd."],
                   "STA": ["08:50", "09:05", "15:05", "25 Elm St."],
                   "STB": ["07:45", "08:00", "14:15", "832 Worcester Rd"],
                   "WAL": ["07:55", "08:15", "14:25", "301 Brook St."],
                   "WIL": ["08:50", "09:05", "15:05", "169 Leland St."]
                   }

    # School: [pickup_time1, pickup_time2, pickup_time3, etc.]
    school_dict = dict()
    df = df.dropna(subset=['pickup_time'])
    break_counter = 0

    for index, row in df.iterrows():
        school = row["school"]
        time = datetime.strptime(row["pickup_time"], '%I:%M %p')
        am_dest = row["pickup_stop_desc"]
        pm_dest = row["dropoff_stop_desx"]

        if school not in school_dict:
            school_dict[school] = [[time.timestamp(), am_dest, pm_dest]]
        else:
            school_dict[school] += [[time.timestamp(), am_dest, pm_dest]]

    for y in school_dict:
        gmap = gmplot.GoogleMapPlotter(42.2981, -71.4361, 15)
        gmap.apikey = key

        if break_counter < 100:
            break_counter += 1

            school_times = [item[0] for item in school_dict[y]]
            time_stamps = school_times

            earliest_pickup = datetime.fromtimestamp(min(time_stamps)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[1][:-3]
            latest_pickup = datetime.fromtimestamp(max(time_stamps)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[1][:-3]
            average_pickup = datetime.fromtimestamp(sum(time_stamps)/len(time_stamps)).strftime("%Y-%m-%d %H:%M:%S").split(" ")[1][:-3]

            subtitle = "Earliest Pickup: " + earliest_pickup + " | Latest Pickup: " + latest_pickup +\
                       " | Average Pickup: " + average_pickup + " | Drop Off Time: " + school_time[y][0] + " | Start Time: " + school_time[y][1]

            fig, ax = plt.subplots()

            # create 10 bins evenly spaced out between first and last pickup time per school
            counter = min(time_stamps)
            step = (max(time_stamps) - min(time_stamps))/10.0
            calculated_bins = [counter]
            for x in range(10):
                counter += step
                calculated_bins += [counter]

            # plot histogram
            (n, bins, patches) = ax.hist(time_stamps, color="skyblue", bins=calculated_bins, rwidth=0.8)
            ax.set_xticks(calculated_bins)

            back_to_date = []
            for x in bins:
                back_to_date += [datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S").split(" ")[1][:-3]]

            ax.set_xticklabels(back_to_date)
            ax.xaxis.set_minor_locator(tkr.AutoMinorLocator(n=2))
            ax.xaxis.set_minor_formatter(tkr.FixedFormatter(back_to_date))
            ax.xaxis.set_major_formatter(tkr.NullFormatter())

            for tick in ax.xaxis.get_minor_ticks():
                tick.tick1line.set_markersize(0)

            title = "School Pickup Data for " + str(y)
            plt.suptitle(title, fontsize=14)
            plt.title(subtitle, fontsize=6.5)
            plt.xlabel("Time")
            plt.ylabel("Number of Students")

            plt.show()

            # below is for plotting points on map
            # retrieving data points within each of the histogram bins
            binlist = np.c_[bins[:-1], bins[1:]]
            d = np.array(time_stamps)
            list_time = []
            for i in range(len(binlist)):
                if i == len(binlist) - 1:
                    l = d[(d >= binlist[i, 0]) & (d <= binlist[i, 1])]
                else:
                    l = d[(d >= binlist[i, 0]) & (d < binlist[i, 1])]
                list_time += [l.tolist()]

            school_info = school_dict[y]
            bin_dict = {i: list_time[i] for i in range(0, len(list_time))}
            pickup_dict = {i: [] for i in range(0, len(list_time))}

            for x in school_info:
                for n in range(10):
                    if x[0] in bin_dict[n]:
                        pickup_dict[n] += [(x[1]).replace('*', '')]

            for key in pickup_dict:
                pickup_dict[key] = list(set(pickup_dict[key]))

            lat_dict = {i: [] for i in range(0, 10)}
            lon_dict = {i: [] for i in range(0, 10)}

            for key in pickup_dict:
                for value in pickup_dict[key]:
                    pickup_coordinates = get_coordinates(value)
                    if pickup_coordinates[0] is not None and pickup_coordinates[1] is not None:
                        lat_dict[key] += [pickup_coordinates[0]]
                        lon_dict[key] += [pickup_coordinates[1]]

            # Place map
            colors = ["#ffffff", "#ecd8e9", "#d8b1d4", "#c38bbf", "#ad66a9", "#973e95", "#800080", "#6a0c6a", "#551054", "#411140", "#2d102c"]
            for x in range(10):
                gmap.scatter(lat_dict[x], lon_dict[x], color=colors[x], size=150, marker=False)

            school_location = get_coordinates(school_time[y][-1])
            school_lat_coordinates = [school_location[0]]
            school_lon_coordinates = [school_location[1]]
            gmap.scatter(school_lat_coordinates, school_lon_coordinates, color=colors[10], size=300, marker=False)

            gmap.draw("pickup_" + str(y) + ".html")


school_histogram("2017-2018 Framingham Bus Data.xlsx")

