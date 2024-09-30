# Introdução

Esse projeto foi desenvolvido para realizar previsões do valor da criptomoeda Dogecoin (DOGE-USD) utilizando um modelo LSTM, além de permitir consultas ao histórico de preços e salvar logs de consultas. A API integra dados da yfinance para obter preços em tempo real e usa TinyDB para armazenar informações de normalização (valores mínimo e máximo). O sistema prevê preços futuros e recomenda se o usuário deve comprar, vender ou manter o ativo.

Nesse sentido, para ver mais aprofundamente sobre as especificações de como foi tratado a questão da limpeza dos dados, meétricas avaliadas, escolhas dos modelos para as previsões recomendo acessar o notebook `analise.ipynb` e `criacaoModelo.ipynb` localizando em `modulo7\notebooks`.

O modelo escolhido para realizar o treinamento do modelo desse projeto foi o LSTM (Long Short-Term Memory) por algumas razões. A primeira delas é que esse algoritmo é especialmente projetado para lidar com dados sequenciais e temporais, o que é crucial para a análise de séries temporais de preços de criptoativos.  Ao contrário de redes neurais tradicionais, o LSTM possui mecanismos de memória que permitem armazenar informações relevantes por longos períodos, capturando dependências temporais e padrões que podem ser críticos para previsões precisas. Além disso, a capacidade do LSTM de mitigar problemas de desvanecimento do gradiente facilita o aprendizado em sequências mais longas, tornando-o adequado para os dados dinâmicos e muitas vezes não estacionários encontrados no mercado de criptomoedas. 

Para este projeto, foram criadas duas imagens de Docker, juntamente com um arquivo docker-compose.yml para orquestrar a execução do projeto e garantir um bom desempenho em qualquer dispositivo. A separação da execução do projeto em duas imagens de Docker permite a promoção de uma arquitetura limpa, possibilitando que cada componente seja desenvolvido, testado e escalado de forma independente, facilitando a manutenção e atualização sem impactar o outro. Além disso, a utilização do Docker assegura um ambiente de execução consistente em diferentes máquinas, eliminando problemas de "funciona na minha máquina" e promovendo uma melhor integração entre desenvolvedores e equipes de operações. Por fim, o Docker Compose simplifica a configuração e a orquestração dos contêineres, permitindo uma fácil definição e gerenciamento das interações entre os serviços, incluindo rede e volumes. Essa abordagem otimiza a implementação e o escalonamento em ambientes de produção, uma vez que a contêinerização permite a rápida replicação e o gerenciamento eficiente de recursos em nuvem, aumentando a eficácia do sistema, o que pode até reduzir os custos do projeto.

# Execução do projeto

Para executar o projeto, o usuario deve clonar o respositorio do projeto com o seguinte comando: `git clone https://github.com/IsabelleVOliveira/modulo7.git`

Depois de garanit rque o repositorio foi clonado para sua maquina, o usuario deve apenas executar o comando ``docker compose up --build``

Depois disso, ousuario deve acessar o seu navegador e acessar o localhost de seu computador pela URL na porta 7000.

Ao acessar a interface, o usuario deve receber informações sobre as previsões do modelo em relação ao valor da criptomoeda DogeCoin, logo a baixo, informações sobre o que deve fazer no momento sobre compra e venda da moeda e por ultimo, no final da tela se encontram as informações de Logs, dos usuarios do sistema e quais foram suas ações enquanto usava a aplicação.

É importante notar que sempre que a pagina for atualizada, os dados nelas tbm serão, o que garante grande precisão sobre a qualidade dos dados obtidos pe API e maior precisão em relação as previsões do modelo criado.

# Backend e TinyDB

O backend desse projeto é executado no arquivo app.py, encontrado no diretorio `backend`. Este código é uma aplicação desenvolvida com FastAPI que utiliza o TensorFlow e integra a API do Yahoo Finance (yfinance) para obter dados financeiros, processá-los e alimentá-los em um modelo de previsão baseado em LSTM. A aplicação oferece diversas rotas, incluindo previsões de preço para Dogecoin, histórico de preços, previsão de preços para os próximos 7 dias e um endpoint para visualizar logs das consultas realizadas. Além disso, implementa um sistema de normalização de dados para garantir que as previsões sejam precisas, e utiliza o TinyDB para armazenar informações sobre normalização e logs de atividades.

A decisão de não utilizar um data lake neste projeto se baseia em considerações práticas e de eficiência. O backend lida com dados em tempo real, e um banco de dados Tity DB é mais adequado para consultas rápidas e gerenciamento eficiente de dados estruturados. Os dados históricos e previsões de preços dos criptoativos podem ser armazenados de forma organizada no Tity DB, permitindo operações ágeis de leitura e escrita. Além disso, a complexidade e o custo de implementar e manter um data lake, que requer uma infraestrutura robusta para grandes volumes de dados não estruturados, são desnecessários para as demandas deste projeto. Assim, um banco de dados tradicional oferece uma solução mais simples, eficiente e econômica para o sistema de apoio à decisão de investimento.

``@app.get("/doge"):
``
 - Esta rota processa e prevê o preço do Dogecoin (DOGE-USD).
 - Verifica se os dados de normalização estão disponíveis e, se não, busca os dados históricos do yFinance.
 - Carrega um modelo LSTM salvo para prever o próximo valor e usa uma função comparator para dar recomendações de compra, venda ou manutenção com base nas previsões.

`` @app.get("/hist_doge"):
``
 - Retorna o histórico de preços do Dogecoin nos últimos 5 dias, excluindo informações irrelevantes (como Dividends e Stock Splits).
 - Os dados são formatados como JSON antes de serem retornados.


``@app.get("/logs"):
``
 - Carrega e retorna os logs de consultas realizadas, salvando a data e o tipo de consulta atual.

``@app.get("/doge_forecast_7days"):``

 - Faz previsões para os próximos 7 dias do Dogecoin.
 - Similar à rota de previsão única, carrega o modelo e processa os dados, mas gera várias previsões, atualizando as entradas a cada iteração.
 - Retorna as previsões desnormalizadas para os próximos 7 dias.

 Essas rotas permitem que o frontend se comunique com o backend, fornecendo dados em tempo real, históricos e previsões sobre o Dogecoin, além de registrar as consultas realizadas.