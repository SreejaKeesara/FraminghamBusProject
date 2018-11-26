import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np


def school_histogram(filename):
    df = pd.read_excel(filename)
    df.columns = ['school', 'grade', 'res_addr', 'pickup_time', 'pickup_bus', 'pickup_location', 'pickup_stop',
                  'pickup_stop_desc', 'dropoff_time', 'dropoff_bus', 'dropoff_location', 'dropoff_stop',
                  'dropoff_stop_desx', 'pickup_dist_from_stop', 'dropoff_dist_from_stop']

    # School: [Drop Off, Start Time]
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

    # School: [pickup_time1, pickup_time2, pickup_time3, etc.]
    school_dict = dict()
    df = df.dropna(subset=['pickup_time'])

    for index, row in df.iterrows():
        school = row["school"]
        time = datetime.strptime(row['pickup_time'], '%I:%M %p')
        if school not in school_dict:
            school_dict[school] = [time]
        else:
            school_dict[school] += [time]

    to_timestamp = np.vectorize(lambda x: x.timestamp())

    for y in school_dict:
        time_stamps = to_timestamp(school_dict[y])
        time_stamps = time_stamps.tolist()

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


school_histogram("2017-2018 Framingham Bus Data.xlsx")

