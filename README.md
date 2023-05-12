# bank-system
Um sistema bancário para a matéria de gerência de Configuração e Mudanças.


## Requisitos
- python 3.10
- pipenv
- docker

## Executando em desenvolvimeto
```bash
    docker compose up -d # Levanta o container com o banco
    pipenv shell # Entra no nas variaveis de ambiente
    pipenv sync # Instala os pacotes necessários pro projeto
    python manage.py migrate # Executa as migrations
    python manage.py runserver # Executa o projeto na prota 8000
```