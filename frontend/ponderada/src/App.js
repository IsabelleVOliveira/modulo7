import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [dogePrediction, setDogePrediction] = useState(null);
  const [dogeHistory, setDogeHistory] = useState(null);
  const [logs, setLogs] = useState(null);

  // Função para obter a previsão do Dogecoin
  const fetchDogePrediction = async () => {
    try {
      const response = await axios.get('http://localhost:8000/doge');  // Alterar para o URL correto do seu backend
      setDogePrediction(response.data);
    } catch (error) {
      console.error('Erro ao obter a previsão do Dogecoin:', error);
    }
  };

  // Função para obter o histórico do Dogecoin
  const fetchDogeHistory = async () => {
    try {
      const response = await axios.get('http://localhost:8000/hist_doge');
      setDogeHistory(response.data);
    } catch (error) {
      console.error('Erro ao obter o histórico do Dogecoin:', error);
    }
  };

  // Função para obter os logs
  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://localhost:8000/logs');
      setLogs(response.data);
    } catch (error) {
      console.error('Erro ao obter os logs:', error);
    }
  };

  useEffect(() => {
    fetchDogePrediction();  // Obtém a previsão do Dogecoin
    fetchDogeHistory();     // Obtém o histórico do Dogecoin
    fetchLogs();            // Obtém os logs de consultas
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Dogecoin Prediction</h1>
        {dogePrediction ? (
          <p>Prediction: {dogePrediction}</p>
        ) : (
          <p>Loading Dogecoin prediction...</p>
        )}

        <h2>Dogecoin History</h2>
        {dogeHistory ? (
          <pre>{JSON.stringify(dogeHistory, null, 2)}</pre>
        ) : (
          <p>Loading Dogecoin history...</p>
        )}

        <h2>Logs</h2>
        {logs ? (
          <pre>{JSON.stringify(logs, null, 2)}</pre>
        ) : (
          <p>Loading logs...</p>
        )}
      </header>
    </div>
  );
}

export default App;
