import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './History.css';

const History = () => {
  const [priceHistory, setPriceHistory] = useState([]); // Inicializa como um array
  const [dogePrediction, setDogePrediction] = useState(''); // Inicializa como uma string vazia
  const [error, setError] = useState('');

  // Função para obter a previsão do Dogecoin da API
  const fetchDogePrediction = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/doge`);
      setDogePrediction(response.data); // Atualiza para o formato correto do retorno
    } catch (error) {
      setError('Erro ao obter a previsão do Dogecoin');
      console.error(error);
    }
  };

  useEffect(() => {
    // fetchPriceHistory();
    fetchDogePrediction();
  }, []); // Chamado uma vez ao montar o componente

  return (
    <div className="history-container">
      <div className="prediction-result">
        <h2>Previsão do Dogecoin</h2>
        <p>Previsão: {dogePrediction}</p>
      </div>
    </div>
  );
};

export default History;
