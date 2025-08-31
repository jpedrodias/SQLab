# (PT) Laboratório de SQL em Docker, Jupyter ou VM
O objetivo principal deste repositório é fornecer um ambiente de testes e aprendizagem para bases de dados relacionais e NoSQL, permitindo ao utilizador:
1. Instalar e configurar rapidamente múltiplos SGBDs (MySQL, PostgreSQL, MongoDB, OracleDB e Microsoft SQL Server) através de Docker;
1. Experimentar e praticar SQL em Jupyter Notebooks usando bibliotecas como o JupySQL;
1. Executar ambientes pré-configurados em Máquinas Virtuais para quem preferir não usar Docker;
1. Utilizar ferramentas Web e clientes gráficos para administração de bases de dados, sem necessidade de configurações complexas.
Trata-se, portanto, de um laboratório portátil de bases de dados, ideal para aprendizagem, experimentação, ensino e desenvolvimento.


Em resumo,destina-se a programadores, estudantes e professores que precisem de um laboratório completo de bases de dados, permitindo instalar e experimentar rapidamente vários SGBDs em ambientes isolados. É didático, modular e orientado para aprendizagem prática.




* 🐳 [Docker](#-preparação-do-sistema-para-correr-em-docker)
* 📓 [Jupyter Notebook](#-preparação-do-sistema-para-correr-em-jupyter-notebook)
* 🖥️ [Máquina virtual](#-preparação-do-sistema-para-correr-em-máquina-virtual)
* 🧰 [Outras ferramentas](#-ferramentas-para-ligação-a-bases-de-dados)


---
---


# 🐳 Preparação do sistema para correr em Docker

Nos ficheiros de *docker-compose* incluídos neste repositório existem diferentes cenários de base de dados e as respetivas ferramentas de administração que permitem a ligação a essas bases de dados:

| Ficheiro                         | Servidores                      | Ferramentas Web de Ligação       |
|----------------------------------|---------------------------------|----------------------------------|
| **docker-compose-mysql.yml**     | MySQL                           | Adminer, phpMyAdmin, CloudBeaver |
| **docker-compose-postgres.yml**  | PostgreSQL                      | Adminer, pgAdmin, CloudBeaver    |
| **docker-compose-mongo.yml**     | MongoDB                         | Mongo Express                    |
| **docker-compose-oracle.yml**    | OracleDB CE (Community Edition) | Adminer_ci8, , CloudBeaver       |
| **docker-compose-sqlserver.yml** | Microsoft SQL Server (Express)  | Adminer, CloudBeaver             |
| **docker-compose-redis.yml**     | Redis                           | DbGate                           |
| **docker-compose-ALL.yml**       | Todas as anteriores             | Todas as anteriores              |


## Servidores incluídos

* 🐬 **[MySQL](https://www.mysql.com/)** — SGBD relacional (RDBMS)
* 🐘 **[PostgreSQL](https://www.postgresql.org/)** — SGBD relacional avançado (ORDBMS)
* 🍃 **[MongoDB](https://www.mongodb.com/)** — Base de dados NoSQL orientada a documentos (Document Store)
* 🔶 **[OracleDB CE](https://www.oracle.com/pt/database/technologies/appdev/xe.html)** — SGBD relacional corporativo, versão gratuita *Community Edition* para testes e desenvolvimento
* 🟦 **[Microsoft SQL Server Express](https://www.microsoft.com/pt-br/sql-server/sql-server-downloads)** — SGBD relacional da Microsoft, versão gratuita *Express* para desenvolvimento e aplicações pequenas
* 🟥 **[Redis](https://redis.io/)** — Base de dados NoSQL em memória, utilizada para cache, filas e armazenamento de dados chave-valor



## Ferramentas de administração via Web

* 🛠️ **[Adminer](https://www.adminer.org/)** — Interface única, leve, compatível com vários SGBDs
* ☁️ **[CloudBeaver](https://github.com/dbeaver/cloudbeaver)** — Interface web universal do DBeaver, compatível com todos os SGBDs
* 🐘 **[pgAdmin](https://www.pgadmin.org/)** — Ferramenta oficial de administração PostgreSQL
* 🍃 **[Mongo Express](https://github.com/mongo-express/mongo-express)** — Interface leve para MongoDB
* 🐬 **[phpMyAdmin](https://www.phpmyadmin.net/)** — Interface clássica para MySQL/MariaDB
* 🟧 **[DbGate](https://dbgate.io/)** — Interface web para administração de bases de dados SQL e NoSQL (ex: Redis, MongoDB)
* 🔴 **[RedisInsight](https://redis.com/redis-enterprise/redis-insight/)** - ferramenta gráfica para administração e visualização de bases de dados Redis


---
---



## 🛠️ Etapas da instalação

### 0. Pré-requisitos

Certifique-se de que tem **Git**, **WSL** e **Docker Desktop** instalados:

* 🐳 [Git](https://git-scm.com/downloads)
* 🐧 [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/pt-pt/windows/wsl/install)
* 🐙 [Docker Desktop](https://www.docker.com/get-started/)



**Windows:**
Como alternativa, em windows, é possível fazer esta instalação usando o **winget**:

```bash
wsl --install
wsl --update
winget update
winget install -e --id Git.Git
winget install -e --id Docker.DockerDesktop
```

**macOS:**
Como alternativa, em macOS, é possível fazer esta instalação usando o **Homebrew**:

```bash
# Instalar Homebrew (se ainda não estiver instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Git e Docker Desktop
brew install git
brew install --cask docker
```

**Linux (Ubuntu/Debian):**
Para distribuições baseadas em Debian, use o **apt**:

```bash
# Atualizar repositórios
sudo apt update

# Instalar Git
sudo apt install git

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Reiniciar sessão ou executar:
newgrp docker
```



### 1. Clonar este repositório
```bash
git clone https://github.com/jpedrodias/SQLab.git
cd SQLab
```
> Ou, em alternativa, copie apenas os ficheiros `docker-compose-*.yml` pretendidos e o ficheiro `.env` de configuração das variáveis de ambiente.



### 2. Iniciar o docker container:
```bash
docker compose up
```
> Para manter os serviços em funcionamento é necessário manter o terminal aberto e para parar estes serviços basta pressionar `Ctrl+C`

Para iniciar os serviços em background é a mesma instrução mas, com a flag ` -d` (detached mode):
```bash
docker compose up -d
```
> E neste caso, não é necessário manter o terminal aberto e para parar estes serviços que ficaram a correr em background fazer `docker compose down`. Ou parar estes serviços através do Docker Desktop.



#### Extra - Servidor 1: MySQL
- Para correr a versão com o servidor da base de dados MySQL, usar o comando:
>    ```bash
>    docker compose -f docker-compose-mysql.yml up
>    ```


#### Extra - Servidor 2: PostgreSQL
- Para correr a versão com o servidor da base de dados Postgres, usar o comando:
>    ```bash
>    docker compose -f docker-compose-postgres.yml up
>    ```

#### Extra - Servidor 3: MongoDB
- Para correr a versão com o servidor de base de dados MongoDB, usar o comando:
>    ```bash
>    docker compose -f docker-compose-mongo.yml up
>    ```

#### Extra - Servidor 4: Oracle Database Express Edition
- Para correr a versão com o servidor de base de dados Oracle, usar o comando:
>    ```bash
>    docker compose -f docker-compose-oracle.yml up
>    ```


#### Extra - Servidor 5: Microsoft SQL Server - Express
- Para correr a versão com a base de dados da Microsoft SQL Server, usar o comando:
>    ```bash
>    docker compose -f docker-compose-sqlserver.yml up
>    ```


#### Extra - Servidor 6: Redis
- Para correr a versão com a base de dados Redis, usar o comando:
>    ```bash
>    docker compose -f docker-compose-redis.yml up
>    ```


#### Extra - CloudBeaver (Interface Universal):
- Para correr apenas o CloudBeaver (compatível com todos os SGBDs), usar o comando:
>    ```bash
>    docker compose -f docker-compose-cloudbeaver.yml up
>    ```
> O CloudBeaver é a versão web do popular DBeaver e suporta conexões a MySQL, PostgreSQL, MongoDB, Oracle, SQL Server e muitos outros SGBDs numa única interface.


#### Extra - Todos os servidores:
- Para correr a versão com todos os servidores (e ferramentas), usar o comando:
>    ```bash
>    docker compose -f docker-compose-ALL.yml up
>    ```
![Footprint de todos os servidores](img/footprint.png)  


#### Extra - Menu para inicializar os serviços:


**Windows:**
- Em alternativa, será possível inicializar qualquer um dos serviços anteriores correndo o ficheiro `batch`:
>    ```batch
>    .\run_in_docker.bat
>    ```

**Linux/macOS:**
- Para Linux e macOS, utilize o script `bash` equivalente:
>    ```bash
>    chmod +x run_in_docker.sh
>    ./run_in_docker.sh
>    ```
(`chmod` adicina as permissões para esse ficheiro poder ser executado)


**Extra:**
- Ou, se preferir executar diretamente um serviço específico:
>    ```bash
>    ./run_in_docker.sh mysql      # Para MySQL
>    ./run_in_docker.sh postgres   # Para PostgreSQL
>    ./run_in_docker.sh mongo      # Para MongoDB
>    ./run_in_docker.sh ALL        # Para todos os serviços
>    ```
> 
> ![Menu run_in_docker.bat](img/print_run_in_docker.png)
> 


**Avançado:**
É possível iniciar uma linha de comandos dentro do serviço. 
> No Docker Desktop, selecionar o serviço que está a correr e depois escolher o tab "Exec". 

Isso é o equivalente a fazer:
```bash
docker exec -it mysql_server    /bin/bash
docker exec -it postgres_server /bin/bash
docker exec -it mongodb_server  /bin/bash
docker exec -it oracle_server   /bin/bash
docker exec -it mssql_server    /bin/bash
docker exec -it redis_server    /bin/bash
```



### 3. Dados de acesso:
Para aceder a um servidor de base de dados, utilizado uma das ferramentas aqui incluida, o servidor **não** pode ser `localhost` e terá de ser o servidor indicado. 
Contudo, para ligação usando outras ferramentas, por exemplo, o DBeaver, o campo `Server host` será `localhost`.


3.1. ao servidor 1 - `MySQL`
```yml
Servidor: mysql ou localhost
user: mysql_user
password: mysql_password
base de dados: mydatabase
```
PS: No DBeaver, pode ser necessário fazer uma configuração adicional. Em `Driver properties` alterar `allowPublickeyRetrieval` de `false` para **`TRUE`**.


3.1. ao servidor 2 - `PostgreSQL`
```yml
Servidor: postgres ou localhost
user: postgres_user
password: postgres_password
base de dados: mydatabase
```

3.3. ao servidor 3 - `MongoDB`
```yml
Servidor: mongo ou localhost
user: mongo_user
password: mongo_password
base de dados: mydatabase
```

3.4. ao servidor 4 - `Oracle Database Express Edition`
```yml
Servidor: oracle ou localhost
user: system
password: oracle_password
base de dados: mydatabase
```

3.5. ao servidor 5 - `Microsoft SQL Server - Express`
```yml
Servidor: sqlserver ou localhost
user: sa
password: mssql_Sup3rStrong3Password!
base de dados: tempdb (ou deixar vazio)
```

3.6. ao servidor 6 - `Redis`
```yml
Servidor: redis ou localhost
```




### 4. Clientes Web (sem instalações adicionais)
Estas ferramentas incluidas permitem o acesso ao servidor de bases de dados, também sem qualquer instalação adicional. Contudo, nem todas as ferramentas permitem o acesso a todos as bases de dados. 

|Ferramenta   |Porta |MySQL|Postgres|Oracle|MS SQL|MongoDB |Redis|Acesso |
|-------------|------|-----|--------|------|------|--------|-----|-------|
|Adminer      |[8081](http://localhost:8081)  |✅  |✅      |❌    |✅   |❌ |❌  | none |
|CloudBeaver  |[8082](http://localhost:8082)  |✅  |✅      |✅    |✅   |❌ |❌  | initial setup required |
|pgAdmin      |[8083](http://localhost:8083)  |❌  |✅      |❌    |❌   |❌ |❌  | user: `admin@admin.com`, pass: `admin` |
|Mongo Express|[8084](http://localhost:8084)  |❌  |❌      |❌    |❌   |✅ |❌  | user: `admin`, pass: `admin` |
|Adminer_ci8  |[8085](http://localhost:8085)  |❌  |❌      |✅    |❌   |❌ |❌  | none |
|phpMyAdmin   |[8086](http://localhost:8086)  |✅  |❌      |❌    |❌   |❌ |❌  | none |
|DbGate       |[8087](http://localhost:8087)  |❌  |✅      |✅    |✅   |✅ |✅  | none |





### 5. 🧹 Limpeza completa do *cache* do Docker

Embora o Docker não tenha uma pegada tão grande quanto uma máquina virtual tradicional, continua a ser uma forma de virtualização que pode consumir espaço considerável em disco. Para além das imagens descarregadas, o Docker cria volumes, redes e outros artefactos que se podem acumular.

Nem sempre o Docker Desktop exibe todos os recursos ocupados. Para uma melhor gestão, será possível adicionar uma extensão chamada [Portainer](https://www.portainer.io/) em Extensões no Docker Desktop.


Ou em alternativa, será possível uma limpeza completa do *cache* utilizando:

```bash
docker compose down
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) -f
docker volume rm $(docker volume ls -q)
docker network prune -f
docker builder prune --all -f
docker system prune -a --volumes -f
```

> ℹ️ **Nota:** Os *volumes* Docker armazenam dados persistentes, como os das bases de dados.  
> ⚠️ **Atenção:** Use estes comandos com precaução, pois podem eliminar dados importantes que não possam ser recuperados.



---
---



# 📓 Preparação do sistema para correr em Jupyter Notebook:
O `JupySQL` permite executar comandos SQL e criar gráficos de grandes conjuntos de dados no Jupyter através das magias %sql, %%sql e %sqlplot. O JupySQL é compatível com todos os principais bancos de dados (por exemplo, PostgreSQL, MySQL, SQL Server), data warehouses (como Snowflake, BigQuery, Redshift) e motores embarcados (SQLite e DuckDB).

[ver JupySQL](https://jupysql.ploomber.io/en/latest/quick-start.html)


```python
!pip install ipykernel jupyterlab jupysql --upgrade --no-cache-dir
!pip cache purge

%load_ext sql
%sql sqlite:///database.sqlite

%config SqlMagic.displaylimit = 0
%sql PRAGMA foreign_keys = ON
```

## a) Correr Jupyter Online:
- [Google Colab](https://colab.research.google.com/)
- [Try Jupyter Lab](https://jupyter.org/try-jupyter/lab/)


## b) Correr Jupyter localmente em windows:
```bash
python -m venv C:\TEMP\venvs\SQLab
C:\TEMP\venvs\SQLab\Scripts\Activate.ps1
pip install -r requirements.txt --upgrade --no-cache-dir
pip cache purge
```
PS: Em Windows 11/10, poderá existir restrição na execução de scripts PowerShell `.ps1`. Neste caso, pode desactivar essa restrição ou executar o `activate.bat` em alternativa.

Para desactivar as restrições de execução de scripts `.ps1` abrir um terminal em mode de administrador e executar a seguinte instrução:
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
> ```



## c) Correr Jupyter localmente em macOS/Linux:
```bash
python3 -m venv /tmp/SQLab
source /tmp/SQLab/bin/activate
pip install -r requirements.txt --upgrade --no-cache-dir
pip cache purge
```



---
---



# 🖥️ Preparação do sistema para correr em máquina virtual:
- [Oracle Database Free VirtualBox Appliance](https://www.oracle.com/database/technologies/databaseappdev-vm.html) (da Oracle)
    - user: oracle ou system, password: oracle
    - fazer atualizações
    ```bash
    sudo dnf check-updates
    sudo dnf clean all
    ```
- [Máquina Virtual "Mint" com base de dados MySql e Postgress](https://drive.google.com/file/d/15cBQOABUNHihoPV5I7NGLIcFw-IkJ3k7/view)
    - user: osboxes.org, password: osboxes.org
    - fazer/forçar atualizações:
    ```bash
    sudo apt update -y && sudo apt upgrade -y && sudo apt full-upgrade -y && sudo apt dist-upgrade -y
    sudo apt autoclean -y && sudo apt autoremove -y
    ```
    - consertar falhas na atualização:
    ```bash
    sudo apt -fix-missing install
    ```


---
---



# 🧰 Ferramentas para ligação a bases de dados:
## a) aplicações:
* [DBeaver](https://dbeaver.io/download/) - ligação a diferentes bases de dados (sqlite, mysql, postgres, mongodb, oracle, etc);
* [sqlite3](https://www.sqlite.org/download.html) - ferramenta de linha de comandos para ligar a sqlite;
* [DB Browser for SQLite](https://sqlitebrowser.org/) - ferramenta gráfica para SQLite;
* [pgAdmin](https://www.pgadmin.org/download/) - ligação a bases de dados PostgreSQL;
* [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) - para ligação a db mysql/mariadb
* [SqlDbx](https://www.sqldbx.com/index.htm) - ligação a diferentes bases de dados;
* [MongoDB Compass](https://www.mongodb.com/try/download/compass) - para ligação a MongoDB
* [DbGate](https://dbgate.io/) - para ligação a SQL & NoSQL (Ex: MongoDB e Redis)
* [RedisInsight](https://redis.com/redis-enterprise/redis-insight/) - ferramenta gráfica para administração e visualização de bases de dados Redis


## b) ferramentas web de ligação:
* 🛠️ **[Adminer](https://www.adminer.org/)** — Interface única, leve, compatível com vários SGBDs
* ☁️ **[CloudBeaver](https://github.com/dbeaver/cloudbeaver)** — Interface web universal do DBeaver, compatível com todos os SGBDs
* 🐘 **[pgAdmin](https://www.pgadmin.org/)** — Ferramenta oficial de administração PostgreSQL
* 🍃 **[Mongo Express](https://github.com/mongo-express/mongo-express)** — Interface leve para MongoDB
* 🐬 **[phpMyAdmin](https://www.phpmyadmin.net/)** — Interface clássica para MySQL/MariaDB
* 🟧 **[DbGate](https://dbgate.io/)** — Interface web para administração de bases de dados SQL e NoSQL (ex: Redis, MongoDB)


## c) outras ferramentas web:
* [draw.io](https://draw.io) - Desenho de ERD (Entity-Relationship Diagrams)
* [mockarro](https://mockaroo.com/) - Criação dados aleatórios
* [SandboxSQL](https://sandboxsql.com/) - Ambiente online para praticar SQL com bases de dados reais
* [dbdiagram.io](https://dbdiagram.io) - Desenho de ERD (Entity-Relationship Diagrams)
* [SQLiteOnline](https://sqliteonline.com/) - Editor online para testar SQL em SQLite, PostgreSQL, MySQL e outros


---
---

# Aprender SQL
* [Cheatsheets](https://github.com/FavioVazquez/ds-cheatsheets)


---
---
end of file: (PT) Laboratório de SQL em Docker, Jupyter ou VM