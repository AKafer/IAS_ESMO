#!/bin/bash
# Запуск Модуля Esmo в докере.

# 1. Запускаем Esmo если он остановлен.
function run_esmo {
    clear
    echo -en "\033[37;1;41m Останавливаем контейнеры. \033[0m\n"
    docker-compose down
    echo -en "\033[37;1;41m Собираем контейнеры. \033[0m\n"
    docker-compose up -d --build
    echo -en "\033[37;1;41m Применяем миграции. \033[0m\n"
    docker exec esmo_app python manage.py migrate --noinput
    echo -en "\033[37;1;41m Собираем статику. \033[0m\n"
    docker exec esmo_app python manage.py collectstatic --no-input
    echo -en "\033[37;1;41m Создаем суперюзера статику. \033[0m\n"
    docker exec -it esmo_app python manage.py createsuperuser
    echo -en "\033[37;1;41m Перезагружаем контейнеры. \033[0m\n"
    docker-compose restart
    echo -en "\033[37;1;41m Готово. Модуль ESMO запущен. \033[0m\n"
}

# 2. Обновляем Модуль esmo.
function update_esmo {
    clear
    echo -en "\033[37;1;41m Останавливаем контейнеры. \033[0m\n"
    docker-compose stop
    echo -en "\033[37;1;41m Удаляем все тома. \033[0m\n"
    docker-compose down -v
    echo -en "\033[37;1;41m Собираем контейнеры. \033[0m\n"
    docker-compose up -d --build
    echo -en "\033[37;1;41m Собираем приложение \033[0m\n"
    docker exec esmo_app python manage.py migrate --noinput
    echo -en "\033[37;1;41m Собираем статику. \033[0m\n"
    docker exec esmo_app python manage.py collectstatic --no-input
    echo -en "\033[37;1;41m Перезагружаем контейнеры. \033[0m\n"
    docker-compose restart
    echo -en "\033[37;1;41m Готово. Приложение запущено. \033[0m\n"
}

# 3. Перезапускаем Модуль СИЗ.
function migr_esmo {
    clear
    set -e
    set -x
    echo -en "\033[37;1;41m Применяем опять миграции. \033[0m\n"
    docker exec -it esmo_app python manage.py migrate
#    docker-compose exec esmo_app python manage.py migrate
    echo -en "\033[37;1;41m Применили миграции. \034[0m\n"
}

# 4. Делаем бекап базы данных.
function backup_jppe {
    clear
    echo -en "\033[37;1;41m Делаем бекап базы данных. \033[0m \n"
    docker-compose start
    # trunk-ignore(shellcheck/SC2046)
    docker-compose exec backend python manage.py dumpdata --format json -e contenttypes -e auth.permission > ./backups/db_backup_$(date -d "today" +"%Y.%m.%d_%H.%M").json
    echo -en "\033[37;1;41m База сохранена в папку JournalPersonalProtectiveEquipment/application/backups под именем backup_$(date -d "today" +"%Y.%m.%d_%H.%M").json \033[0m\n"
    echo -en "\033[37;1;41m Готово \033[0m\n"
}

# 5. Чистая установка из csv файлов.
function clear_install_jppe {
    clear
    echo -en "\033[37;1;41m Останавливаем контейнеры. \033[0m\n"
    docker-compose stop
    echo -en "\033[37;1;41m Собираем контейнеры. \033[0m\n"
    docker-compose up -d --build
    echo -en "\033[37;1;41m Применяем миграции. \033[0m\n"
    docker-compose exec backend python manage.py makemigrations
    docker-compose exec backend python manage.py migrate --noinput
    echo -en "\033[37;1;41m Собираем статику. \033[0m\n"
    docker-compose exec backend python manage.py collectstatic --no-input
    echo -en "\033[37;1;41m Готово \033[0m\n"
    docker-compose exec backend python manage.py del_mat
    echo -en "\033[37;1;41m Перезагружаем контейнеры. \033[0m\n"
    docker-compose restart
    echo -en "\033[37;1;41m Готово \033[0m\n"
}

# 6. Чистое обновление без перезаписи базы данных. Только код.
function simple_update_linux_jppe {
    clear
    echo -en "\033[37;1;41m Удаляем контейнеры backend, nginx и том статики. \033[0m\n"
    docker rm -f application_backend_1
    docker rm -f application_nginx_1
    echo -en "\033[37;1;41m Останавливаем контейнеры. \033[0m\n"
    docker-compose stop
    echo -en "\033[37;1;41m Собираем контейнеры. \033[0m\n"
    docker-compose up -d --build
    echo -en "\033[37;1;41m Собираем приложение \033[0m\n"
    docker-compose exec backend python manage.py makemigrations
    docker-compose exec backend python manage.py migrate --noinput
    echo -en "\033[37;1;41m Собираем статику. \033[0m\n"
    docker-compose exec backend python manage.py collectstatic --no-input
    echo -en "\033[37;1;41m Перезагружаем контейнеры. \033[0m\n"
    docker-compose restart
    echo -en "\033[37;1;41m Готово \033[0m\n"
}

# 7. Чистка мусора от не нужных данных.
function clear_trash_jppe {
    clear
    echo -en "\033[37;1;41m Запускаем чистку мусора. \033[0m \n"
    docker system prune -a -f
    echo -en "\033[37;1;41m Готово. Мусор удален. \033[0m\n"
}

# 8. Остановить Модуль ESMO.
function stop_esmo {
    clear
    echo -en "\033[37;1;41m Останавливаем Модуль ESMO. \033[0m \n"
    docker-compose down
    echo -en "\033[37;1;41m Готово. Модуль ESMO остановлен. \033[0m\n"
}

function menu {
    clear
    echo
    echo -e "\033[37;1;41m\t\t\t Меню Модуля СИЗ \033[0m\n"
    echo -e "\t 1) Запустить Модуль СИЗ (Если остановлен)"
    echo -e "\t 2) Обновить Модуль СИЗ (Переустановка с восстановлением базы из бекапа)"
    echo -e "\t 3) Перезапустить Модуль СИЗ (При необходимости)"
    echo -e "\t 4) Сделать бекап базы данных (В формате db_backup_YYYY.MM.DD.json)"
    echo -e "\t 5) Удалить не нужные материалы массово."
    echo -e "\t 6) Обновление кода в Astra Linux (База данных не обновится)"
    echo -e "\t 7) Чистка мусора (Запускать при ЗАПУЩЕННОМ Модуле СИЗ)"
    echo -e "\t 8) Остановить Модуль СИЗ"
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
        update_esmo ;;
        3)
        migr_esmo ;;
        4)
        backup_jppe ;;
        5)
        clear_install_jppe ;;
        6)
        simple_update_linux_jppe ;;
        7)
        clear_trash_jppe ;;
        8)
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
