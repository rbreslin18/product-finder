from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd
def main():
    root = Tk()

    #Providing Geometry to the form
    root.geometry("750x750")

    #Providing title to the form
    root.title('Item finder')

    #this creates 'Label' widget for Registration Form and uses place() method.
    label_0 =Label(root,text="Item Finder", width=20,font=("bold",20))
    #place method in tkinter is  geometry manager it is used to organize widgets by placing them in specific position
    label_0.place(x=190,y=60)

    #this creates 'Label' widget for Fullname and uses place() method.
    label_1 =Label(root,text="URL", width=20,font=("bold",10))
    label_1.place(x=100,y=130)

    #this will accept the input string text from the user.
    entry_1=Entry(root)
    entry_1.place(x=290,y=130)

    #this creates 'Label' widget for Email and uses place() method.
    label_3 =Label(root,text="search item", width=20,font=("bold",10))
    label_3.place(x=100,y=180)

    entry_3=Entry(root)
    entry_3.place(x=290,y=180)




    #the variable 'var' mentioned here holds Integer Value, by deault 0
    var=IntVar()




    ##this creates 'Label' widget for country and uses place() method.
    label_5=Label(root,text="Where to search",width=20,font=("bold",10))
    label_5.place(x=70,y=280)

    #this creates list of countries available in the dropdownlist.
    list_of_country=[ 'Google' ,'Amazon' , 'Ebay' ,'Germany' ,'Austria']

    #the variable 'c' mentioned here holds String Value, by default ""
    c=StringVar()
    droplist=OptionMenu(root,c, *list_of_country)
    droplist.config(width=50)
    c.set('Select where to retrieve items(unfinished)')
    droplist.place(x=240,y=280)




    #the variable 'var1' mentioned here holds Integer Value, by default 0


    #this creates button for submitting the details provides by the user and also begins the Selenium search
    Button(root, text='Submit' , width=20,bg="black",fg='white', command=lambda: search(entry_1.get(),entry_3.get())).place(x=275,y=380)


    #this will run the mainloop.
    root.mainloop()

def search(url,item):
    web = url
    

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome()
    driver.get(web)

    driver.implicitly_wait(5)
    keyword = item
    search = driver.find_element(By.ID, 'twotabsearchtextbox')
    search.send_keys(keyword)
    # click search button
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    search_button.click()

    driver.implicitly_wait(5)

    product_asin = []
    product_name = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []

    items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for item in items:
        # find name
        name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
        product_name.append(name.text)

        # find ASIN number 
        data_asin = item.get_attribute("data-asin")
        product_asin.append(data_asin)

        # find price
        whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
        
        if whole_price != [] and fraction_price != []:
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        else:
            price = 0
        product_price.append(price)

        # find ratings box
        ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

        # find ratings and ratings_num
        if ratings_box != []:
            ratings = ratings_box[0].get_attribute('aria-label')
            ratings_num = ratings_box[1].get_attribute('aria-label')
        else:
            ratings, ratings_num = 0, 0
        
        product_ratings.append(ratings)
        product_ratings_num.append(str(ratings_num))
        
        # find link
        link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
        product_link.append(link)
        #next_button = driver.find_element(By.CLASS_NAME, 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator')
        #next_button.click()
    driver.quit()

    # to check data scraped
    print(product_name)
    print(product_asin)
    print(product_price)
    print(product_ratings)
    print(product_ratings_num)
    print(product_link)
    df = pd.DataFrame({'Product Name':product_name,'Product ASIN':product_asin,'Price':product_price,'Rating':product_ratings,'Product rating num':product_ratings_num,'Product Link':product_link}) 
    df.to_csv(keyword+'.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    main()