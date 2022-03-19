import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
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

downloadPath = os.path.abspath('./../database/IBX50')
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

url = "https://br.investing.com/indices/brazil-index-50-historical-data"

driver.get(url)
try:
    cookies = driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
    driver.execute_script("arguments[0].click();", cookies)
except NoSuchElementException:
    print("Sem cookies")
tabela = driver.find_element(By.CSS_SELECTOR, "#curr_table")

df = pd.read_html(tabela.get_attribute("outerHTML"))[0]
driver.quit()
if datetime.now().weekday() == 0:#segunda
    data = datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%d.%m.%Y")
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%Y-%m-%d")]
else:
    data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%d.%m.%Y")
    dataSave = [datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")]

valor = df.loc[df["Data"] == data, "Var%"].values[0]
valor = float(str.replace(str.replace(valor, ".", ""), ",", ".").strip("%"))/100

d = {"Data":dataSave, "Valor":valor}
finalDf = pd.DataFrame(data=d)
finalDf.to_csv(os.path.join(downloadPath, "ibx50.csv"),  sep = ",", index=False)