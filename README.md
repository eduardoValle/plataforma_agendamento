# plataforma_agendamento
Plataforma de agendamento de serviços


### Ativar ambiente virtual

`.\venv\Scripts\activate`


### Subir serviço do Celey

`celery -A plataforma_agendamento worker -l info -P solo`



### Subir container do RabbitMQ

`docker run -d -p 5672:5672 rabbitmq`



-----
### Rodar as migrations

`py manage.py migrate`



### Rodar o projeto

`py manage.py runserver`



### Criar 'Super user' para a área ADM

`py manage.py createsuperuser`



### Criar novo módulo

`py manage.py startapp login`



-----

# Poetry

### Crie um básico pyproject.tomlcom djangocomo dependência:

`poetry init --no-interaction --dependency django`



### Crie venv com todas as dependências necessárias:

`poetry install`



### Inicie seu projeto de demonstração:

`poetry run django-admin startproject plataforma-agendamento`