from sqlalchemy import create_engine, text
import pymysql
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")
con = engine.connect()

con.execute(text('CREATE DATABASE IF NOT EXISTS SUBWAY_DATABASE'))
con.close()

engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")
con = engine.connect()

con.execute(text("""CREATE TABLE IF NOT EXISTS storedata (
                 ORDERID TEXT,
                DATE TEXT,
                NAME TEXT,
                ITEM TEXT,
                VARIANT TEXT,
                PRICE BIGINT,
                QUANTITY BIGINT,
                TOTAMT BIGINT)""")
                )

con.execute(text("""CREATE TABLE IF NOT EXISTS MENU (
                 TYPE TEXT,
                 VARIANT TEXT,
                 PRICE BIGINT)""")
                 )

con.close()
