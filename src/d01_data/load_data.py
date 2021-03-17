import pandas as  pd
import mysql.connector

def loadExcel(path, skiprows=0, columns=-1) :
    all_data_xl = pd.read_excel(path, skiprows=skiprows)
    if columns != -1 :
        data = all_data_xl[columns]
        return data
    else :
        return all_data_xl

def loadCSV(path, columns=-1) :
    all_data_csv = pd.read_csv(path)
    if columns != -1 :
        data = all_data_csv[columns]
    else :
        return all_data_csv
