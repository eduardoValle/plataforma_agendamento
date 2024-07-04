# Plataforma de Agendamento

Desafio de criar uma aplicação backend para uma empresa fictícia que gerencia uma plataforma de agendamento de serviços.


## Dados importantes
```
-> O projeto já possúi um banco de dados sqlite integrado, portanto não precisa se preocupar em configuar um!
-> Esse projeto já está configurado com um smtp e uma conta e-mail, por isso não se preocupe em com essa parte!
-> já existe cadastrado na base um usuário 'super-admin' registrado e os dados de acesso são:
    usuário: teste@teste.com
    senha: 1234
```


#### [link redoc (localhost)](http://127.0.0.1:8000/redoc/)

#### [link swagger (localhost)](http://127.0.0.1:8000/swagger/)


## Intruções


Os comandos abaixo devem ser executados em um terminal mapeado na pasta raiz do projeto.

#### 1 - Abra um `terminal` e ative um ambiente virtual `venv`:

```
.\venv\Scripts\activate
```


#### 2 - Instalar as dependências do projeto do ambiente `venv`:

```
poetry install
```



#### 3 - Certifique-se que está no ambiente `venv` e inicie o projeto:

```
poetry run manage.py runserver
```



#### 4 - Abra um segundo terminal, certifique-se que este também está no ambiente `venv` e inicie o `Celery`:

```
celery -A plataforma_agendamento worker -l info -P solo
```


#### 5 - Por fim, subir container do `RabbitMQ`:

```
docker run -d -p 5672:5672 rabbitmq
```


## Removendo o banco de dados atual


#### 1 - Remova o arquivo `db.sqlite3` da pasta raiz do projeto


#### 2 - Abra um `terminal` e ative um ambiente virtual `venv`:

```
.\venv\Scripts\activate
```

#### 3 - Execute o comando abaixo para que o python gere as migrations necessárias:

```
poetry run manage.py makemigrations
```


#### 4 - Execute o comando abaixo para que o python gere o banco e as tabelas do projeto:

```
poetry run manage.py migrate
```


#### 5 - Crie um novo usuário `super-admin` para ter acesso à parte administrativa do proejto:

```
poetry run manage.py createsuperuser
```