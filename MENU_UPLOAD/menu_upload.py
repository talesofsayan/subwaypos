import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")
con = engine.connect()

piz = 'menu//pizza.csv'
bur = 'menu//burger.csv'
sand = 'menu//sandwich.csv'
wr = 'menu//wrap.csv'
sal = 'menu//salad.csv'

pizza = pd.read_csv(piz)
pizza.name = 'pizza'

burger = pd.read_csv(bur)
burger.name = 'burger'

sandwich = pd.read_csv(sand)
sandwich.name = 'sandwich'

wrap = pd.read_csv(wr)
wrap.name = 'wrap'

salad = pd.read_csv(sal)
salad.name = 'salad'

li = [pizza,burger,sandwich,wrap,salad]

df = pd.DataFrame(columns=['TYPE','VARIANT','PRICE'])

for i in range(len(li)):
    for j in range(len(li[i])):
        df.loc[len(df)] = [li[i].name,li[i]['variant'][j],li[i]['price'][j]]

df.to_sql('menu',con,index=False,if_exists='replace')
con.close()
