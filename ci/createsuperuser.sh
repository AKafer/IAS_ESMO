#!/usr/bin/expect -f

set timeout 1

set ADMIN_LOGIN $::env(ADMIN_LOGIN)
set ADMIN_EMAIL $::env(ADMIN_EMAIL)
set ADMIN_PASSWORD $::env(ADMIN_PASSWORD)

spawn docker exec -it esmo_app python manage.py createsuperuser

expect "Username (leave blank to use 'root'):\r"

send "$ADMIN_LOGIN\r"

expect "Email address:\r"

send "$ADMIN_EMAIL\r"

expect "Password:\r"

send "$ADMIN_PASSWORD\r"

expect "Password (again):\r"

send "$ADMIN_PASSWORD\r"

expect eof
