"""
CS506 : parceExcel
Team : Vidya Akavoor, Lauren DiSalvo, Sreeja Keesara
Description :

Notes : 

October 28, 2018
"""

import xlrd
import xlwt
from Classes import Bus, School, Student

workbook = xlrd.open_workbook('2016-2017 Framingham Bus Data.xlsx')
worksheet = workbook.sheet_by_name('qmf_temp')

studentResidentialAddresses = worksheet.col_values(2)
bus = Bus(bus_id=5, capacity=60)
print(bus.latitude)



