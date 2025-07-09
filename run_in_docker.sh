#!/bin/bash
# Script para iniciar serviços Docker com base em docker-compose
# Compatível com Linux e macOS

# Função para mostrar o menu
show_menu() {
    clear
    echo "Escolha o serviço Docker:  ╔═════════════════════╗"
    echo "╔══════════════════════════╣ S E R V I D O R E S ║"
    echo "║ [ 1 ] - MySQL            ╚═════════════════════╣"
    echo "║ [ 2 ] - PostgreSQL                             ║"
    echo "║ [ 3 ] - MongoDB                                ║"
    echo "║ [ 4 ] - OracleDB CE                            ║"
    echo "║ [ 5 ] - Microsoft SQL Server Express           ║"
    echo "║ [ * ] - Iniciar todos os servidores            ║"
    echo "║ [ x ] - STOP Parar todos os servidores         ║"
    echo "║ [ ! ] - PURGE Apagar tudo (vol., imagens, nw)  ║"
    echo "║ [ 0 ] - Sair           ╔═══════════════════════╣"
    echo "╠════════════════════════╣ F E R R A M E N T A S ║"
    echo "║ [ A ] - Adminer        ╚═══════════════════════╣"
    echo "║ [ B ] - phpMyAdmin                             ║"
    echo "║ [ C ] - pgAdmin                                ║"
    echo "║ [ D ] - Mongo Express                          ║"
    echo "║ [ E ] - Adminer_ci8                            ║"
    echo "╚════════════════════════════════════════════════╝"
}

# Função para executar um serviço específico
run_service() {
    local service=$1
    if [ -f "docker-compose-${service}.yml" ]; then
        echo "Iniciando serviço: ${service}..."
        docker compose -f "docker-compose-${service}.yml" up -d
    else
        echo "Erro: Ficheiro docker-compose-${service}.yml não encontrado!"
    fi
    echo "Prima Enter para continuar..."
    read
}

# Função para parar todos os serviços
stop_all() {
    echo "Parando todos os serviços..."
    for file in docker-compose-*.yml; do
        if [ -f "$file" ]; then
            echo "Parando $file..."
            docker compose -f "$file" down --remove-orphans
        fi
    done
    echo "Todos os serviços foram parados!"
    echo "Prima Enter para continuar..."
    read
}

# Função para limpeza completa
purge_all() {
    echo "⚠️  ATENÇÃO: Esta operação irá eliminar TODOS os dados Docker!"
    echo "Tem a certeza? (y/N): "
    read -r confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo "Realizando limpeza completa..."
        
        # Parar todos os compose files
        for file in docker-compose-*.yml; do
            if [ -f "$file" ]; then
                echo "Parando $file..."
                docker compose -f "$file" down --remove-orphans
            fi
        done
        
        # Limpeza completa do Docker
        echo "Parando todos os containers..."
        docker stop $(docker ps -aq) 2>/dev/null || true
        
        echo "Removendo todos os containers..."
        docker rm $(docker ps -aq) 2>/dev/null || true
        
        echo "Removendo todas as imagens..."
        docker rmi $(docker images -q) -f 2>/dev/null || true
        
        echo "Removendo todos os volumes..."
        docker volume rm $(docker volume ls -q) 2>/dev/null || true
        
        echo "Limpando redes..."
        docker network prune -f
        
        echo "Limpeza completa do sistema..."
        docker system prune -a --volumes -f
        
        echo "Limpeza completa realizada!"
    else
        echo "Operação cancelada."
    fi
    echo "Prima Enter para continuar..."
    read
}

# Função principal
main() {
    # Se foi passado um argumento, executar diretamente
    if [ $# -eq 1 ]; then
        run_service "$1"
        exit 0
    fi
    
    # Loop do menu principal
    while true; do
        show_menu
        echo -n "Opção: "
        read -r option
        
        case $option in
            1) run_service "mysql" ;;
            2) run_service "postgres" ;;
            3) run_service "mongo" ;;
            4) run_service "oracle" ;;
            5) run_service "sqlserver" ;;
            "*") run_service "ALL" ;;
            [Aa]) run_service "adminer" ;;
            [Bb]) run_service "phpmyadmin" ;;
            [Cc]) run_service "pgadmin" ;;
            [Dd]) run_service "mongo_express" ;;
            [Ee]) run_service "adminer_oci8" ;;
            [Xx]) stop_all ;;
            "!") purge_all ;;
            0) 
                echo "A sair..."
                exit 0
                ;;
            *)
                echo "Opção inválida!"
                echo "Prima Enter para continuar..."
                read
                ;;
        esac
    done
}

# Executar função principal com todos os argumentos
main "$@"
