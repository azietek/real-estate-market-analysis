import jinja2
import pdfkit
from datetime import datetime
import pandas as pd
import time 

import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

def generate_pdf(data):
    """Generuje plik PDF na podstawie podanej ramki danych dotyczącej nieruchomości."""

    df = data.iloc[0:7]

    # zbieranie linków do zdjęć
    img_urls = []

    for url in df['link']:
        driver = webdriver.Chrome()
        driver.get(url)

        try:
            img = driver.find_element(By.CLASS_NAME, 'image-gallery-image')
            img_urls.append(img.get_attribute("src"))
        except:
            pass

        driver.quit()

    html_mail = ''''''

    with open('D:/Jupyter/MM Python - projekt/mail/html_mail.html', 'w', encoding='utf-8') as file:
        file.write(html_mail)

    # Modyfikacja pliku html

    with open('D:/Jupyter/MM Python - projekt/mail/html_mail.html', 'r') as file:
        html_content = file.read()

        for i in range(df.shape[0]):
            
            # zbieranie zdjęć
            img_path = img_urls[i]

            # uzpełnianie opisu
            lokalizacja = df.iloc[i]['lokalizacja']
            cena = df.iloc[i]['cena']
            powierzchnia = df.iloc[i]['powierzchnia']
            pokoje = int(df.iloc[i]['pokoje'])
            pietro = df.iloc[i]['piętro']
            r_zabudowy = df.iloc[i]['rodzaj zabudowy']
            telefon = df.iloc[i]['telefon']
            link_o = df.iloc[i]['link']

            html_code = \
                '''<p style="padding-left: 10px;">

                <img align="left" src="{}" alt="Oferta" width="300" height="300", a>

                <strong>Lokalizacja</strong>: {}
                <br /><strong>Cena</strong>: {}
                <br /><strong>Powierzchnia</strong>: {}
                <br /><strong>Liczba pokoi</strong>: {}
                <br /><strong>Piętro</strong>: {}
                <br /><strong>Rodzaj zabudowy</strong>: {}
                <br /><strong>Telefon</strong>: {}
                <br /><strong>Link</strong>: <a href="{}">{}</a></p>
                
                <p style="padding-left: 10px;">&nbsp;</p>
                <p>&nbsp;</p>
                '''
                
            formatted_html_code = html_code.format(img_path, lokalizacja, cena, powierzchnia, pokoje, pietro, r_zabudowy, telefon, link_o, link_o)

            html_content += formatted_html_code

    html_preamble = '''
    <html>

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-teal.css">

    <head>
        <meta charset="utf-8">
    </head>

    <body>

    <div class="w3-card-4">

    <div class="w3-container w3-theme w3-card">
    <h1 style="text-align: center;">Raport nieruchomości {}</h1>
    </div>

    <div class="w3-theme-l5">

    </div>
    '''

    data = datetime.now().strftime('%d-%m-%Y')
    html_preamble = html_preamble.format(data)

    html_tail = '''
    </div>

    </body>
    </html>
    '''

    with open('D:/Jupyter/MM Python - projekt/mail/html_mail.html', 'w', encoding='utf-8') as file:
        file.write(html_preamble)
        file.write(html_content)
        file.write(html_tail)

# Wysyłanie Maila

def sent_mail(sender, receiver, body, pdf_dir):
    """Wysyła maila z ofertami spełniającymi kryteria użytkownika."""

    # Genereowanie PDF

    template_loader = jinja2.FileSystemLoader('D:/Jupyter/MM Python - projekt/mail')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('html_mail.html')

    pdf_content = template.render()

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    output_pdf_path = 'D:/Jupyter/MM Python - projekt/mail/Raport.pdf'  
    pdfkit.from_string(pdf_content, output_pdf_path, configuration=config,
                        css='D:/Jupyter/MM Python - projekt/mail/style.css', options={"enable-local-file-access": ""})
    
    # Wysyłanie Maila

    msg = MIMEMultipart()              # pozwala na dodawanie plików do maila
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Python Projekt'

    with open('D:/Jupyter/MM Python - projekt/mail/password.txt', "r") as f:
        password = f.readline()
    
    # Treść maila
    msg.attach(MIMEText(body, 'plain'))

    # Dodanie załącznika PDF
    attachment = open(pdf_dir, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename = Raport.pdf')
    msg.attach(part)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())  # msg.as_string() - zapewnia poprawny format maila

properties = pd.read_csv('D:/Jupyter/MM Python - projekt/mail/sample4map2.csv')
# generate_pdf(properties)
# sent_mail('Raport.wyceny@gmail.com', 'piotr.granieczny26@gmail.com', 'Twój raport nieruchomości.', 'D:/Jupyter/MM Python - projekt/mail/Raport.pdf')

# Schedule the tasks
schedule.every().sunday.at("23:10").do(generate_pdf, properties)
schedule.every().sunday.at("23:10").do(sent_mail, 'Raport.wyceny@gmail.com', 'piotr.granieczny26@gmail.com', 'Twój raport nieruchomości.', 'D:/Jupyter/MM Python - projekt/mail/Raport.pdf')

# Keep the script running
while True:
    schedule.run_pending() # sprawdza czy są zadania do wykonania
    time.sleep(1)          # ma na celu ogranieczenie zużycia zasobów CPU