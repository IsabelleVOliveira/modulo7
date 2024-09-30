# Introdução

Esse projeto foi desenvolvido para prever se o usuario deve comprar DogeCoin, manter sua posse da moeda ou comprar DOgecoin com base no historico de dados dos ultimos 60 minutos para ser usada no modelo LSTM. Por isso, foi desenvolvido um frontend que é atualizado sempre que acessado com uma nova.

Nesse sentido, para ver mais aprofundamente sobre as especificações de como foi tratado a questão da limpeza dos dados, meétricas avaliadas, escolhas dos modelos para as previsões recomendo acessar o notebook `main.ipynb` localizando em `MODULO-7/atividade_1/src/main.ipynb`.

Sendo assim, os modelos escolhidos para esse projetos forma: GARCH e o Arima. Cabe auqi uma breve explicação de cada um dos modelos escolhidos. Nesse sentido, o GARCH foi escolhido por referências acâdemicas na área de ecnomia, pois ele é indicado para modelar a volatilidade variando no tempo de determiandas séries, assim podemos ter acesso a volatibilidade do Bitcoin pelo tempo e indicar para quando se deve comprar ou não. Já o Arima, foi utilizado para avaliar os valores futuros que o Bitcoin pode assumir para que se pudesse ter valores futuros a indicar para pessoa comprar.