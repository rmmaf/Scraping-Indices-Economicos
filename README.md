# Scraping-Indices-Economicos
Coleta diária de alguns índices econômicos (guardando tais índices num arquivo CSV)

**Tutorial:** <br />
 &ensp;   - Apenas execute o arquivo run.sh dentro da pasta scripts:<br />
   &emsp;       sh run.sh<br />
 &ensp;  - O arquivo resultante é o bm_daily.csv dentro da pasta database e ele segue a seguinte estrutura:<br />
  &emsp;        A primeira coluna é a data de coleta e as outras são os respectivos índices.<br />

**Requisitos:**<br />
  &ensp;   -Bibliotecas Python:<br />
       &emsp;      "pandas" e "selenium"<br />
  &ensp;   -Bibliotecas R:<br />
       &emsp;      "plyr" e "data.table"<br />
  &ensp;   -ChromeDriver e Google Chrome instalado na máquina ([tutorial de como instalar o ChromeDriver](https://chromedriver.chromium.org/getting-started))<br />


 **ATENÇÃO: A última atualização do código foi feita em 21/02/2022, há a possibilidade de algum script de coleta não funcionar devido à mudanças no website.**
