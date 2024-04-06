#!/bin/bash
# Запуск Модуля Esmo в докере.

# 1. Запускаем Esmo если он остановлен.
function run_esmo {
    clear
    echo -en "\033[37;1;41m Останавливаем контейнеры. \033[0m\n"
    docker-compose down -v
    echo -en "\033[37;1;41m Собираем контейнеры. \033[0m\n"
    docker-compose up -d --build
    echo -en "\033[37;1;41m Применяем миграции. \033[0m\n"
    docker exec esmo_app python manage.py migrate --noinput
    echo -en "\033[37;1;41m Собираем статику. \033[0m\n"
    docker exec esmo_app python manage.py collectstatic --no-input
    echo -en "\033[37;1;41m Создаем суперюзера. \033[0m\n"
    docker exec -it esmo_app python manage.py createsuperuser
    echo -en "\033[37;1;41m Перезагружаем контейнеры. \033[0m\n"
    docker-compose restart
    echo -en "\033[37;1;41m Готово. Модуль ESMO запущен. \033[0m\n"
}

# 2. Делаем бекап базы данных.
function backup_esmo {
    clear
    echo -en "\033[37;1;41m Делаем бекап базы данных. \033[0m \n"
    docker-compose start
    # trunk-ignore(shellcheck/SC2046)
    docker exec esmo_app python manage.py dumpdata --format json -e contenttypes -e auth.permission > ./backups/db_backup_$(date -d "today" +"%Y.%m.%d_%H.%M").json
    echo -en "\033[37;1;41m База сохранена в папку Esmo/application/backups под именем backup_$(date -d "today" +"%Y.%m.%d_%H.%M").json \033[0m\n"
    echo -en "\033[37;1;41m Готово \033[0m\n"
}


# 3. Остановить Модуль ESMO.
function stop_esmo {
    clear
    echo -en "\033[37;1;41m Останавливаем Модуль ESMO. \033[0m \n"
    docker-compose down
    echo -en "\033[37;1;41m Готово. Модуль ESMO остановлен. \033[0m\n"
}

function menu {
    clear
    echo
    echo -e "\033[37;1;41m\t\t\t Меню Модуля Esmo \033[0m\n"
    echo -e "\t 1) Запустить Модуль Esmo (Если остановлен)"
    echo -e "\t 2) Сделать бекап базы данных (В формате db_backup_YYYY.MM.DD.json)"
    echo -e "\t 3) Остановить Модуль Esmo"
    echo -e ""
    echo -e "\t 0. Выход"
    echo -e ""
    echo -en "\t Введите номер меню: "
    read -n 1 option
    clear
}

while [ $? -ne 1 ]
    do
        menu
        case $option in
        0)
        break ;;
        1) 
        run_esmo ;;
        2)
        backup_esmo ;;
        3)
        stop_esmo ;;
        *)
        clear

echo -en "\n \033[37;1;41m Нужно выбрать раздел! \033[0m\n"
esac
    echo -en "\n\n\t\t\t\033[37;1;41m Нажмите любую клавишу для продолжения. \033[0m\n"
    # trunk-ignore(shellcheck/SC2034)
    # trunk-ignore(shellcheck/SC2162)
    read -n 1 line
done
clear
