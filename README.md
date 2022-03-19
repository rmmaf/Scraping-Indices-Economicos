# Scraping-Indices-Economicos
Coleta diária de alguns índices econômicos (guardando tais índices num arquivo CSV)

Tutorial:
    - Apenas execute o arquivo run.sh dentro da pasta scripts:
            sh run.sh
    - O arquivo resultante é o bm_daily.csv dentro da pasta database e ele segue a seguinte estrutura:
            A primeira coluna é a data de coleta e as outras são os respectivos índices.

Requisitos:
    -Bibliotecas Python:
            "pandas" e "selenium"
    -Bibliotecas R:
            "plyr" e "data.table"


Observações: A última atualização do código foi feita em 21/02/2022, há a possibilidade de algum script de coleta não funcionar devido à mudanças no website.