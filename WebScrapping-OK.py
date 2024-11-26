
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import jdatetime

# extract all items and price from the given url : www.shop.okcs.com    
def GetAllItemsAndPrice(UrlSite):
    #base_url = "https://shop.okcs.com/group/sanitary-cleaning1401?fromPrice=17626&toPrice=220554&sortBy[0]=discount_percent&sortBy[1]=desc&page={}"
    extendUrl = "{}?fromPrice=8000&toPrice=1499000&sortBy[0]=discount_percent&sortBy[1]=desc&page={}"
    base_url =UrlSite + extendUrl 
    
    # Define the data frame for Categories
    Categories = {
      
        'id': ['1', '2','3','4','5','6','7','8','9','10'],
        'CategoriName': ['groceries', 'beverages', 'snacks', 'protein-material', 'dairy', 
                         'cosmetics-sanitary', 'canned-and-prepared-food', 'house-cleaning', 
                         'seasoning-and-spices', 'home-and-lifestyle'],
        'PersianCategoriName': ['کالای اساسی و خواروبار', 'نوشیدنی ها', 'تنقلات', 'مواد پروتئینی', 
                                'لبنیات', 'آرایشی و بهداشتی', 'کنسرو و غذای آماده', 
                                'نظافت منزل', 'چاشنی و ادویه جات', 'خانه و سبک زندگی']
    }

    # Categories = {
    #     'id': ['1'],
    #     'CategoriName': ['groceries'],
    #     'PersianCategoriName': ['کالای اساسی و خواروبار']
    # }

    dataCategory = pd.DataFrame(Categories)

    gregorian_date = datetime.now()
    persian_date = jdatetime.date.today()  
    
    dataF = pd.DataFrame(columns=['CategoriName', 'PersianCategoriName','ProductName','Price','MDate','PersianDate'])
    # Iterate over each item in the CategoriName list
    for i in range(len(dataCategory)):
      # Start with the first page
      row = dataCategory.iloc[i]
      page_number = 1
      products_found = True
    
      while products_found:
        # Format the URL with the current page number
        url = base_url.format(row['CategoriName'],page_number)
        print(url)
        # Send an HTTP GET request to the URL
        response = requests.get(url)
    
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the page with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all product containers (Assuming each product has a specific class)
            products = soup.find_all('div', class_='col-lg-3 col-md-4 col-sm-6 col-6 pb-3 pl-2')  # refer to the actual class used in the HTML
    
            # Check if products were found on the page
            if not products:
                products_found = False
                break
    
            # Loop through each product and extract the name and price
            for product in products:
                # Assuming the product name and price are within specific tags
                name = product.find('div', class_='promotion__title ellipsis-2').text.strip()  # refer to the actual class used in the HTML
                price = product.find('div', class_='promotion__price').text.strip()  # refer to the actual class used in the HTML

                data = [{'CategoriName': row['CategoriName'], 'PersianCategoriName': row['PersianCategoriName'] ,'ProductName' :name ,
                          'Price': price, 'MDate' : gregorian_date , 'PersianDate' :  persian_date}]
                df = pd.DataFrame(data)
                dataF = pd.concat([dataF, df], ignore_index=True)
            # Move to the next page
            page_number += 1
        else:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            break
    
    return dataF


# Base URL
UrlSite = "https://shop.okcs.com/category/"
Result = GetAllItemsAndPrice(UrlSite)
Result.to_csv('D:/OK-Price.csv', index=False , encoding='utf-8-sig')   
print("It's Done!")
