import sqlite3
from cripto.dataaccess import *
from config import API_KEY

def transacMon(): #Función de transacciones de Moneda: cálculo de cantidades
    dbManager = DBManager()
    query ="SELECT * FROM movimientos WHERE 1==1"
    parametros=[]
    movimientos = dbManager.consultaSQL(query,parametros)

    resultados={}    
    monedas=["ADA","BCH","BNB","BSV","BTC","EOS","ETH","EUR","LTC","TRX","USDT","XLM","XRP"]
    InvMON={"ADA":0,"BCH":0,"BNB":0,"BSV":0,"BTC":0,"EOS":0,"ETH":0,"EUR":0,"LTC":0,"TRX":0,"USDT":0,"XLM":0,"XRP":0}
    GasMON={"ADA":0,"BCH":0,"BNB":0,"BSV":0,"BTC":0,"EOS":0,"ETH":0,"EUR":0,"LTC":0,"TRX":0,"USDT":0,"XLM":0,"XRP":0}
    SalMON={"ADA":0,"BCH":0,"BNB":0,"BSV":0,"BTC":0,"EOS":0,"ETH":0,"EUR":0,"LTC":0,"TRX":0,"USDT":0,"XLM":0,"XRP":0}
    ValActMON={"ADA":0,"BCH":0,"BNB":0,"BSV":0,"BTC":0,"EOS":0,"ETH":0,"EUR":0,"LTC":0,"TRX":0,"USDT":0,"XLM":0,"XRP":0}
                
    for m,n in enumerate(monedas):
        for f in movimientos:
            if f["fromQ"]==monedas[m]:
                a=f["fromQ"]
                InvMON[a]+=f["cantidadFromQ"] #Inversión en la moneda (compra de moneda)
        
            elif f["toQ"]==monedas[m]:
                a=f["toQ"]
                GasMON[a]+=f["cantidadToQ"] #Gasto en la moneda (venta de moneda)
                
    for m in monedas:        
        SalMON[m]+= (GasMON[m]-InvMON[m]) #Saldo = Inversión - Gasto

    resultados["SalMON"]=SalMON #array asociativo para devolver varios resultados
    resultados["monedas"]=monedas
    resultados["movimientos"]=movimientos
    resultados["ValActMON"]=ValActMON
    resultados["InvMON"]=InvMON
    resultados["GasMON"]=GasMON
    
    return resultados

def llamaApi(cantidadFromQ, fromQ, toQ): #Función de conversiones de moneda a través de API
    import requests
    api_key=API_KEY
    url="http://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
    resultado = requests.get(url.format(cantidadFromQ, fromQ, toQ, API_KEY)) 
    if resultado.status_code==200:
        resultadoJSON= resultado.json()   
        cantidadToQ=resultadoJSON["data"]["quote"][toQ]["price"]  
        return cantidadToQ
    else:
        return False