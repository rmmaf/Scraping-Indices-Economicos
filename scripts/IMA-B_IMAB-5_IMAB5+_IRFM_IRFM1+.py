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

downloadPath = os.path.abspath('./../database/IMA-B_IMAB-5_IMAB5+_IRFM_IRFM1+_IRFM1_IMAGERAL')
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

url = "https://www.anbima.com.br/pt_br/informar/ima-resultados-diarios.htm"

driver.get(url)
frame = driver.find_element(By.CSS_SELECTOR, "body > div.container.content-full > div > main > div > p > iframe")
driver.switch_to.frame(frame)

download = driver.find_element(By.CSS_SELECTOR, "#cinza50 > form > div > fieldset:nth-child(2) > font > input[type=radio]:nth-child(4)")
driver.execute_script("arguments[0].click();", download)

formato = driver.find_element(By.CSS_SELECTOR, "#DivOpcoes > right > fieldset > font > input[type=radio]:nth-child(8)")
driver.execute_script("arguments[0].click();", formato)

dataInput = driver.find_element(By.CSS_SELECTOR, "#cinza50 > form > div > fieldset:nth-child(8) > table > tbody > tr > td > input.form_data")
dataInput.clear()

if datetime.now().weekday() == 0:#segunda
    data = datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%d%m%Y")
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%Y-%m-%d")]
elif datetime.now().weekday() == 6:#domingo
    data = datetime.strftime((datetime.now() - timedelta(days=2)).date(), "%d%m%Y")
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=2)).date(), "%Y-%m-%d")]
else:
    data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%d%m%Y")
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")]

dataInput.send_keys(data)

for file in os.listdir(downloadPath):
    os.remove(os.path.join(downloadPath, file))

enviar = driver.find_element(By.CSS_SELECTOR, "#cinza50 > form > div > table > tbody > tr > td > img")
driver.execute_script("arguments[0].click();", enviar)

time.sleep(2)
wait_for_downloads(downloadPath)
driver.quit()

for file in os.listdir(downloadPath):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(downloadPath, file),  sep = ";", header = 1, encoding='iso-8859-1')
        os.remove(os.path.join(downloadPath, file))
        imab = [float(df.loc[df["Índice"] == "IMA-B", 'Variação Diária (%)'].values[0].replace('.','').replace(',','.'))/100]
        imab5 = [float(df.loc[df["Índice"] == "IMA-B 5", 'Variação Diária (%)'].values[0].replace('.','').replace(',','.'))/100]
        imab5plus = [float(df.loc[df["Índice"] == "IMA-B 5+", 'Variação Diária (%)'].values[0].replace('.','').replace(',','.'))/100]
        irfm = [float(df.loc[df["Índice"] == "IRF-M", 'Variação Diária (%)'].values[0].replace('.','').replace(',','.'))/100]
        irfm1plus = [float(df.loc[df["Índice"] == "IRF-M 1+", 'Variação Diária (%)'].values[0].replace('.','').replace(',','.'))/100]
        irfm1 = [float(df.loc[df["Índice"] == "IRF-M 1", 'Variação Diária (%)'].values[0].replace('.','').replace(',','.'))/100]
        imaGeral = [float(df.loc[df["Índice"] == "IMA-GERAL", 'Variação Diária (%)'].values[0].replace('.','').replace(',','.'))/100]
        imaGeralExC = [float(df.loc[df["Índice"] == "IMA-GERAL ex-C", 'Variação Diária (%)'].values[0].replace('.','').replace(',','.'))/100]
        d = {"Data":dataSave, "IMA-B":imab, "IMA-B 5":imab5, "IMA-B 5+":imab5plus, "IRF-M":irfm, "IRF-M 1+":irfm1plus, "IRF-M 1":irfm1, "IMA-GERAL":imaGeral, "IMA-GERAL ex-C":imaGeralExC}
        finalDf = pd.DataFrame(data=d)
        finalDf.to_csv(os.path.join(downloadPath, "IMA-B_IMAB-5_IMAB5+_IRFM_IRFM1+_IRFM1_IMAGERAL.csv"),  sep = ",", index=False)