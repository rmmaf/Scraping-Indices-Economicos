options(scipen=999)
library(data.table)
library(plyr)

bm <- fread(file = "./../database/bm_daily.csv")

bdrx <- fread(file = "./../database/global_BDRX/global_BDRX.csv")
ibovespa <- fread(file = "./../database/ibovespa/ibovespa.csv")
ibx <- fread(file = "./../database/IBX/IBX.csv")
ibx50 <- fread(file = "./../database/IBX50/ibx50.csv")
icon <- fread(file = "./../database/icon/icon.csv")
idiv <- fread(file = "./../database/IDIV/IDIV.csv")
idka <- fread(file = "./../database/idkaIPCA/idkaIPCA2A.csv")
ifix <- fread(file = "./../database/IFIX/IFIX.csv")
igc <- fread(file = "./../database/IGC/IGC.csv")
imab_etc <- fread(file = "./../database/IMA-B_IMAB-5_IMAB5+_IRFM_IRFM1+_IRFM1_IMAGERAL/IMA-B_IMAB-5_IMAB5+_IRFM_IRFM1+_IRFM1_IMAGERAL.csv")
ipca <- fread(file = "./../database/ipca/ipca.csv")
ipcaAnual <- fread(file = "./../database/ipca/ipcaAnual.csv")
msci <- fread(file = "./../database/msciWorld/msciWorld.csv")
small <- fread(file = "./../database/SMALL/SMALL.csv")
sp500 <- fread(file = "./../database/sp500/sp500.csv")
cdi <- fread(file = "./../database/CDI/cdi.csv")

data <- sp500$Data
row <- data.table(Data = data, 
                  IBOVESPA = ibovespa$Valor,
                  BDRX = bdrx$Valor,
                  IBRX = ibx$Valor,
                  `IBRX-50` = ibx50$Valor,
                  ICON = icon$Valor,
                  IDIV = idiv$Valor,
                  `IDKA IPCA 2A` = idka$Valor,
                  IFIX = ifix$Valor,
                  IGC = igc$Valor,
                  `IMA-B` = imab_etc$`IMA-B`,
                  `IMA-B 5` = imab_etc$`IMA-B 5`,
                  `IMA-B 5+` = imab_etc$`IMA-B 5+`,
                  `IRF-M` = imab_etc$`IRF-M`,
                  `IMA GERAL EX-C` = imab_etc$`IMA-GERAL ex-C`,
                  CDI = cdi$Valor,
                  `IMA Geral` = imab_etc$`IMA-GERAL`,
                  `IRF-M 1` = imab_etc$`IRF-M 1`,
                  `IRF-M 1+` = imab_etc$`IRF-M 1+`,
                  IPCA = ipca$Valor,
                  `MSCI World` = msci$Valor,
                  `SMALL CAPS` = small$Valor,
                  `S&P 500` = sp500$Valor,
                  `120% DO CDI` = 1.2*(cdi$Valor),
                  `97% DO IMA B` = 0.97*(imab_etc$`IMA-B`),
                  `Índice IPCA +5,0%` = ipca$Valor + 0.05*ipcaAnual$Valor,
                  `Índice IPCA +5,41%` = ipca$Valor + 0.0541*ipcaAnual$Valor,
                  `Índice IPCA +5,870%` = ipca$Valor + 0.0587*ipcaAnual$Valor,
                  `IPCA + 10,5%` = ipca$Valor + 0.105*ipcaAnual$Valor,
                  `IPCA + 11,90%` = ipca$Valor + 0.119*ipcaAnual$Valor,
                  `IPCA + 6` = ipca$Valor + 0.06*ipcaAnual$Valor,
                  `IPCA + 7,5%` = ipca$Valor + 0.075*ipcaAnual$Valor,
                  `IPCA + 7%` = ipca$Valor + 0.07*ipcaAnual$Valor,
                  `IPCA + 8,5%` = ipca$Valor + 0.085*ipcaAnual$Valor,
                  `IPCA + 8%` = ipca$Valor + 0.08*ipcaAnual$Valor,
                  `IPCA + 9%` = ipca$Valor + 0.09*ipcaAnual$Valor)

finalDf <- rbind.fill(bm, row)
fwrite(finalDf, "./../database/bm_daily.csv")