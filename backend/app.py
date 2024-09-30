import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from tensorflow import keras
import yfinance as yf
from datetime import datetime
import numpy as np
import pandas as pd
import json
import uvicorn
import pickle
from tinydb import TinyDB, Query
from fastapi.middleware.cors import CORSMiddleware

# Inicializa o TinyDB com o arquivo 'info_db.json'
db = TinyDB('info_db.json')

# Inicializa a aplicação FastAPI
app = FastAPI()

# Habilita o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://172.22.208.1:3000", "http://localhost:3000", "http://172.22.208.1:7000", "http://localhost:7000"],  # Endereço do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Função para verificar e criar os dados de normalização no TinyDB se não existirem
def check_and_create_info_db(coin: str):
    Coin = Query()
    result = db.search(Coin.name == coin)

    if not result:
        print(f"{coin} não encontrado no banco, buscando dados do yfinance para criar...")
        ticker = yf.Ticker(coin)
        df = ticker.history(period="1y", interval='1d')

        if df.empty:
            print("Erro: Nenhum dado retornado pelo yfinance")
            return {"error": "Failed to fetch data from yfinance"}
        
        print(f"Dados retornados do yfinance:\n{df.head()}")

        min_value = df['Close'].min()
        max_value = df['Close'].max()

        print(f"Valor mínimo: {min_value}, Valor máximo: {max_value}")

        db.insert({
            'name': coin,
            'min': float(min_value),
            'max': float(max_value)
        })
        print(f"Dados de normalização para {coin} inseridos com sucesso no TinyDB.")
        
        return {"min": float(min_value), "max": float(max_value)}

    else:
        print(f"Dados de normalização para {coin} já existem no TinyDB.")
        return result[0]

# Função para processar os dados da criptomoeda, normalizar e preparar para o modelo LSTM
def process_data(coin: str):
    ticker = yf.Ticker(coin)
    
    # Tenta primeiro com 7 dias
    df = ticker.history(period="7d", interval='1m')

    # Se os dados estiverem vazios, tenta com 5 dias
    if df.empty:
        print("Error: No data for 7 days. Trying 5 days...")
        df = ticker.history(period="5d", interval='1m')

    # Se ainda estiver vazio, tenta com 1 dia
    if df.empty:
        print("Error: No data for 5 days. Trying 1 day...")
        df = ticker.history(period="1d", interval='1m')

    # Se os dados ainda estiverem vazios, retorna um erro
    if df.empty:
        print(f"Error: No data fetched from yfinance for {coin}")
        return {"error": f"No data fetched from yfinance for {coin}"}

    # Verifica se há dados suficientes (60 minutos)
    if len(df) < 60:
        print(f"Error: Not enough data fetched for {coin}. Only {len(df)} minutes available.")
        return {"error": f"Not enough data fetched for {coin}. Only {len(df)} minutes available."}

    # Processa os dados normalmente após garantir que eles foram obtidos
    df = df.drop(columns=["Dividends", "Stock Splits", "High", "Low", "Open"])
    df = df.rename(columns={"Close": "Value"})

    normalization_info = check_and_create_info_db(coin)
    
    if isinstance(normalization_info, dict) and "error" in normalization_info:
        print(f"Error: {normalization_info['error']}")
        return normalization_info

    try:
        df["Value"] = (df["Value"] - normalization_info["min"]) / (normalization_info["max"] - normalization_info["min"])
    except KeyError:
        print(f"Error: KeyError during normalization for {coin}")
        return {"error": f"Normalization info for {coin} not found in TinyDB"}

    values = df["Value"].values.reshape(-1, 1)

    # Verifica novamente se existem dados suficientes para criar a sequência de 60 minutos
    if len(values) < 60:
        print("Error: Not enough data to create a 60-minute sequence")
        return {"error": "Not enough data to create a 60-minute sequence"}

    # Cria a sequência de 60 minutos
    x_p = np.array([values[-60 + i] for i in range(60)]).reshape(1, 60, 1)
    vol = df["Volume"].values[-1]

    # Obtém os volumes recentes para passar ao comparator
    recent_volumes = df["Volume"].values[-60:]  # Últimos 60 minutos de volume

    return [x_p, vol, recent_volumes]


# Função para comparar previsões e dar uma sugestão de compra, venda ou manutenção
def comparator(arr: list, vol: int, recent_volumes: np.array):
    avg_vol = np.mean(recent_volumes)

    if arr[0] > 0.1 and arr[1] > 0.1 and vol < 0.1 * avg_vol:
        return "Buy"
    elif arr[0] < -0.1 and arr[1] < -0.1 and vol < 0.2 * avg_vol:
        return "Sell"
    else:
        return "Hold"

# Função para carregar ou inicializar o arquivo de logs
def load_logs():
    try:
        with open('logs.json', 'r') as openfile:
            log = json.load(openfile)
    except (FileNotFoundError, json.JSONDecodeError):
        log = {"typeConsult": [], "date": []}
        with open('logs.json', 'w') as outfile:
            json.dump(log, outfile)
    return log

# Função para salvar logs
def save_logs(log):
    with open('logs.json', 'w') as outfile:
        json.dump(log, outfile)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/doge")
def predictDOGE():
    normalization_info = check_and_create_info_db("DOGE-USD")
    
    if isinstance(normalization_info, dict) and "error" in normalization_info:
        return normalization_info

    log = load_logs()

    log["typeConsult"].append("Predicao Dogecoin")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    save_logs(log)

    model_path = "model_lstm.pkl"

    try:
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        print("Modelo carregado com sucesso")
    except OSError as e:
        return {"error": "Falha ao carregar o modelo", "message": str(e)}

    try:
        data = process_data("DOGE-USD")
        if isinstance(data, dict) and "error" in data:
            return data
    except Exception as e:
        return {"error": "Falha no processamento de dados", "message": str(e)}

    try:
        X, vol, recent_volumes = data
        y = model.predict(X)
        delta = [(X[0][-1][0] - X[0][-2][0]) * 10, (X[0][-1][0] - y[0][0]) * 10]
    except Exception as e:
        return {"error": "Falha na previsão", "message": str(e)}

    try:
        return comparator(delta, vol, recent_volumes)
    except Exception as e:
        return {"error": "Falha na comparação", "message": str(e)}

@app.get("/hist_doge")
def histDOGE():
    log = load_logs()

    log["typeConsult"].append("Historico Dogecoin")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    save_logs(log)

    ticker = yf.Ticker("DOGE-USD")
    df = ticker.history(period="5d", interval='1m')
    df = df.drop(columns=["Dividends", "Stock Splits", "High", "Low", "Open", "Volume"])
    df = df.rename(columns={"Close": "Value"})
    df.index = df.index.strftime("%d/%m/%Y %H:%M:%S")
    
    j = df.to_json(orient='index')
    parsed = json.loads(j)

    return parsed

@app.get("/logs")
def logs():
    log = load_logs()
    
    log["typeConsult"].append("Logs")
    log["date"].append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    save_logs(log)

    return log

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
