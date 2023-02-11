from selenium.webdriver.common.keys import Keys
from pandas import DataFrame as df
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

driver = webdriver.Chrome('C:/Users/user/chromedriver.exe')
driver.get('https://www.markedbyteachers.com/customer/account/login/')
sleep(1)

#logging
username = driver.find_element_by_xpath('//*[@id="username"]')
passwd = driver.find_element_by_xpath('//*[@id="password"]')
username.send_keys('shivang.ahd1234@gmail.com')
passwd.send_keys('hello123', Keys.ENTER)
sleep(1)

#grabbing the essays
sheet = df({'Topic':[''], 'Essay Title':[''], 'Essay':['']})
topic = 'othello'
counter = 2
driver.get('https://www.markedbyteachers.com/catalogsearch/result/index/?dir=desc&q=othello')

while len(sheet) <= 1000 :

    sleep(3)
    #Imports the HTML of the current page into python
    soup = BeautifulSoup(driver.page_source, 'lxml')
    soup2 = BeautifulSoup(driver.page_source, 'lxml')
    
    #Grabs the HTML of each listing
    essays = soup.find_all('li', id , class_ = 'product')
    links = []
    #grabs all the link for each listing and access it to start grabing the images and tags
    for essay in essays:
        try:
            link = essay.find('a', class_ = 'product-image').get('href')
            driver.get(link)
            sleep(2)
            
            #clicking on read more button
            driver.find_element_by_xpath('//*[@id="product-view-desc-loader"]').click()
            sleep(1)
            
            #grabing title and essay body
            soup = BeautifulSoup(driver.page_source, 'lxml')
            title = soup.find('h1', id='main-title').text.strip()
            # getting only 3200 words max
            essay_body = soup.find('p', id='product-view-desc-desc').text.strip()
            sheet.loc[len(sheet)] = [topic,title,essay_body]
        except:
            pass
   
    #visit the next page
    try:  
        sleep(30)
        nextButton = f'https://www.markedbyteachers.com/catalogsearch/result/index/?dir=desc&p={counter}&q=othello'
        driver.get(nextButton)
        counter += 1
    except:
        break
print('process finished succefully')
driver.close()
sheet.to_csv('C:/Users/user/Desktop/essays-scraper/all_essays.csv', index=False)

