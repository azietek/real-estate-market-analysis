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

def get_info_otodom(url):
    
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(1)
    button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    button.click()
    driver.maximize_window()
    
    nazwa = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/header/h1').text
    cena = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/header/strong').text

    
    try:
        zametr = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/header/div[3]').text
    except:
        zametr = None

    try:
        pokoje = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/a').text
    except:
        pokoje = None
    
    try:
        lokalizacja = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/header/div[2]/a').text
    except:
        lokalizacja = None
    
    try:
        powierzchnia = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[1]/div[2]/div').text
    except:
        powierzchnia = None
    
    try:
        umeblowane = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[6]/div/div[10]/div[2]/div').text   # na otodom podpisane jako wyposażenie
    except:
        umeblowane = None
        
    try:
        czynsz = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[7]/div[2]/div').text
    except:
        czynsz = None
        
    try:
        rodzaj_zabudowy = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[6]/div/div[5]/div[2]/div').text
    except:
        rodzaj_zabudowy  = None
    
    try:
        rynek = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[5]/div/div[1]/div[2]/div').text
    except:
        rynek  = None
    
    try:
        pietro = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[2]/div/div[5]/div[2]/div').text
    except:
        pietro  = None

    try:
        typ = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div[6]/div/div[2]/div[2]/div').text   # typ oferenta
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
        
    col = ['nazwa_ogloszenia', 'cena', 'opis', 'lokalizacja','zametr','pokoje', 'powierzchnia' , 'umeblowane', 'czynsz' , 'rodzaj zabudowy', 'rynek', 'piętro', 'typ', 'forma wlasnosci','stan wykonczenia', 'balkon/ogrod/taras', 'miejsce parkingowe', 'ogrzewanie']
    dane = [[nazwa, cena, opis, lokalizacja,zametr,pokoje, powierzchnia, umeblowane, czynsz, rodzaj_zabudowy, rynek, pietro, typ, forma_wlasnosci, stan_wykonczenia, balkon_ogrod_taras, miejsce_parkingowe, ogrzewanie]]

    

    

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


urls=['https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing']
for i in range(2,257):
    url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing'+ '''%3Fpage%3D1&page=''' +str(i)
    urls.append(url)


if __name__ == '__main__':
    pool = mp.Pool(2)#mp.cpu_count()//2) #na razie 2 watki mozna podkrecic
    oficjalne_linki = pool.map(get_links, [url for url in urls])
    pool.close()
    pool = mp.Pool(2)#mp.cpu_count()//2) #na razie 2 watki mozna podkrecic
    results = pool.map(get_info_otodom, [url for url in oficjalne_linki[0]])
    pool.close()
    wynik = pd.DataFrame()
    for i in results:
        wynik=pd.concat([wynik, i], ignore_index = True)
    wynik.to_csv('C:/Studia/modelowanie w pythonie/projekt/oferty.csv', sep = ',', index = False, encoding = 'utf-8') 