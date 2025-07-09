@echo off
REM Script para iniciar serviços Docker com base em docker-compose
chcp 65001 >nul

if "%1"=="" goto MENU
if not "%1"=="" goto RUN

:MENU
set op=""
cls
echo Escolha o serviço Docker:  ╔═════════════════════╗
echo ╔══════════════════════════╣ S E R V I D O R E S ║
echo ║ [ 1 ] - MySQL            ╚═════════════════════╣
echo ║ [ 2 ] - PostgreSQL                             ║
echo ║ [ 3 ] - MongoDB                                ║
echo ║ [ 4 ] - OracleDB CE                            ║
echo ║ [ 5 ] - Microsoft SQL Server Express           ║
echo ║ [ * ] - Iniciar todos os servidores            ║
echo ║ [ x ] - STOP Parar todos os servidores         ║
echo ║ [ ! ] - PURGE Apagar tudo (vol., imagens, nw)  ║
echo ║ [ 0 ] - Sair           ╔═══════════════════════╣
echo ╠════════════════════════╣ F E R R A M E N T A S ║
echo ║ [ A ] - Adminer        ╚═══════════════════════╣
echo ║ [ B ] - phpMyAdmin                             ║
echo ║ [ C ] - pgAdmin                                ║
echo ║ [ D ] - Mongo Express                          ║
echo ║ [ E ] - Adminer_ci8                            ║
echo ╚════════════════════════════════════════════════╝
set /p op=Opção: 

if "%op%"=="1" %0 mysql
if "%op%"=="2" %0 postgres
if "%op%"=="3" %0 mongo
if "%op%"=="4" %0 oracle
if "%op%"=="5" %0 sqlserver
if "%op%"=="*" %0 ALL

if /I "%op%"=="A" %0 adminer
if /I "%op%"=="B" %0 phpmyadmin
if /I "%op%"=="C" %0 pgadmin
if /I "%op%"=="D" %0 mongo_express
if /I "%op%"=="E" %0 adminer_oci8

if /I "%op%"=="X" goto STOP
if "%op%"=="!" goto PURGE
if "%op%"=="0" exit

echo Opção inválida!
pause
goto MENU


:PURGE
echo ⚠️  ATENÇÃO: Esta operação irá eliminar TODOS os dados Docker!
echo Isto inclui:
echo   • Todos os containers
echo   • Todas as imagens
echo   • Todos os volumes (DADOS SERÃO PERDIDOS!)
echo   • Todas as redes
echo.
set /p confirm=Tem a certeza? (y/N): 
if /I not "%confirm%"=="y" (
    echo Operação cancelada.
    pause
    goto MENU
)

echo Realizando limpeza completa...
for %%f in (docker-compose-*.yml) do (
    echo Parando %%f...
    docker compose -f %%f down --remove-orphans
)
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) -f
docker volume rm $(docker volume ls -q)
docker network prune -f
docker system prune -a --volumes -f
echo Limpeza completa realizada!
pause
goto MENU


:STOP
for %%f in (docker-compose-*.yml) do (
    echo Parando %%f...
    docker compose -f %%f down --remove-orphans
)
echo Todos os serviços foram parados!
pause
goto MENU

:RUN
if exist "docker-compose-%1.yml" (
    echo Iniciando serviço: %1...
    docker compose -f docker-compose-%1.yml up -d
) else (
    echo Erro: Ficheiro docker-compose-%1.yml não encontrado!
)
pause
goto MENU

:EOF