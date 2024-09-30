import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Prediction.css';

const Prediction = () => {
  const [dogePrediction, setDogePrediction] = useState(null);
  const [errorPrediction, setErrorPrediction] = useState('');

  // Função para obter a previsão do Dogecoin
  const fetchDogePrediction = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/doge`);
      setDogePrediction(response.data);
    } catch (error) {
      setErrorPrediction('Erro ao obter a previsão do Dogecoin');
      console.error(error);
    }
  };

  useEffect(() => {
    fetchDogePrediction();
  }, []);

  return (
    <div className="prediction-container">
      <h2>Previsão do Dogecoin</h2>
      {errorPrediction && <p className="error">{errorPrediction}</p>}
      {dogePrediction && (
        <div className="prediction-info">
          <p>Previsão: {dogePrediction.prediction}</p>
          <p>Recomendação: {dogePrediction.recommendation}</p>
        </div>
      )}
    </div>
  );
};

export default Prediction;
