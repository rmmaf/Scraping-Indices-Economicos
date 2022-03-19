import pandas as pd
from datetime import datetime
from datetime import timedelta
import os
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

writePath = os.path.abspath('./../database/IBX')
os.makedirs(writePath, mode=0o777, exist_ok=True)  # create dir if it not exist

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&datatype=csv&symbol=IBXX.SA&apikey=9271MV28TR4HK23C'

df = pd.read_csv(url)

if datetime.now().weekday() == 0:#segunda
    data = datetime.strftime((datetime.now() - timedelta(days=3)).date(), "%Y-%m-%d")
    dataAnterior = datetime.strftime((datetime.now() - timedelta(days=4)).date(), "%Y-%m-%d")
elif datetime.now().weekday() == 1:#terça
    data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")
    dataAnterior = datetime.strftime((datetime.now() - timedelta(days=4)).date(), "%Y-%m-%d")
else:
    data = datetime.strftime((datetime.now() - timedelta(days=1)).date(), "%Y-%m-%d")
    dataAnterior = datetime.strftime((datetime.now() - timedelta(days=2)).date(), "%Y-%m-%d")

valorAntigo = df.loc[df['timestamp'] == dataAnterior, "close"].values[0]
valor = df.loc[df['timestamp'] == data, "close"].values[0]
retorno = [valor/valorAntigo - 1]
data = [data]
d = {"Data":data, "Valor":retorno}
finalDf = pd.DataFrame(data=d)
finalDf.to_csv(os.path.join(writePath, "IBX.csv"),  sep = ",", index=False)