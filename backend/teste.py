import yfinance as yf

ticker = yf.Ticker("DOGE-USD")
df = ticker.history(period="1y", interval='1d')

print(df.head())  # Verifique os dados retornados
