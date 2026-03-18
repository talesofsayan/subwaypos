import pymysql
from sqlalchemy import create_engine
import matplotlib.pyplot as py
import pandas as pd
import random as r
import hashlib as hs
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__),'..','.env'))

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
admin_password_hash = os.getenv('ADMIN_PASSWORD_HASH')

gen_db = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")

menu_db_con = gen_db.connect()
datab = gen_db.connect()

pizza = pd.read_sql("select variant, price from menu where type='pizza';",menu_db_con)
burger = pd.read_sql("select variant, price from menu where type='burger';",menu_db_con)
sandwich = pd.read_sql("select variant, price from menu where type='sandwich';",menu_db_con)
wrap = pd.read_sql("select variant, price from menu where type='wrap';",menu_db_con)
salad = pd.read_sql("select variant, price from menu where type='salad';",menu_db_con) 

item = {
    'PIZZA':pizza,
    'BURGER':burger,
    'SANDWICH':sandwich,
    'WRAP':wrap,
    'SALAD':salad
}

print("========================")
print("| ****** SUBWAY ****** |")
print("========================")

while True:

    gendb = gen_db.connect()
    gen = pd.read_sql('select * from storedata;',gendb)
    gendb.close()

    print("+------------------------------+")
    print("| 1. CUSTOMER PORTAL           |")
    print("| 2. ADMIN PORTAL              |")
    print("+------------------------------+")
    print('| stop. QUIT PROGRAM           |')
    print("+------------------------------+")

    portal = input('ENTER MODE : ').upper()

    if portal == '1':

        while True:

            print("+---------------------+")
            print("| 1. VIEW MENU        |")
            print("| 2. PLACE ORDER      |")
            print("+---------------------+")
            print("| exit. EXIT PORTAL   |")
            print("+---------------------+")

            print()
            mode = input("ENTER MODE : ").upper()
            print()

            if mode == '1':

                print("+----------------------------------+")
                print('PIZZA : ')
                print(pizza)
                print("+----------------------------------+")
                print('BURGER : ')
                print(burger)
                print("+----------------------------------+")
                print('SANDWICH : ')
                print(sandwich)
                print("+----------------------------------+")
                print('WRAP : ')
                print(wrap)
                print("+----------------------------------+")
                print('SALAD : ')
                print(salad)
                print("+----------------------------------+")

                defi = input("PRESS ENTER TO CONTINUE")

            elif mode == '2':

                while True:

                    date = str(input("ENTER DATE OF ORDER (DD-MM-YYYY) : ")).upper()
                    
                    if date == 'EXIT':
                        print('QUITING ...')
                        break

                    name = input('ENTER YOUR NAME : ')

                    order_item = input("ITEM : ").upper()

                    if order_item in item:

                        mdf = item[order_item]

                        codes = list(gen.loc[:,'ORDERID'])

                        while True:
                            order_id = "O" + "".join(r.choices('0123456789', k = 10))

                            if order_id not in codes:
                                break

                        while True:
                            print("Choose no. of your variant : ")
                            print()
                            print(mdf)
                            print()

                            var = int(input("-> "))
                            if var in mdf.index:
                                variant = mdf.loc[var,'variant']
                                break

                            else:
                                print()
                                print('INVALID INPUT ! TRY AGAIN PROPERLY')
                                print("-->")

                        print()
                        quantity = int(input('quantity : '))
                        price = mdf.loc[var,'price']
                        t_amt = quantity*price
                        tot_amt = int(t_amt)

                        dfs = {
                            'ORDERID': str(order_id),
                            'DATE':str(date).upper(),
                            'NAME':str(name).upper(),
                            'ITEM':str(order_item).upper(),
                            'VARIANT':str(variant).upper(),
                            'PRICE':int(price),
                            'QUANTITY':int(quantity),
                            'TOTAMT':int(tot_amt)
                            }

                        df = pd.DataFrame(dfs,index=[0])
                        print()
                        print(df)
                        print()
                        
                        df.to_sql('storedata',datab,index = False, if_exists='append')

                        break      

                    else:
                        print('ITEM NOT IN OUR STORE OR INVALID INPUT ! PLEASE RETRY ..')
                        print()

            elif mode == 'EXIT':
                print("EXITING ...")
                print()
                break

            else:
                print('INVALID INPUT | TRY AGAIN !')

    elif portal == '2':

        print()
        pass_ask = input('Enter Password: ')
        has_pas = hs.sha256(pass_ask.encode()).hexdigest()

        if has_pas == admin_password_hash:

            while True:

                gendb = gen_db.connect()
                gen = pd.read_sql('select * from storedata;',gendb)
                gendb.close()

                print('+------------------------------+')
                print("| 1. EDIT ENTRY                |")
                print("| 2. DELETE ENTRY              |")
                print("| 3. VIEW ALL DATA OF ORDERS   |")
                print("| 4. VIEW SPECIFIC DATA        |")
                print("| 5. SALES GRAPH               |")
                print('+------------------------------+')
                print("| exit. EXIT PORTAL            |")
                print('+------------------------------+')

                ask = input('ENTER MODE : ').upper()

                if ask == '1':

                    print()

                    code = input("ENTER ORDER-ID : ").upper()
                    o_list = gen.loc[:,'ORDERID']
                    o_list = list(o_list)

                    if code in o_list:
                        print(gen.loc[gen['ORDERID'] == code])

                        ask_item = input('ITEM : ').upper()
                        v_pr = item[ask_item]
                        print(v_pr)
                        ask_var = int(input("ENTER INDEX OF VARIENT : "))
                        var_l = v_pr.loc[ask_var,'variant']
                        pr = v_pr.loc[ask_var,'price']
                        ask_q = int(input("QUANTITY : "))

                        gen.loc[gen['ORDERID'] == code,'ITEM'] = ask_item
                        gen.loc[gen['ORDERID'] == code,'VARIANT'] = var_l.upper()
                        gen.loc[gen['ORDERID'] == code,'QUANTITY'] = ask_q
                        gen.loc[gen['ORDERID'] == code,'PRICE'] = pr
                        gen.loc[gen['ORDERID'] == code,'TOTAMT'] = pr*ask_q

                        s = (gen.loc[gen['ORDERID'] == code])

                        print(gen.loc[gen['ORDERID'] == code])

                        gen.to_sql('storedata',datab,index = False, if_exists='replace')

                        print("EDITING DONE !")
                        print()

                    else:
                        print('INVALID ORDERID ! TRY AGAIN ..')


                elif ask == '2':

                    ask = input('ENTER ORDERID : ').upper()

                    print(gen.loc[gen['ORDERID'] == ask])

                    o_list = gen.loc[:,'ORDERID']
                    o_list = list(o_list)

                    while True:

                        if ask in o_list:
                            
                            df = gen.loc[gen['ORDERID'] != ask]
                            df.to_sql('storedata',datab,index=False,if_exists='replace')
                            print('DELETED SUCCESSFULLY !')
                            print()
                            
                            break

                        elif ask == 'exit'.upper():
                            print('EXITING MODE ..')

                            break

                        else:
                            print('INVALID ! TRY AGAIN OR TYPE EXIT ..')

                    print()

                elif ask == '3':

                    print()
                    print(gen)
                    print()

                elif ask == '4':

                    while True:

                        c_ask = input('ENTER ORDERID : ').upper()
                        l_order = list(gen.loc[:,'ORDERID'])

                        if c_ask in l_order:
                            print()
                            sp_data = gen.loc[gen['ORDERID'] == c_ask]
                            print("---------------------------------------------------------------------------------------")
                            print(sp_data)
                            print("---------------------------------------------------------------------------------------")
                            print()
                            break

                        elif c_ask == 'exit'.upper():
                            print('EXITING MODE ...')
                            break

                        else:
                            print('INVALID CODE | TRY AGAIN OR TYPE STOP TO EXIT MODE')

                elif ask == '5':

                    df = gen
                    df_t = gen.loc[:,'DATE']

                    dd = []
                    mm = []
                    yyyy = []

                    test_list = list(df_t)

                    for i in test_list:
                        dd.append(i[0:2])
                        mm.append(i[3:5])
                        yyyy.append(i[6:10])

                    df.loc[:,'dd'] = dd
                    df.loc[:,'mm'] = mm
                    df.loc[:,'yyyy'] = yyyy

                    sa = df.loc[:,'yyyy']

                    yr_str = []

                    for i in sa:
                        if i not in yr_str:
                            yr_str.append(i)

                    print('VALID YEARS OF DATA IN ENTRY : ',yr_str)
                    print()
                    
                    
                    print("ENTER YEAR or TYPE 'LATEST' FOR LATEST ENTERED YEAR GRAPH | or TYPE 'YEARLY' TO GET YEARLY GRAPH : ")
                    ask_year = input("-> ").upper()

                    if (ask_year != 'YEARLY' and ask_year in yyyy) or ask_year == 'LATEST':

                        if ask_year == 'latest'.upper():
                            ask_year = yyyy[-1]

                        l_yr = yyyy[-1]

                        print("+-------------+")
                        print("| Daily   : 1 |")
                        print("| Monthly : 2 |")
                        print("+-------------+")

                        g_ask = int(input('-> '))

                        f = []

                        for t in yyyy:
                            if t not in f:
                                f.append(t)

                        if g_ask == 1:

                            l1 = list(gen.loc[gen['yyyy'] == ask_year,'DATE'])

                            date_l = []
                            d_price = []

                            for i in l1:
                                if i not in date_l:
                                    date_l.append(i)

                            for t in date_l:
                                dp = sum(gen.loc[gen['DATE'] == t,'TOTAMT'])
                                d_price.append(dp)

                            py.bar(date_l,d_price)
                            py.xlabel(f'DAYS OF LATEST ENTRY YEAR DATA - {ask_year}')
                            py.ylabel('SALES - [in INR]')
                            py.show()

                        elif g_ask == 2:

                            m_price = []

                            month = ['01','02','03','04','05','06','07','08','09','10','11','12']
                            month_str = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']
                            
                            d1 = df.loc[df['yyyy'] == ask_year]

                            for t in month:
                                d2 = d1.loc[d1['mm'] == t]

                                ds = d2.loc[:,'TOTAMT']

                                dp = sum(list(ds))

                                m_price.append(dp)

                            py.bar(month_str,m_price)
                            py.xlabel(f'MONTHS OF LATEST ENTRY YEAR DATA - {ask_year}')
                            py.ylabel('SALES - [in INR]')
                            py.show()

                    elif ask_year == 'YEARLY':

                        y_price = []

                        f = []

                        for t in yyyy:
                            if t not in f:
                                f.append(t)

                        for i in f:
                            d1 = df.loc[df['yyyy'] == i]

                            ds = d1.loc[:,'TOTAMT']
                            dp = sum(list(ds))

                            y_price.append(dp)

                        py.bar(yr_str,y_price)
                        py.xlabel('YEARS')
                        py.ylabel('SALES - [in INR]')
                        py.show()

                    else:
                        print('INVALID INPUT OR YEAR !')


                elif ask.upper() == 'EXIT':
                    print('EXITING PORTAL ...')
                    print()
                    break

                else:
                    print('INVALID INPUT !')

        else:
            print('Invalid password')

    elif portal == "stop".upper():
        
        print("QUITING ! HAVE A GOOD TIME")
        break

    elif portal == '3':

        print('testing section')
        
    else:
        print('INVALID INPUT !')

    print()
