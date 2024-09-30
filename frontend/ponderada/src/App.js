import React from 'react';
import Forecast from './components/Forecast';
import History from './components/History';
import Logs from './components/Logs';
import './App.css';

function App() {
  return (
    <div className="App">
      <h1>Dogecoin Forecast Dashboard</h1>
      <Forecast />
      <History />
      <Logs />
    </div>
  );
}

export default App;
