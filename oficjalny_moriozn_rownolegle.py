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
    
    
    try:
        nazwa = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[4]/h1').text
    except:
        nazwa=None

    try:
        cena = driver.find_element(By.XPATH, '//*[@id="basic-info-price-row"]/div/span[1]').text
    except:
        cena=None

    try:
        pokoje = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[2]/span[1]/span').text.split(" ")[0]
    except:
        pokoje = None
    
    try:
        lokalizacja = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[3]/h2/span[2]').text
    except:
        lokalizacja = None
    

    try:
        x=''
        dane = driver.find_elements(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[6]')
        for i in dane:
            x = x + i.text + ', '
        try:
            dane = driver.find_elements(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[7]')
            for i in dane:
                x = x + i.text + ', '
        except:
            pass
        wynik = obrabianie(x)
    except:
        wynik=None

    
    try:
        miejsce_parkingowe = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/main/div[4]/section/div[10]/ul/li[3]/span').text 
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
  
    col = ['nazwa_ogloszenia', 'link','cena', 'opis', 'lokalizacja','pokoje', 'miejsce parkingowe']
    dane = [[nazwa,url,cena, opis, lokalizacja,pokoje, miejsce_parkingowe]]
    czesc = pd.DataFrame(data=dane,columns=col)
    koncowy = pd.concat([czesc, wynik], ignore_index = False ,axis=1)
    driver.quit()

    

    return koncowy

def get_links(url):
    links = []
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    linki = driver.find_elements(By.CSS_SELECTOR, 'a')
    for link in linki:
        try:
            if 'oferta/sprzedaz' in link.get_attribute("href"):
                links.append(link.get_attribute("href"))
        except:
            pass
    return list(set(links))

def obrabianie(dane):
    features_df = pd.DataFrame(columns=['powierzchnia', 'balkon','taras', 'piętro', 'rok budowy','stan wykonczenia'])
    slownik = {'Pow. całkowita':None, 'Balkon':None, 'Taras':None, 'Piętro':None, 'Rok budowy':None,'Stan nieruchomości':None}
    dane = dane.split('\n')
    nowe=[]
    for i in dane:
       nowe.extend(i.split(', '))
    for i in range(0,len(nowe)):
        if nowe[i] in slownik.keys():
            slownik[nowe[i]] = nowe[i+1]
    slownik['powierzchnia']=slownik['Pow. całkowita']
    slownik['stan wykonczenia']=slownik['Stan nieruchomości']
    data_dict_lower = {key.lower(): value for key, value in slownik.items()}
    features_df.loc[len(features_df)] = data_dict_lower
    return features_df


def ogarniacz_linkow(URL, page_start, page_stop,threads):
    urls = []                 

    for i in range(page_start, page_stop):
        url = URL + '?page=' + str(i)
        urls.append(url)

    pool = mp.Pool(threads)      # Ustawia ilczbę wątków
    oficjalne_linki = pool.map(get_links, [url for url in urls])
    pool.close()

    if len(oficjalne_linki) > 1:
        oficjalne_linki = [url for sublist in oficjalne_linki for url in sublist]
    else:
        oficjalne_linki = oficjalne_linki[0]
    return oficjalne_linki
        

def scrapowanie(URL, page_start, page_stop,threads):
    '''url do glownej strony z ktorej ma sciagac linki, page start nr strony na ktorej ma zaczac, page stop numer strony na ktorej ma skonczyc -1, threads liczba watkow'''
    wynik=pd.DataFrame()
    linki = ogarniacz_linkow(URL, page_start, page_stop,threads)

    pool = mp.Pool(threads)      # Ustawia ilczbę wątków # mp.cpu_count()//2) 
    results = pool.map(get_info_morizon, [url for url in linki]) # [url for i in range(len(oficjalne_linki)) for url in oficjalne_linki[i]]
    pool.close()

    for i in results:
        wynik = pd.concat([wynik, i], ignore_index = True)
        

    wynik.to_csv('C:/Studia/modelowanie w pythonie/projekt/morizon_tescik_rownolegle.csv', sep = ',', index = False, encoding = 'utf-8') 
    return wynik

if __name__ == '__main__':
    scrapowanie('https://www.morizon.pl/mieszkania/wroclaw/', 1, 2,4)