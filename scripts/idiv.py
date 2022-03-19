from numpy import NaN
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time
from selenium.webdriver.support.ui import Select
from datetime import datetime
from datetime import timedelta
def wait_for_downloads(path):
    print("Waiting for downloads", end="")
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(path)]):
        time.sleep(1)
        print(".", end="")
    print("done!")

downloadPath = os.path.abspath('./../database/IDIV')
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

url = "https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/indice-dividendos-idiv-estatisticas-historicas.htm"

driver.get(url)

frame = driver.find_element(By.CSS_SELECTOR, "#bvmf_iframe")
driver.switch_to.frame(frame)

anoAtual = datetime.now().year
selecaoAno = Select(driver.find_element(By.CSS_SELECTOR, "#selectYear"))
selecaoAno.select_by_value(str(anoAtual))
baixar = driver.find_element(By.CSS_SELECTOR, "#divContainerIframeB3 > div > div.col-lg-9.col-12.order-2.order-lg-1 > form > div:nth-child(5) > div > div > div > div > div.list-avatar-row > div.content > p > a")
driver.execute_script("arguments[0].click();", baixar)
time.sleep(3)
wait_for_downloads(downloadPath)

driver.quit()
if(os.path.exists(os.path.join(downloadPath, "IDIV.csv"))):
    os.remove(os.path.join(downloadPath, "IDIV.csv"))

for file in os.listdir(downloadPath):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(downloadPath, file),  sep = ";", header = 1, skip_blank_lines=True, encoding='latin3', nrows=31)
        os.remove(os.path.join(downloadPath, file))
        meses = {1:"Jan",  2:"Fev", 3:"Mar", 4:"Abr", 5:"Mai", 6:"Jun", 7:"Jul", 8:"Ago", 9:"Set", 10:"Out", 11:"Nov", 12:"Dez"}
        if datetime.now().weekday() == 0:#segunda
            dia = (datetime.now() - timedelta(days=3)).day
            mes = (datetime.now() - timedelta(days=3)).month
            diaAnterior = (datetime.now() - timedelta(days=4)).day
            mesAnterior = (datetime.now() - timedelta(days=4)).month
            data = datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%Y-%m-%d")
        elif datetime.now().weekday() == 1:#terça
            dia = (datetime.now() - timedelta(days=1)).day
            mes = (datetime.now() - timedelta(days=1)).month
            diaAnterior = (datetime.now() - timedelta(days=4)).day
            mesAnterior = (datetime.now() - timedelta(days=4)).month
            data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")
        else:
            dia = (datetime.now() - timedelta(days=1)).day
            mes = (datetime.now() - timedelta(days=1)).month
            diaAnterior = (datetime.now() - timedelta(days=2)).day
            mesAnterior = (datetime.now() - timedelta(days=2)).month
            data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")
        mesCol = meses[mes]
        valor = str(df.loc[df['Dia'] == dia, mesCol].values[0])
        mes = (datetime.now() - timedelta(days=1)).month
        valor = str.replace(valor, ".", "")
        valor = str.replace(valor, ",", ".")
        valor = float(valor)
        mesCol = meses[mesAnterior]
        valorAntes = str(df.loc[df['Dia'] == diaAnterior, mesCol].values[0])
        valorAntes = str.replace(valorAntes, ".", "")
        valorAntes = str.replace(valorAntes, ",", ".")
        valorAntes = float(valorAntes)
        retorno = [valor/valorAntes - 1]
        data = [data]
        d = {"Data":data, "Valor":retorno}
        finalDf = pd.DataFrame(data=d)
        finalDf.to_csv(os.path.join(downloadPath, "IDIV.csv"),  sep = ",", index=False)
        