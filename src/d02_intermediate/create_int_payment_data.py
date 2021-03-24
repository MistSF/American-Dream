import mysql.connector
import numpy as np
import re
import pandas as pd

def createData(cursor, data, name, mydb) :
    """
    Insert data into database
    """
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
    """
        Data cleaning
    """

    gender = ['Male','Female','Prefer not to say','Non-binary/third gender']

    # Remove row without pertinent data

    data = data.loc[data.Country == 'United States']    # On veux des exemples de personnes vivant aux USA
    data = data.loc[data.YearsWithThisTypeOfJob > 0]    # Je veux que les personnes ai au moins 1 ans à leur poste
    data = data.loc[data.SalaryUSD > 10000]             # On vire les salaire à moins de 10 000$
    data = data.loc[data.SalaryUSD < 1000000]           # On vire les salaire supérieur à 1M

    # Hours Per Week
    # On remplace les valeur incohérente par null, ainsi que la réponse Not Asked pour avoir des données cohérentes

    cleanHoursPerWeek = data.HoursWorkedPerWeek.replace(['Not Asked'], [np.nan])
    cleanHoursPerWeek.loc[cleanHoursPerWeek > 100] = np.nan
    data.HoursWorkedPerWeek = cleanHoursPerWeek

    # Gender
    # On vire tout les genre fictif qui ont été répondu

    cleanGender = data.Gender
    cleanGender.loc[(~data.Gender.isin(gender))] = np.nan
    data.Gender = cleanGender

    # Years
    # On vire les + de 40 ans à ce poste

    cleanYearsWithThisTypeOfJob = data.YearsWithThisTypeOfJob
    cleanYearsWithThisTypeOfJob.loc[cleanYearsWithThisTypeOfJob > 40] = np.nan
    data.YearsWithThisTypeOfJob = cleanYearsWithThisTypeOfJob

    # Postal Code
    # On vérifie le format du code ZIP

    cleanPostalCode = data.PostalCode.replace(['Not Asked'], 0)
    newPostal = []
    for x in cleanPostalCode :
        if len(str(x)) > 5 or re.search(r'[a-zA-Z]', str(x)): 
            newPostal.append(np.nan)
        else :
            newPostal.append(x)
    data.PostalCode = pd.Series(newPostal)

    # How Many Comp
    # remplace not asked par 0 pour avoir les même types

    newHowMany = []
    cleanHowManyComp = data.HowManyCompanies.replace(['Not Asked'], 0)
    for x in cleanHowManyComp :
        newHowMany.append(int(str(x)[0]))
    data.HowManyCompanies = pd.Series(newHowMany)

    # Job Title
    # Remplace toutes les variantes de DBA par DBA

    cleanJobTitle = []
    for x in data.JobTitle :
        if "DBA" in x :
            cleanJobTitle.append("DBA")
        else :
            cleanJobTitle.append(x)
    data.JobTitle = pd.Series(cleanJobTitle)

    return data
