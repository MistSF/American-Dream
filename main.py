import conf.config as cfg
import src.d01_data.load_data as ld

mydb = mysql.connector.connect(
    host=cfg.mysql["host"],
    user=cfg.mysql["user"],
    password=cfg.mysql["passwd"],
    auth_plugin='mysql_native_password'
)

cursor = mydb.cursor(buffered=True)

ld.load2020('/home/apprenant/American-Dream/Data/DataAnalyst.csv')