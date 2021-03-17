import mysql.connector
import numpy as np
import re
import pandas as pd

def createData(cursor, data, name, mydb) :
    for x in data.iloc(0) :
        request = """
            INSERT INTO {} (SalaryUSD, Country, PostalCode, JobTitle, YearsWithThisTypeOfJob, HowManyCompanies, 
            OtherPeopleOnYourTeam, Gender, HoursWorkedPerWeek) VALUES (""".format(name)
        for y in x :
            if type(y) == str :
                request = request + "\"" + str(y) + "\", "
            elif str(y) == 'nan' :
                request = request + "NULL , "
            else :
                request =request + str(y) + ", "
        request = request[:-2] + ")"
        try :
            cursor.execute(request)
        except mysql.connector.Error as err :
            print(err)  
    mydb.commit()

def cleanData(data) :
    gender = ['Male','Female','Prefer not to say','Non-binary/third gender']
    data = data[data.Country == 'United States']

    cleanHoursPerWeek = data.HoursWorkedPerWeek.replace(['Not Asked'], [np.nan])
    cleanHoursPerWeek.loc[cleanHoursPerWeek > 100] = np.nan
    data.HoursWorkedPerWeek = cleanHoursPerWeek

    cleanGender = data.Gender
    cleanGender.loc[(~data.Gender.isin(gender))] = np.nan
    data.Gender = cleanGender

    cleanYearsWithThisTypeOfJob = data.YearsWithThisTypeOfJob
    cleanYearsWithThisTypeOfJob.loc[cleanYearsWithThisTypeOfJob > 40] = np.nan
    data.YearsWithThisTypeOfJob = cleanYearsWithThisTypeOfJob

    # Postal Code

    cleanPostalCode = data.PostalCode.replace(['Not Asked'], 0)
    newPostal = []
    for x in cleanPostalCode :
        if len(str(x)) > 5 or re.search(r'[a-zA-Z]', str(x)): 
            newPostal.append(np.nan)
        else :
            newPostal.append(x)
    data.PostalCode = pd.Series(newPostal)

    # How Many Comp

    newHowMany = []
    cleanHowManyComp = data.HowManyCompanies.replace(['Not Asked'], 0)
    for x in cleanHowManyComp :
        newHowMany.append(int(str(x)[0]))
    data.HowManyCompanies = pd.Series(newHowMany)

    return data
