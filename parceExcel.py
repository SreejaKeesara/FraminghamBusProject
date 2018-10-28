"""
CS506 : parceExcel
Team : Vidya Akavoor, Lauren DiSalvo, Sreeja Keesara
Description :

Notes : 

October 28, 2018
"""

import xlrd

workbook = xlrd.open_workbook('2016-2017 Framingham Bus Data.xlsx')
worksheet = workbook.sheet_by_name('qmf_temp')

print(worksheet.cell(1,0).value)
