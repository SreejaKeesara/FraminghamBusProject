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



# times = [datetime.strptime(df['pickup_time'][1], '%I:%M %p'), datetime.strptime(df['pickup_time'][13], '%I:%M %p')]
# times.sort()
# time1 = times[0].time()


df = pd.read_excel("2017-2018 Framingham Bus Data.xlsx")
df.columns = ['school', 'grade', 'res_addr', 'pickup_time', 'pickup_bus', 'pickup_location', 'pickup_stop', 'pickup_stop_desc', 'dropoff_time', 'dropoff_bus', 'dropoff_location', 'dropoff_stop', 'dropoff_stop_desx', 'pickup_dist_from_stop', 'dropoff_dist_from_stop']

bus_dict = {}

for index, row in df.iterrows():
    bus_id = row['pickup_bus']
    if type(row['pickup_time']) != str:
        continue
    time = datetime.strptime(row['pickup_time'], '%I:%M %p')
    if bus_id in bus_dict:
        bus_dict[bus_id] += [time]
    else:
        bus_dict[bus_id] = [time]


for key in bus_dict:
    times = bus_dict[key]
    to_timestamp = np.vectorize(lambda x: x.timestamp())
    times = to_timestamp(times.sort())
    # np.histogram(, 10)
    plt.hist(times)
    plt.title("Histogram for bus", key)
    plt.show()
    break







































