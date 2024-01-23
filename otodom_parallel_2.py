from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import multiprocessing as mp
import time
from os.path  import basename
import requests
from PIL import Image
from IPython.display import display
import pandas as pd

def get_info_otodom(url):
    
    cService = webdriver.ChromeService(executable_path='C:\Program Files (x86)\chromedriver.exe')
    driver = webdriver.Chrome(service = cService)
    driver.get(url)

    try:
        button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        button.click()
    except:
        pass

    driver.maximize_window()

    try:
        button = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/aside/div/div[1]/div/div/div[3]/div/button')
        button.click()
    except:
        pass    
    try:
        tel = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div[1]/div[3]/div/a').text
    except:
        tel = None
    try:
        if tel == None:
            tel = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/aside/div/div[1]/div/div/div[3]/div/a').text
    except:
        tel = None

    try:
        # if driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/button'):
        button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/button')
        button.click()
    except:
        pass  

    try:
        nazwa = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/header/h1').text
    except:
        nazwa = None

    try:
        cena = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/header/strong').text
    except:
        cena = None
    
    try:
        if len(driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/header/div[3]').text) < 15:
            zametr = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/header/div[3]').text  # //*[@id="__next"]/main/div[2]/div[2]/header/div[3]

        elif driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/header/div[4]'):
            zametr = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/header/div[4]').text

    except:
        zametr = None

    try:
        lokalizacja = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div[1]/div[2]/a').text # //*[@id="__next"]/main/div[2]/div[2]/header/div[1]  |  //*[@id="__next"]/main/div[2]/div[2]/header/div[2]/a
    except:
        lokalizacja = None

    try:
        pokoje = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/a').text
    except:
        pokoje = None
    
    try:
        powierzchnia = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[1]/div[2]/div').text
    except:
        powierzchnia = None
    
    try:
        wysposazenie = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div[5]/div/div[10]/div[2]/div').text   # na otodom podpisane jako wyposażenie
    except:
        wysposazenie = None
        
    try:
        czynsz = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[7]/div[2]/div').text
    except:
        czynsz = None
        
    try:
        rodzaj_zabudowy = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div[5]/div/div[5]/div[2]/div').text
    except:
        rodzaj_zabudowy = None
    
    try:
        rynek = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[5]/div/div[1]/div[2]/div').text
    except:
        rynek  = None
    
    try:
        pietro = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[5]/div[2]/div').text
    except:
        pietro  = None

    try:
        typ = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div[5]/div/div[2]/div[2]/div').text   # typ oferenta
    except:
        typ = None
    
    try:
        forma_wlasnosci = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[2]/div[2]/div').text 
    except:
        forma_wlasnosci = None

    try:
        stan_wykonczenia = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[4]/div[2]/div').text 
    except:
        stan_wykonczenia = None

    try:
        balkon_ogrod_taras = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[6]/div[2]/div').text 
    except:
        balkon_ogrod_taras = None

    try:
        miejsce_parkingowe = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[8]/div[2]/span/span/div').text 
    except:
        miejsce_parkingowe = None

    try:
        ogrzewanie = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[10]/div[2]/div').text 
    except:
        ogrzewanie = None

    try:
        button = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/section[2]/div/button')
        button.click()
    except:
        pass

    try:
        opis = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/section[2]/div/div/div').text
    except:
        opis = None
    if opis == 'Obsługa zdalna':
        opis = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/section[3]/div/div/div').text                                             

    col = ['nazwa ogloszenia', 'cena', 'opis', 'lokalizacja', 'zametr','pokoje', 'powierzchnia' , 'wysposażenie', 'czynsz', 'rodzaj zabudowy', 'rynek',
            'piętro', 'typ', 'forma wlasnosci', 'stan wykonczenia', 'balkon/ogrod/taras', 'miejsce parkingowe', 'ogrzewanie', 'telefon']
    dane = [[nazwa, cena, opis, lokalizacja, zametr, pokoje, powierzchnia, wysposazenie, czynsz, rodzaj_zabudowy, rynek,
              pietro, typ, forma_wlasnosci, stan_wykonczenia, balkon_ogrod_taras, miejsce_parkingowe, ogrzewanie, tel]]


    return pd.DataFrame(data=dane,columns=col)

def get_links(url):
    links = []
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    button.click()
    linki = driver.find_elements(By.CSS_SELECTOR, 'a')

    for link in linki:
        if 'oferta' in link.get_attribute("href"):
            links.append(link.get_attribute("href"))
            
    return list(set(links))

def start_scraper(URL, page_start, page_count, threads):
    """Startuje scraper dla OtoDom. Jako page_start należy podać wartość większą od 1, zalecana wartość page_count to nie więcej niż 20.
      Zalecana liczba wątków (threads) to: liczba wątków - 2."""

    urls = []                 

    for i in range(page_start, page_start + page_count):
        url = URL + '''%3Fpage%3D1&page=''' + str(i)
        urls.append(url)

    pool = mp.Pool(threads)      # Ustawia ilczbę wątków
    oficjalne_linki = pool.map(get_links, [url for url in urls])
    pool.close()

    if len(oficjalne_linki) > 1:
        oficjalne_linki = [url for sublist in list for url in sublist]
    else:
        oficjalne_linki = oficjalne_linki[0]

    print(oficjalne_linki)

    pool = mp.Pool(threads)      # Ustawia ilczbę wątków # mp.cpu_count()//2) 
    results = pool.map(get_info_otodom, [url for url in oficjalne_linki]) # [url for i in range(len(oficjalne_linki)) for url in oficjalne_linki[i]]
    pool.close()
    wynik = pd.DataFrame()

    for i in results:
        wynik = pd.concat([wynik, i], ignore_index = True)
        print(wynik)

    wynik['link'] = oficjalne_linki

    wynik.to_csv('D:/Jupyter/MM Python - projekt/oferty_test.csv', sep = ',', index = False, encoding = 'utf-8') 


if __name__ == '__main__':
    mp.freeze_support()
    linki = start_scraper('https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?limit=36&ownerTypeSingleSelect=ALL&daysSinceCreated=7&by=DEFAULT&direction=DESC&viewType=listing', 1, 1, 6)

    # print(linki)
    # print(len(linki))
    # print(len(linki[0]))
    # print(len(linki[1]))
    # print(len(linki[2]))