import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from datetime import timedelta
def wait_for_downloads(path):
    print("Waiting for downloads", end="")
    while any([filename.endswith(".crdownload") for filename in 
               os.listdir(path)]):
        time.sleep(1)
        print(".", end="")
    print("done!")

downloadPath = os.path.abspath('./../database/CDI')
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

url = "https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries"

driver.get(url)

try:
    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

    alert = driver.switch_to.alert
    alert.accept()
    print("alert accepted")
except TimeoutException:
    print("no alert")

driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "#tabLCS > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(12) > td"))
frame = driver.find_element(By.CSS_SELECTOR, "#iCorpo")
driver.switch_to.frame(frame)
select = Select(driver.find_element(By.CSS_SELECTOR, "body > center > form > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(6) > select"))
select.select_by_visible_text("Cetip")
classificacao = driver.find_element(By.CSS_SELECTOR, "body > center > form > table:nth-child(1) > tbody > tr:nth-child(5) > td:nth-child(2) > input[type=checkbox]")
driver.execute_script("arguments[0].click();", classificacao)
driver.find_element(By.CSS_SELECTOR, "#txtPesquisa").send_keys("CDI")
nomeSerie = driver.find_element(By.CSS_SELECTOR, "#chkNome")
driver.execute_script("arguments[0].click();", nomeSerie)
pesquisar = driver.find_element(By.CSS_SELECTOR, "body > center > form > input.botao")
driver.execute_script("arguments[0].click();", pesquisar)

driver.switch_to.default_content()
marcar = driver.find_element(By.CSS_SELECTOR, "#botaoMarcar > input")
driver.execute_script("arguments[0].click();", marcar)

consultar = driver.find_element(By.CSS_SELECTOR, "body > form > center > span > center > table > tbody > tr > td:nth-child(4) > div > input")
driver.execute_script("arguments[0].click();", consultar)

valores = driver.find_element(By.CSS_SELECTOR, "body > center > form > div.cen > input:nth-child(2)")
driver.execute_script("arguments[0].click();", valores)

for file in os.listdir(downloadPath):
    os.remove(os.path.join(downloadPath, file))

download = driver.find_element(By.CSS_SELECTOR, "#seriesSelecionadas > tbody > tr:nth-child(1) > td:nth-child(2) > a")
driver.execute_script("arguments[0].click();", download)

time.sleep(5)
wait_for_downloads(downloadPath)
time.sleep(2)
driver.quit()

if datetime.now().weekday() == 0:#segunda
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%Y-%m-%d")]
elif datetime.now().weekday() == 6:#domingo
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=2)).date(), "%Y-%m-%d")]
else:
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")]

for file in os.listdir(downloadPath):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(downloadPath, file),  sep = ";", encoding='iso-8859-1', skipfooter=1, decimal=",", engine="python")
        os.remove(os.path.join(downloadPath, file))
        valor = [float(df.iloc[-1,1])/100]
        data = dataSave
        d = {"Data":data, "Valor":valor}
        finalDf = pd.DataFrame(data=d)
        finalDf.to_csv(os.path.join(downloadPath, "cdi.csv"),  sep = ",", index=False)
        
