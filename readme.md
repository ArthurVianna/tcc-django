# SEAS - STUDENT EVASION ANALYSIS SYSTEM

Trabalho desenvolvido para conclusão do curso de Análise e Desenvolvimento de Sistemas - UFPR.

## Instale o Python

Instale a versão mais recente do Python 3, então, se você tiver uma versão anterior, precisará atualizá-la. Se você já tem versão 3.6 ou superior, deve ficar bem.

## Baixe o projeto

Baixe o projeto, mantenha-o na pasta `tcc-django`. Note que o projeto ainda não tem sua virtualenv, nem o django instalado e nem as configurações para os bancos de dados.

## Configure o virtualenv e instale o Django

### Ambiente virtual

Vamos criar um ambiente virtual (também chamado um virtualenv). O virtualenv isolará seu código Python/Django em um ambiente organizado por projetos. Isso significa que as alterações que você fizer em um projeto não afetará os outros projetos que você estiver desenvolvendo ao mesmo tempo.

Tudo o que você precisa fazer é entrar no diretório `tcc-django` e criar o ambiente virtual com o comando abaixo.

```
$ python3 -m venv tccenv
```

### Trabalhando com o virtualenv

Inicie o seu ambiente virtual executando:

```
$ source tccenv/bin/activate
```

### Instalando o Django

Com a virtualenv ativa é hora de instalar o Django.

Mas antes, garanta que tem a última versão do pip instalada.

```
(tccenv) ~$ python -m pip install --upgrade pip
```

#### Instalando pacotes com requisitos

O arquivo `requirements.txt` guarda as dependências que serão instaladas utilizando o pip install.

Como esse projeto já tem suas dependências basta rodar o comando abaixo que todas elas serão instaladas, inclusive a versão do Django necessária para o projeto.

```
(tccenv) ~$ pip install -r requirements.txt
```

## Configure o banco de dados

Instale o MySQL 5.7

Encontre o arquivo `defaultDatabases.py` dento da pasta tcc e mude o user, password, host e port para aquelas que foram definidas nas suas configurações.

No MySQL Workbench ou na linha de comando do banco rode as seguintes linhas:

```
CREATE DATABASE tcc;

CREATE DATABASE datawarehousetcc;
```

## Rode as migrations

Rode os seguintes comandos para criar as tabelas dentro dos bancos de dados:

```
(tccenv) ~$ python manage.py migrate

(tccenv) ~$ manage.py migrate --database=datawarehouse
```

## Rode o projeto

Para rodar o projeto use o comando abaixo:

```
(tccenv) ~$ python manage.py runserver
```

Obs.: Para rodar o projeto sempre será necessário rodar esse comando, mas lembre de sempre incializar a virtualenv antes disso.

No navegador entre no endereço: `localhost:8000`.

Deve abrir a tela de login então como usuário coloque `admin` e como senha coloque `a1b2c3d4`.

Esse login te da acesso como super usuário.

Agora basta importar um arquivo (que segue o padrão utilizado para desenvolver o sistema) pela tela de Upload de CSV e esperar os scripts rodarem (pode demorar bastante) que o sistema terá os dados e a predição para cada aluno listado no arquivo.

---

O código está disponível no github nesse link: [tcc-django](https://github.com/ArthurVianna/tcc-django).

Para mais informações sobre o Django basta acessar a documentação oficial e se quiser um tutorial rápido para começar um projeto recomendamos o [Django Girls](https://tutorial.djangogirls.org/pt/).


**Devs:** Arthur Vianna Landeo ([ArthurVianna](https://github.com/ArthurVianna)), Cassiano Ricardo Filho ([Cassianosricardo](https://github.com/Cassianosricardo)), Tatiane Portela Medeiros ([corvinau](https://github.com/corvinau)).
