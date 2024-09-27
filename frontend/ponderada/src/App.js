import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [dogePrediction, setDogePrediction] = useState(null);
  const [dogeHistory, setDogeHistory] = useState(null);
  const [logs, setLogs] = useState(null);

  // Estados de erro separados
  const [errorPrediction, setErrorPrediction] = useState(null);
  const [errorHistory, setErrorHistory] = useState(null);
  const [errorLogs, setErrorLogs] = useState(null);

  // Função para obter a previsão do Dogecoin
  const fetchDogePrediction = async () => {
    try {
      console.log(process.env.REACT_APP_API_BASE_URL);
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/doge`);
      setDogePrediction(response.data);
    } catch (error) {
      setErrorPrediction('Erro ao obter a previsão do Dogecoin');
      console.error(error);
    }
  };

  // Função para obter o histórico do Dogecoin
  // Função para obter o histórico do Dogecoin
  const fetchDogeHistory = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/hist_doge`);

      // Adiciona um log para ver o que está sendo retornado pela API
      console.log('Histórico retornado:', response.data);

      // Verifica se a resposta é um objeto, e se ele contém dados válidos
      if (response.data && typeof response.data === 'object') {
        const dataArray = Object.values(response.data); // Converte o objeto em um array de valores
        const lastThreeEntries = dataArray.slice(-3);  // Seleciona os últimos 3 dados
        setDogeHistory(lastThreeEntries);
      } else {
        throw new Error('Histórico retornado não é um objeto válido.');
      }
    } catch (error) {
      setErrorHistory('Erro ao obter o histórico do Dogecoin');
      console.error(error);
    }
  };


  // Função para obter os logs
  const fetchLogs = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/logs`);
      setLogs(response.data);
    } catch (error) {
      setErrorLogs('Erro ao obter os logs');
      console.error(error);
    }
  };

  // useEffect para carregar os dados ao montar o componente
  useEffect(() => {
    fetchDogePrediction();  // Obtém a previsão do Dogecoin
    fetchDogeHistory();     // Obtém o histórico do Dogecoin
    fetchLogs();            // Obtém os logs de consultas
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Dogecoin Prediction</h1>
        
        {/* Seção da previsão */}
        {errorPrediction ? (
          <p style={{ color: 'red' }}>{errorPrediction}</p>
        ) : (
          dogePrediction ? <p>Prediction: {dogePrediction}</p> : <p>Loading Dogecoin prediction...</p>
        )}

        {/* Seção do histórico */}
        <h2>Dogecoin History</h2>
        {errorHistory ? (
          <p style={{ color: 'red' }}>{errorHistory}</p>
        ) : (
          dogeHistory ? <pre>{JSON.stringify(dogeHistory, null, 2)}</pre> : <p>Loading Dogecoin history...</p>
        )}

        {/* Seção dos logs */}
        <h2>Logs</h2>
        {errorLogs ? (
          <p style={{ color: 'red' }}>{errorLogs}</p>
        ) : (
          logs ? <pre>{JSON.stringify(logs, null, 2)}</pre> : <p>Loading logs...</p>
        )}
      </header>
    </div>
  );
}

export default App;
