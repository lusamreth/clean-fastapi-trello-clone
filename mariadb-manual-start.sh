#!/bin/bash 

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

chmod 777 /var/lib/mysql
mkdir /run/mysqld
chmod 777 /run/mysqld



