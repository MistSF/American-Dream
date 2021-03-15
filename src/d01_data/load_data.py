import pandas as  pd

def load2020(path) :
    data = pd.read_csv(path)
    df1 = data[['Job Title', 'Salary Estimate', 'Company Name', 'Location', 'Rating', 'Size', 'Sector']]
    for x in df1 :
        print(x)