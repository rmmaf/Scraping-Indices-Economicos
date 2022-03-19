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

downloadPath = os.path.abspath('./../database/ipca')
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

url = "http://www.ipeadata.gov.br/Default.aspx"
driver.get(url)
driver.find_element(By.CSS_SELECTOR, "#busca").send_keys("ipca")
pesquisar = driver.find_element(By.CSS_SELECTOR, "#barra_superior_azul > table > tbody > tr > td:nth-child(12) > table:nth-child(1) > tbody > tr > td:nth-child(3) > img")
driver.execute_script("arguments[0].click();", pesquisar)
frame = driver.find_element(By.CSS_SELECTOR, "#conteudo")
driver.switch_to.frame(frame)
ipcaGeral = driver.find_element(By.LINK_TEXT, "IPCA - geral - taxa de variação")
driver.execute_script("arguments[0].click();", ipcaGeral)

tabela = driver.find_element(By.CSS_SELECTOR, "#grd")
df = pd.read_html(tabela.get_attribute("outerHTML"), decimal=",", thousands=".")[0]

driver.quit()
i_m = float(df.iloc[-1,1])
i_d = (1+i_m)**(1/30) -1

if datetime.now().weekday() == 0:#segunda
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%Y-%m-%d")]
else:
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")]
d = {"Data":dataSave, "Valor":i_d}
finalDf = pd.DataFrame(data=d)
finalDf.to_csv(os.path.join(downloadPath, "ipca.csv"),  sep = ",", index=False)