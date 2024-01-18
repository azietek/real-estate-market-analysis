from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import multiprocessing as mp
import time
from os.path  import basename
import requests
from PIL import Image
from IPython.display import display
import pandas as pd


def get_info_morizon(url):
    
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(8)
    button = driver.find_element(By.XPATH, '//*[@id="rasp_cmp"]/div/div[6]/button[2]')
    button.click()
    
    
    nazwa = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[4]/h1').text

    try:
        cena = driver.find_element(By.XPATH, '//*[@id="basic-info-price-row"]/div/span[1]').text
    except:
        cena = None

    try:
        zametr = driver.find_element(By.XPATH, '//*[@id="basic-info-price-row"]/div/span[2]').text
    except:
        zametr = None

    try:
        pokoje = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[2]/span[1]/span').text.split(" ")[0]
    except:
        pokoje = None
    
    try:
        lokalizacja = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[3]/h2/span[2]').text
    except:
        lokalizacja = None
    
    
    try:
        umeblowane = driver.find_element(By.XPATH, ).text  ##########################
    except:
        umeblowane = None
        
    try:
        czynsz = driver.find_element(By.XPATH, ).text #############
    except:
        czynsz = None
        
   

    try:
        typ = driver.find_element(By.XPATH, ).text ################
    except:
        typ = None
    
    
    try:
        stan_wykonczenia = driver.find_element(By.XPATH, ).text ##########
    except:
        stan_wykonczenia = None

    try:
        x=''
        dane = driver.find_elements(By.CLASS_NAME, '_3GSGCU')
        for i in dane:
            x = x + i.text + ', '
        wynik = obrabianie(x)
    except:
        wynik=None

    
    try:
        miejsce_parkingowe = driver.find_element(By.XPATH, ).text ##########
    except:
        miejsce_parkingowe = None


    try:
        button = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[4]/button')
        button.click()
    except:
        pass

    try:
        opis = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[4]/div').text
    except:
        opis = None
  
    col = ['nazwa_ogloszenia', 'cena', 'opis', 'lokalizacja','zametr','pokoje' , 'umeblowane', 'czynsz', 'typ','stan wykonczenia', 'miejsce parkingowe']
    dane = [[nazwa, cena, opis, lokalizacja,zametr,pokoje, umeblowane, czynsz, typ, stan_wykonczenia, miejsce_parkingowe]]
    czesc = pd.DataFrame(data=dane,columns=col)
    koncowy = pd.concat([czesc, wynik], ignore_index = False ,axis=1)
    

    

    return koncowy

def obrabianie(dane):
    features_df = pd.DataFrame(columns=['powierzchnia', 'balkon','taras', 'forma wlasnosci', 'rodzaj zabudowy', 'ogrzewanie', 'rynek', 'piętro'])
    slownik = {'Pow. całkowita':None, 'Balkon':None, 'Taras':None, 'Forma własności':None,  'Typ budynku':None, 'Ogrzewanie':None, 'Rynek':None, 'Piętro':None}
    dane = dane.split('\n')
    nowe=[]
    for i in dane:
       nowe.extend(i.split(', '))
    for i in range(0,len(nowe)):
        if nowe[i] in slownik.keys():
            slownik[nowe[i]] = nowe[i+1]
    slownik['forma wlasnosci']=slownik['Forma własności']
    slownik['rodzaj zabudowy']=slownik['Typ budynku']
    slownik['powierzchnia']=slownik['Pow. całkowita']
    
    data_dict_lower = {key.lower(): value for key, value in slownik.items()}
    features_df.loc[len(features_df)] = data_dict_lower
    return features_df
        


urls=['https://www.morizon.pl/mieszkania/wroclaw/']
for i in range(2,162):#162
    url = 'https://www.morizon.pl/mieszkania/wroclaw/'+ '?page=' + str(i)
    urls.append(url)


def get_links(url):
    links = []
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(9)
    button = driver.find_element(By.XPATH, '//*[@id="rasp_cmp"]/div/div[6]/button[2]')
    button.click()
    linki = driver.find_elements(By.CSS_SELECTOR, 'a')
    for link in linki:
        try:
            if 'oferta/sprzedaz' in link.get_attribute("href"):
                links.append(link.get_attribute("href"))
        except:
            pass
    return list(set(links))


if __name__ == '__main__':
    pool = mp.Pool(2)#mp.cpu_count()//2) #na razie 2 watki mozna podkrecic
    oficjalne_linki = pool.map(get_links, [url for url in urls])
    pool.close()
    pool = mp.Pool(2)#mp.cpu_count()//2) #na razie 2 watki mozna podkrecic
    results = pool.map(get_info_morizon, [url for url in oficjalne_linki[0]])
    pool.close()
    wynik = pd.DataFrame()
    for i in results:
        wynik=pd.concat([wynik, i], ignore_index = True)
    print(wynik)
    wynik.to_csv('C:/Studia/modelowanie w pythonie/projekt/oferty_morizon.csv', sep = ',', index = False, encoding = 'utf-8') 