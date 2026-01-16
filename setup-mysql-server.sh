#!/bin/bash

# Helps to set up a local MySQL server for use with the csv_sync tool.

# Function to install a local MySQL server
install_mysql() {
    if command -v mysql &> /dev/null; then
        echo "MySQL is already installed."
        return
    fi
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
    fi
    if command -v mysql &> /dev/null; then
        echo "MySQL installation verified."
    else
        echo "MySQL installation failed."
        exit 1
    fi
    if ! command -v jq &> /dev/null; then
        echo "jq is not installed. Installing jq..."
        sudo apt install jq -y &> /dev/null
        if [ "$?" -ne 0 ]; then
            echo "There was an issue installing jq. Please install it manually."
            exit 1
        fi
    fi
}

# Function to parse the JSON config file and assign DB variables (needs jq)
load_config() {
    LOCATION_OF_SCRIPT=$(dirname "$0")
    CONFIG_FILE="$LOCATION_OF_SCRIPT/db_config.json"
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Configuration file not found! Please copy db_config_default.json to db_config.json and update the values."
        exit 1
    fi

    DB_HOST=$(jq -r '.database.host' "$CONFIG_FILE")
    DB_PORT=$(jq -r '.database.port' "$CONFIG_FILE")
    DB_NAME=$(jq -r '.database.database_name' "$CONFIG_FILE")
    DB_USER=$(jq -r '.database.user' "$CONFIG_FILE")
    DB_PASS=$(jq -r '.database.password' "$CONFIG_FILE")
}

build_database() {
    sudo mysql -h "$DB_HOST" -P "$DB_PORT" <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
EOF
}



install_mysql
load_config
build_database