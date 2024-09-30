import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

const Forecast = () => {
  const [forecast, setForecast] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/doge_forecast_7days')
      .then((response) => response.json())
      .then((data) => setForecast(data.forecast_7_days))
      .catch((error) => console.error('Erro ao obter previsões:', error));
  }, []);

  const forecastData = {
    labels: Array.from({ length: 7 }, (_, i) => `Day ${i + 1}`),
    datasets: [
      {
        label: 'Dogecoin Forecast',
        data: forecast,
        fill: false,
        backgroundColor: 'rgba(75,192,192,1)',
        borderColor: 'rgba(75,192,192,1)',
      },
    ],
  };

  return (
    <div>
      <h2>Previsão para os próximos 7 dias</h2>
      {forecast.length > 0 ? <Line data={forecastData} /> : <p>Carregando previsões...</p>}
    </div>
  );
};

export default Forecast;
