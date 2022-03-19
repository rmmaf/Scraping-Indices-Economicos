import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time
from datetime import datetime
from datetime import timedelta
def wait_for_downloads(path):
    print("Waiting for downloads", end="")
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(path)]):
        time.sleep(1)
        print(".", end="")
    print("done!")

downloadPath = os.path.abspath('./../database/idkaIPCA')
os.makedirs(downloadPath, mode=0o777, exist_ok=True)  # create dir if it not exist

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--allow-running-insecure-content")
options.add_argument("--window-size=1920,1080")
options.add_argument('--no-sandbox')
options.add_argument(f'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36')
options.add_argument("--remote-debugging-address=0.0.0.0")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--disable-browser-side-navigation")
options.add_experimental_option('prefs', {
"download.default_directory": downloadPath, #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})

print("Init chrome driver ...")
driver = webdriver.Chrome(service = Service(executable_path= '/usr/local/bin/chromedriver'),options=options)
driver.implicitly_wait(10)
print("chrome driver ok!")

url = "https://www.anbima.com.br/pt_br/informar/consulta-idka.htm"

driver.get(url)
frame = driver.find_element(By.CSS_SELECTOR, "body > div.container.content-full > div > main > div > p > iframe")
driver.switch_to.frame(frame)

download = driver.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(1) > td > div > table > tbody > tr:nth-child(2) > td > form > div > div > fieldset:nth-child(1) > font > input[type=radio]:nth-child(4)")
driver.execute_script("arguments[0].click();", download)

formato = driver.find_element(By.CSS_SELECTOR, "#DivOpcoes > right > fieldset > font > input[type=radio]:nth-child(8)")
driver.execute_script("arguments[0].click();", formato)

dataInput = driver.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(1) > td > div > table > tbody > tr:nth-child(2) > td > form > div > div > fieldset:nth-child(3) > table > tbody > tr > td:nth-child(1) > input.form_data")
dataInput.clear()

if datetime.now().weekday() == 0:#segunda
    data = datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%d%m%Y")
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%Y-%m-%d")]
else:
    data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%d%m%Y")
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")]

dataInput.send_keys(data)

for file in os.listdir(downloadPath):
    os.remove(os.path.join(downloadPath, file))

enviar = driver.find_element(By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(1) > td > div > table > tbody > tr:nth-child(2) > td > form > div > div > fieldset:nth-child(3) > table > tbody > tr > td:nth-child(2) > img")
driver.execute_script("arguments[0].click();", enviar)

time.sleep(2)
wait_for_downloads(downloadPath)
driver.quit()

for file in os.listdir(downloadPath):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(downloadPath, file),  sep = ";", header = 1, encoding='iso-8859-1')
        os.remove(os.path.join(downloadPath, file))
        idka2a = [float(df.loc[df["Índices"] == "IDkA IPCA 2A", "Retorno (% Dia)"].values[0].replace('.','').replace(',','.'))/100]
        d = {"Data":dataSave, "Valor":idka2a}
        finalDf = pd.DataFrame(data=d)
        finalDf.to_csv(os.path.join(downloadPath, "idkaIPCA2A.csv"),  sep = ",", index=False)
