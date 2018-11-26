"""
CS506 : parceExcel
Team : Vidya Akavoor, Lauren DiSalvo, Sreeja Keesara
Description :

Notes : 

October 28, 2018
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime



def bus_hists():
    df = pd.read_excel("2017-2018 Framingham Bus Data.xlsx")
    df.columns = ['school', 'grade', 'res_addr', 'pickup_time', 'pickup_bus', 'pickup_location', 'pickup_stop', 'pickup_stop_desc', 'dropoff_time', 'dropoff_bus', 'dropoff_location', 'dropoff_stop', 'dropoff_stop_desx', 'pickup_dist_from_stop', 'dropoff_dist_from_stop']


    # School: [Drop_off, Start_Time]
    school_time = {"ALT": ["09:20", "09:30"],
                   "BAR": ["08:50", "09:05"],
                   "BRO": ["09:00", "09:15"],
                   "CAM": ["07:55", "08:15"],
                   "CHA": ["08:00", "08:30"],
                   "DUN": ["08:50", "09:05"],
                   "FHS": ["07:00", "07:25"],
                   "FUL": ["07:55", "08:15"],
                   "HEM": ["09:00", "09:15"],
                   "JUN": ["00:00", "00:00"],  # NEEDS VERIFICATION
                   "KNG": ["09:10", "09:25"],
                   "MAR": ["07:18", "07:20"],
                   "MCC": ["08:00", "08:15"],
                   "POT": ["09:00", "09:15"],
                   "STA": ["08:50", "09:05"],
                   "STB": ["00:00", "00:00"],  # NEEDS VERIFICATION
                   "WAL": ["07:55", "08:15"],
                   "WIL": ["08:50", "9:05"]
                   }



    bus_dict = {}
    bus_school = {}

    for index, row in df.iterrows():
        bus_id = row['pickup_bus']
        if type(row['pickup_time']) != str:
            continue
        time = datetime.strptime(row['pickup_time'], '%I:%M %p')
        if bus_id in bus_dict:
            bus_dict[bus_id] += [time]
        else:
            bus_dict[bus_id] = [time]

        if bus_id in bus_school:
            school = row['school']
            if school not in bus_school[bus_id]:
                if school != "JUN" and school != "STB":
                    bus_school[bus_id] += [school]
        else:
            school = row['school']
            if school != "JUN" and school != "STB":
                bus_school[bus_id] = [row['school']]


    for key in bus_dict:
        # get timestamps for labels
        times = bus_dict[key]
        max_timestamp = max(times)
        min_timestamp = min(times)
        dif_stamp = (max_timestamp - min_timestamp) / 10

        # turn timestamps into representative numbers to make bins
        to_timestamp = np.vectorize(lambda x: x.timestamp())
        times = to_timestamp(times)
        max_time = max(times)
        min_time = min(times)
        dif = (max_time - min_time) / 10

        # make bins
        bins = [min_time]
        labels = [min_timestamp.strftime ('%H:%M')]
        next_time = min_time
        next_timestamp = min_timestamp
        for i in range(10):
            next_time += dif
            next_timestamp += dif_stamp
            bins += [next_time]
            labels += [next_timestamp.strftime ('%H:%M')]

        # prepare to make lines for histogram
        schools = bus_school[key]
        starts = [datetime.strptime(school_time[x][1], '%H:%M') for x in schools]
        print(schools)
        starts = to_timestamp(starts)


        # histogram
        plt.figure(figsize=(7,3.5))
        plt.hist(times, bins)
        plt.title("Histogram for bus " + key)
        for time in starts:
            plt.axvline(time, color='r', linewidth=1)

        plt.xticks(bins, labels)
        plt.show()