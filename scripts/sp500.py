import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time
from datetime import date, datetime
from datetime import timedelta
def wait_for_downloads(path):
    print("Waiting for downloads", end="")
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(path)]):
        time.sleep(1)
        print(".", end="")
    print("done!")

downloadPath = os.path.abspath('./../database/sp500')
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

url = "https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC"

driver.get(url)

tabela = driver.find_element(By.CSS_SELECTOR, "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table")
df = pd.read_html(tabela.get_attribute("outerHTML"))[0]
df = df[:-1]
df['Date'] = [datetime.strptime(str(d), "%b %d, %Y") for d in df['Date']]

if datetime.now().weekday() == 0:#segunda
    data = datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%Y-%m-%d")
    dataAnterior = datetime.strftime((datetime.now() - timedelta(days=4)).date(), "%Y-%m-%d")
elif datetime.now().weekday() == 1:#terça
    data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")
    dataAnterior = datetime.strftime((datetime.now() - timedelta(days=4)).date(), "%Y-%m-%d")
else:
    data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")
    dataAnterior = datetime.strftime((datetime.now() - timedelta(days=2)).date(), "%Y-%m-%d")

valorAntigo = df.loc[df['Date'] == dataAnterior, "Adj Close**"].values[0]
valor = df.loc[df['Date'] == data, "Adj Close**"].values[0]
retorno = [float(valor)/float(valorAntigo) - 1]
data = [data]
d = {"Data":data, "Valor":retorno}
finalDf = pd.DataFrame(data=d)

finalDf.to_csv(os.path.join(downloadPath, "sp500.csv"),  sep = ",", index=False)