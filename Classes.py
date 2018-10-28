"""
CS506 : Classes.py
Team : Vidya Akavoor, Lauren DiSalvo, Sreeja Keesara
Description :

Notes : 

October 28, 2018
"""


class Bus:
    def __init__(self, **kwargs):
        self.capacity = 0
        self.latitude = 0
        self.longitude = 0
        self.yard = None
        self.type = None
        self.yard_address = None
        self.num_on_bus = 0

        if kwargs is not None:
            if 'bus_id' in kwargs:
                self.bus_id = id
            else:
                print("ERROR: no bus id provided")

            self.__dict__.update(kwargs)


class Student:
    def __init__(self, **kwargs):
        self.id = 0
        self.res_latitude = 0
        self.res_longitude = 0
        self.school = None
        self.stop_latitude = 0
        self.stop_longitude = 0

        if kwargs is not None:
            if 'bus_id' in kwargs:
                self.id = id
            else:
                print("ERROR: no bus id provided")

            self.__dict__.update(kwargs)


class School:
    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude