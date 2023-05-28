# bank-system
Um sistema bancário para a matéria de gerência de Configuração e Mudanças.


## Requisitos
- python 3.10
- pipenv
- docker

## Executando em desenvolvimeto
```bash
    docker compose up -d # Levanta o container com o banco
    cp .env.development .env # Copia o .env
    pipenv shell # Entra no nas variaveis de ambiente
    pipenv sync # Instala os pacotes necessários pro projeto
    python manage.py migrate # Executa as migrations
    python manage.py runserver # Executa o projeto na prota 8000
```

## Árvore com histórico do projeto
![RabbitMQ first version](/resources/git-tree.png)

Na figura é possivel verificar o histórico de commits e branches do projeto. Na árvore vemos em baixo o início do projeto com o desenvolvimento de features e merges na develop. Logo apos vemos merges na develop até a criação da primeira release candidate 1.1. Com isso foram feitas correções na release candidate gerando novas versões e depois o merge na main dando origem a primeira primeira release em produção a tag rel-1.3. Com foi feita uma hotfix e mergeada na main e também mergeada na release e develop com ajudas de branches auxiliares para resolver conflitos em paralelo quando nossas features são adicionadas. 