import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Desabilita a otimização do TensorFlow em algumas configurações de hardware
from fastapi import FastAPI  # Framework FastAPI para criação da API
from tensorflow import keras  # Keras para trabalhar com modelos de machine learning
import yfinance as yf  # Biblioteca para pegar dados financeiros
from datetime import datetime  # Para registrar timestamps nos logs
import numpy as np  # Para operações numéricas
import pandas as pd  # Para manipulação de dados
import json  # Para ler e gravar arquivos JSON
import uvicorn  # Para rodar o servidor

# Inicializa a aplicação FastAPI
app = FastAPI()

# Função para verificar e criar o arquivo JSON de normalização se ele não existir
def check_and_create_info_json(coin: str):
    if not os.path.exists('info.json'):
        # Busca o histórico da criptomoeda usando a API yfinance
        ticker = yf.Ticker(coin)
        # Você pode ajustar o período e o intervalo conforme necessário
        df = ticker.history(period="1y", interval='1d')  # Histórico de 1 ano, diário

        if df.empty:
            return {"error": "Failed to fetch data from yfinance"}

        # Calcula o valor mínimo e máximo da coluna 'Close' (preço de fechamento)
        min_value = df['Close'].min()
        max_value = df['Close'].max()

        # Criação do arquivo de normalização com valores reais
        info = {
            coin: {
                "min": float(min_value),  # Valor mínimo real do histórico
                "max": float(max_value)   # Valor máximo real do histórico
            }
        }

        # Escreve o arquivo JSON
        with open('info.json', 'w') as outfile:
            json.dump(info, outfile)
        
        return info
    else:
        # Se o arquivo já existir, apenas lê o conteúdo
        with open('info.json', 'r') as openfile:
            info = json.load(openfile)
        return info

# Função para processar os dados da criptomoeda, normalizar e preparar para o modelo LSTM
def process_data(coin: str):
    ticker = yf.Ticker(coin)
    df = ticker.history(period="1d", interval='1m')
    df = df.drop(columns=["Dividends", "Stock Splits", "High", "Low", "Open"])
    df = df.rename(columns={"Close": "Value"})

    # Carrega informações de normalização de um arquivo JSON
    try:
        with open('info.json', 'r') as openfile:
            info = json.load(openfile)
    except FileNotFoundError:
        return {"error": "info.json file not found"}

    # Normaliza os valores da criptomoeda com base em min e max armazenados
    try:
        df["Value"] = (df["Value"] - info[coin]["min"]) / (info[coin]["max"] - info[coin]["min"])
    except KeyError:
        return {"error": f"Normalization info for {coin} not found in info.json"}

    values = df["Value"].values.reshape(-1, 1)

    # Seleciona os últimos 60 minutos para criar a sequência de entrada para o LSTM
    if len(values) < 60:
        return {"error": "Not enough data to create a 60-minute sequence"}
    
    x_p = np.array([values[-60 + i] for i in range(60)]).reshape(1, 60, 1)
    vol = df["Volume"].values[-1]

    return [x_p, vol]


# Função para comparar previsões e dar uma sugestão de compra, venda ou manutenção
def comparator(arr: list, vol: int, recent_volumes: np.array):
    avg_vol = np.mean(recent_volumes)  # Calcula a média do volume recente

    if arr[0] > 0.1 and arr[1] > 0.1 and vol < 0.1 * avg_vol:
        return "Buy"
    elif arr[0] < -0.1 and arr[1] < -0.1 and vol < 0.2 * avg_vol:
        return "Sell"
    else:
        return "Hold"
    
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Endpoint para prever a tendência da Dogecoin
@app.get("/doge")
def predictDOGE():
    # Log da consulta
    try:
        with open('logs.json', 'r') as openfile:
            log = json.load(openfile)
    except FileNotFoundError:
        log = {"typeConsult": [], "date": []}
    
    log["typeConsult"].append("Predicao Dogecoin")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    with open('logs.json', 'w') as outfile:
        json.dump(log, outfile)

    # Carrega o modelo LSTM para Dogecoin
    try:
        model = keras.models.load_model("models/DOGE-USD-LSTM.h5")
        print("Model loaded successfully")
    except OSError as e:
        print("Failed to load model")
        return {"error": "Failed to load model", "message": str(e)}
    
    data = process_data("DOGE-USD")
    if isinstance(data, dict) and "error" in data:
        return data
    
    X, vol = data
    y = model.predict(X)

    # Calcula a diferença entre o valor real e a previsão
    delta = [(X[0][-1][0] - X[0][-2][0]) * 10, (X[0][-1][0] - y[0][0]) * 10]

    return comparator(delta, vol)


# Endpoint para obter o histórico recente de Dogecoin
@app.get("/hist_doge")
def histDOGE():
    # Log da consulta de histórico
    try:
        with open('logs.json', 'r') as openfile:
            log = json.load(openfile)
    except FileNotFoundError:
        log = {"typeConsult": [], "date": []}
    
    log["typeConsult"].append("Historico Dogecoin")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    with open('logs.json', 'w') as outfile:
        json.dump(log, outfile)

    # Obtém os dados históricos de Dogecoin
    ticker = yf.Ticker("DOGE-USD")
    df = ticker.history(period="5d", interval='1m')
    df = df.drop(columns=["Dividends", "Stock Splits", "High", "Low", "Open", "Volume"])
    df = df.rename(columns={"Close": "Value"})
    df.index = df.index.strftime("%d/%m/%Y %H:%M:%S")
    
    j = df.to_json(orient='index')
    parsed = json.loads(j)

    return parsed


# Endpoint para visualizar os logs de consultas
@app.get("/logs")
def logs():
    # Carrega o arquivo de logs
    try:
        with open('logs.json', 'r') as openfile:
            logT = json.load(openfile)
    except FileNotFoundError:
        return {"error": "logs.json file not found"}

    # Atualiza o log com a nova consulta
    logT["typeConsult"].append("Logs")
    logT["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    with open('logs.json', 'w') as outfile:
        json.dump(logT, outfile)

    return logT

if __name__ == "_main_":
    uvicorn.run(app, host="127.0.0.1", port=8000)
