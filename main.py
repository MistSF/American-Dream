import conf.config as cfg
import src.d01_data.load_data as ld
import src.d02_intermediate.create_int_payment_data as cip
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host=cfg.mysql["host"],
    user=cfg.mysql["user"],
    password=cfg.mysql["passwd"],
    auth_plugin='mysql_native_password'
)

cursor = mydb.cursor(buffered=True)

try :
    cursor.execute("USE American_Dream")
except mysql.connector.Error as err :
    print(err)

columns = ['SalaryUSD', 'Country', 'PostalCode', 'JobTitle', 'YearsWithThisTypeOfJob', 'HowManyCompanies', 'OtherPeopleOnYourTeam', 'Gender', 'HoursWorkedPerWeek']
data = ld.loadExcel('/home/apprenant/American-Dream/Data/01_RAW.xlsx', 3, columns)

data = cip.cleanData(data)
# cip.createData(cursor, data, "2020Data" , mydb)
data.to_csv('./Data/02_Clean.csv')
