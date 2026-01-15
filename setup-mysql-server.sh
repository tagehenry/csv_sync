#!/bin/bash

DB_NAME="mydatabase"
DB_USER="myuser"
DB_PASS="mypassword"


# Function to install a local MySQL server
install_mysql() {
    sudo apt update &> /dev/null
    # Check if update was successful
    if [ "$?" -ne 0 ]; then
        echo "There was an issue updated the apt repository. This may cause issues with installing mysql."
        read -p "Press Enter to continue: "
    fi
    # Now install mysql
    sudo apt install mysql-server -y &> /dev/null
    mysql_exit_status=$?
    if [ "$mysql_exit_status" -ne 0 ]; then
        echo "There was an issue installing mysql-server. Exit status: $mysql_exit_status"
        read -p "Press Enter to continue: "
    else
        echo "MySQL server was installed successfully!"
    fi
}

build_database() {
    sudo mysql <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF
}



install_mysql
build_database