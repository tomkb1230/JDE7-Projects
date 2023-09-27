from selenium import webdriver
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
from database import connect, insertDf, create_table

import time
import csv

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

driver = webdriver.Chrome()

#driver.get("https://www.sasa.com.hk/v2/official/SalePageCategory/1477?sortMode=Sales")   #new_arrival
#driver.get("https://www.sasa.com.hk/v2/official/SalePageCategory/6070?sortMode=Sales")  #personal
driver.get("https://www.sasa.com.hk/v2/official/SalePageCategory/5886?sortMode=Sales")  #skincare


for i in range(15):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

product_name = []
product_id = []
brand = []
restock = []
sold_out = []
original_price = []
discount_price = []
non_shipping = []
url = []


count = 0
supply_stock = driver.find_elements(By.XPATH, '//div[@class="product-card__vertical__media-container"]')


for su in supply_stock:
    # print(su.text)


    try: 
        restock_element = su.find_element(By.XPATH, './/span[contains(text(), "補貨通知")]')
        restock.append(restock_element.text)
        print(restock_element.text)
    except NoSuchElementException:
        restock.append('')
    

    try: 
        sold_out_element = su.find_element(By.XPATH, './/span[contains(text(), "已售完")]')
        sold_out.append(sold_out_element.text)
        print(sold_out_element.text)
    except NoSuchElementException:
        sold_out.append('')


    count += 1
    print("Total:", count)
     

df1 = pd.DataFrame({'Restock': restock, 'Sold_out': sold_out})
print(df1)

     
num_of_result = 0

supply_stock = driver.find_elements(By.XPATH, '//div[@class="sc-kKQOHL hjKVxV"]')
for result in supply_stock:

    product_img = result.find_elements(By.XPATH, ".//*[contains(@href,'SalePage/Index')]")
    for p in product_img:
        url.append(p.get_attribute('href'))
        print(p.get_attribute('href'))

for product in url:    #loop through each product page link on main page
    driver.get(product)

    pt_list = driver.find_elements(By.XPATH, '//div[@class="salepage-info"]')
    for i in pt_list:
        print(i.text.split('\n'))


        try: 
            pro_element = i.find_element(By.XPATH, './/h1[@class="salepage-title"]')
            product_name.append(pro_element.text)
        except NoSuchElementException:
            product_name.append('')

        try: 
            brand_element = i.find_element(By.XPATH, '//ul[@class="salepage-brand-list"]')
            brand.append(brand_element.text.split('\n')[0])
            
        except NoSuchElementException:
            brand.append('')

        try: 
            non_shipping_element = i.find_element(By.XPATH, './/ul[@class="salepage-tag-ul"]')
            non_shipping.append(non_shipping_element.text)
            print(non_shipping_element.text.split('\n'))
        except NoSuchElementException:
            non_shipping.append('')


        try: 
            org_price_element = i.find_element(By.XPATH, './/div[@class="salepage-suggestprice"]')
            original_price.append(org_price_element.text.replace(".00", "").replace(",", "").replace("HK$", ""))
        except NoSuchElementException:
            original_price.append('')

        try: 
            dis_price_element = i.find_element(By.XPATH, './/div[@class="salepage-price cms-moneyColor"]')
            discount_price.append(dis_price_element.text.replace(".00", "").replace(",", "").replace("HK$", ""))
        except NoSuchElementException:
            discount_price.append('')

       
        try: 
            proid_element = i.find_element(By.XPATH, '//ul[@class="salepage-feature"]')
            product_id.append(proid_element.text.split('\n')[1])
            #print(proid_element.text.split('\n')[1])
        except NoSuchElementException:
            product_id.append('')


    num_of_result += 1
    print("Total:", num_of_result)
    if num_of_result > 10:
        break

today = datetime.now()
today_date = datetime.strftime(today, '%Y-%m-%d')

# df["Created Date"] = today_date      
            
df2 = pd.DataFrame({'Product_ID': product_id, 'Product_Name': product_name, 'Brand': brand, 'Tags': non_shipping,
                   'Original_price': original_price, 'Discount_price': discount_price, 'Created_Date': today_date})
print(df2)


df_combine = pd.concat([df1, df2], axis=1)

print(df_combine)
            
#df_combine.to_csv('C:\\Users\\Tom\\Documents\\sasa_Excel file\\sasa焦點新品20230910.csv', index=False, encoding='utf-8-sig')
#df_combine.to_csv('C:\\Users\\Tom\\Documents\\sasa_Excel file\\個人護理20230911.csv', index=False, encoding='utf-8-sig')
#df_combine.to_csv('C:\\Users\\Tom\\Documents\\sasa_Excel file\\sasa護膚保養20230912.csv', index=False, encoding='utf-8-sig')


# bar chart
df1 = pd.read_csv('C:\\Users\\Tom\\Documents\\\sasa_Excel file\\sasa焦點新品20230910.csv')
df2 = pd.read_csv('C:\\Users\\Tom\\Documents\\\sasa_Excel file\\sasa焦點新品20230911.csv')
df3 = pd.read_csv('C:\\Users\\Tom\\Documents\\\sasa_Excel file\\sasa焦點新品20230912.csv')
df4 = pd.read_csv('C:\\Users\\Tom\\Documents\\\sasa_Excel file\\sasa焦點新品20230913.csv')
df5 = pd.read_csv('C:\\Users\\Tom\\Documents\\\sasa_Excel file\\sasa焦點新品20230914.csv')

Date = ('10/9', '11/9', '12/9', '13/9', '14/9')

out_of_stocks = {
    'Stock': np.array([
        df1['Restock'].isnull().sum(),
        df2['Restock'].isnull().sum(),
        df3['Restock'].isnull().sum(),
        df4['Restock'].isnull().sum(),
        df5['Restock'].isnull().sum()
        
    ]),
    'OutOfStock': np.array([
        df1['Restock'].value_counts(dropna=False)['補貨通知'],
        df2['Restock'].value_counts(dropna=False)['補貨通知'],
        df3['Restock'].value_counts(dropna=False)['補貨通知'],
        df4['Restock'].value_counts(dropna=False)['補貨通知'],
        df5['Restock'].value_counts(dropna=False)['補貨通知']
      
    ])}

width = 0.3  # the width of the bars


fig, ax = plt.subplots()
bottom = np.zeros(5)

for new, out_of_stock in out_of_stocks.items():
    p = ax.bar(Date, out_of_stock, width, label=new, bottom=bottom)
    bottom += out_of_stock

    ax.bar_label(p, label_type='center')

ax.set_title('SASA 新品Stock/OutofStock')
ax.legend()

plt.show()


#Connect to postgreSQL


connection = connect()


create_table()


resp = insertDf(connection, df_combine, 'skin_care')