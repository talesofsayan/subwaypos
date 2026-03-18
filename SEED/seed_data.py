import pymysql
from sqlalchemy import create_engine
import pandas as pd
import random as r
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

menu = {
    'PIZZA': [('MARGHERITA', 199), ('FARMHOUSE', 249), ('CHICKEN SUPREME', 299)],
    'BURGER': [('VEGGIE DELIGHT', 99), ('CRISPY CHICKEN', 129), ('CHEESE BLAST', 149)],
    'SANDWICH': [('CLASSIC VEG', 89), ('PANEER TIKKA', 129), ('CHICKEN MAYO', 149)],
    'WRAP': [('VEGGIE ROLL', 109), ('CHICKEN SEEKH WRAP', 159), ('PANEER MASALA WRAP', 139)],
    'SALAD': [('GARDEN FRESH', 89), ('GREEK SALAD', 129), ('CHICKEN PROTEIN BOWL', 169)]
}

names = ['RIYA', 'ALEX', 'PRIYA', 'OM', 'SAMEER', 'TANYA', 'VIRAT', 'ALIA', 'JOHN', 'MAYA']

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)

data = []

ch = '0123456789'
order_ids = set()
delta = timedelta(days=1)
current = start_date

while current <= end_date:
    for _ in range(5):
        item = r.choice(list(menu.keys()))
        variant, price = r.choice(menu[item])
        quantity = r.randint(1, 5)
        tot_amt = price * quantity
        name = r.choice(names)

        while True:
            order_id = "O" + ''.join(r.choices(ch, k=10))
            if order_id not in order_ids:
                order_ids.add(order_id)
                break

        data.append({
            'ORDERID': order_id,
            'DATE': current.strftime('%d-%m-%Y'),
            'NAME': name,
            'ITEM': item,
            'VARIANT': variant,
            'PRICE': price,
            'QUANTITY': quantity,
            'TOTAMT': tot_amt
        })

    current += delta

df = pd.DataFrame(data)
df['ORDERID'] = df['ORDERID'].astype(str)



engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")
con = engine.connect()

df.to_sql('storedata', con,index=False ,if_exists='replace')
print('Fake data inserted in database successfully!')
con.close()