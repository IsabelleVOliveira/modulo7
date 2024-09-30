import React, { useEffect, useState } from 'react';
import axios from 'axios'; // Importa a biblioteca axios

const Logs = () => {
  const [logs, setLogs] = useState({ typeConsult: [], date: [] }); // Inicializa o estado para os logs
  const [error, setError] = useState(''); // Adiciona estado para gerenciar erros

  // Função para obter os logs da API
  const fetchLogs = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/logs`); // Faz a requisição com axios
      setLogs(response.data); // Atualiza o estado com os dados retornados
    } catch (error) {
      setError('Erro ao obter logs'); // Atualiza o estado de erro
      console.error('Erro ao obter logs:', error); // Loga o erro no console
    }
  };

  useEffect(() => {
    fetchLogs(); // Chama a função para buscar os logs ao montar o componente
  }, []); // Chamado uma vez ao montar o componente

  return (
    <div>
      <h2>Logs de Consultas</h2>
      {error ? ( // Verifica se há um erro
        <p className="error">{error}</p> // Exibe a mensagem de erro
      ) : (
        <table>
          <thead>
            <tr>
              <th>Tipo de Consulta</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {logs.typeConsult.map((consult, index) => (
              <tr key={index}>
                <td>{consult}</td>
                <td>{logs.date[index]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Logs;
