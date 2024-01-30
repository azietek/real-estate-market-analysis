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
    '''Funkcja bioraca pojedynczy link do oferty morizona i wyciagajaca z niego informacje: nazwa, cena, pokoje, lokalizacja,
    miejsce_parkingowe, opis, 'powierzchnia', 'balkon','taras', 'piętro', 'rok budowy','stan wykonczenia'.
    Zwraca DF z informacjami, None jesli nie bylo info.'''
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
    '''Funkcja scrapujaca linki z storny morizona z linkami, wybiera tylko te faktycznie dotyczace ofert. Zwraca liste z linkami bez duplikacji.
    url - strona z ktorej chcemy zebrac linki'''
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
    '''Funkcja wyciagajaca ze zlepionego tekstu danych z morizona informacje, ktore nas interesuja i znajdowaly sie na zmiennej czesci storny. Zwraca wyniki w formie df.
    '''
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
    '''Url do glownej storny moziona z linkami, page_start od jakiej strony zaczac, page_stop na jakiej skonczyc. Zbiera linki do ofert z 
    podanego zakresu stron, zwraca je w formie listy. threads- liczba watkow'''
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
    '''Funkcja sklejajaca wszystkie powyzsze i odpalajaca wszystko automatycznie, Url do glownej strony morizona, page_start page_stop zakres stron jakie ma zescrapowac. 
    threads- liczba watkow'''
   
    wynik=pd.DataFrame()
    linki = ogarniacz_linkow(URL, page_start, page_stop,threads)

    pool = mp.Pool(threads)      
    results = pool.map(get_info_morizon, [url for url in linki]) 
    pool.close()

    for i in results:
        wynik = pd.concat([wynik, i], ignore_index = True)
        

    wynik.to_csv('C:/Studia/modelowanie w pythonie/projekt/morizon_tescik_rownolegle.csv', sep = ',', index = False, encoding = 'utf-8') 
    return wynik

if __name__ == '__main__':
    scrapowanie('https://www.morizon.pl/mieszkania/wroclaw/?ps%5Bdate_from%5D=2024-01-27&0%5Bfbclid%5D=IwAR1uIl9_A2K99371JUNZYhIVMo85bnQFFA6IhFKzefQeAfKe3cvPx1pNWgQ', 1, 2,4)
