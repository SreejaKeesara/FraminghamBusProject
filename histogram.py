import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


#df = pd.read_excel("2017-2018 Framingham Bus Data.xlsx")
#print(df)


def school_histogram(filename):
    df = pd.read_excel(filename)
    df.columns = ['school', 'grade', 'res_addr', 'pickup_time', 'pickup_bus', 'pickup_location', 'pickup_stop',
                  'pickup_stop_desc', 'dropoff_time', 'dropoff_bus', 'dropoff_location', 'dropoff_stop',
                  'dropoff_stop_desx', 'pickup_dist_from_stop', 'dropoff_dist_from_stop']

    school_dict = dict()
    df = df.dropna(subset=['pickup_time'])
    for index, row in df.iterrows():
        school = row["school"]
        time = datetime.strptime(row['pickup_time'], '%I:%M %p')
        if school not in school_dict:
            school_dict[school] = [time]
        else:
            school_dict[school] += [time]

    print("Timestamps BEFORE: ", school_dict["BAR"])
    to_timestamp = np.vectorize(lambda x: x.timestamp())
    time_stamps = to_timestamp(school_dict["BAR"])
    print("Timestamps AFTER: ", time_stamps)
    plt.hist(time_stamps)
    print("done")
    # for key in school_dict:
    #     school_dict[key] = sorted(school_dict[key])
    #
    #
    # plt.hist(school_dict["BAR"], bins=10)
    plt.show()
   # print(school_dict)
school_histogram("2017-2018 Framingham Bus Data.xlsx")

