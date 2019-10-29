from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode


def connect():
    try:
        cnx = mysql.connector.connect(user='root',
                                      password='my-strong-password',
                                      database='words')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


def create_database(cursor, DB_NAME):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def create_tables():
    TABLES = {}
    TABLES['employees'] = ("CREATE TABLE `allwords` ("
                           "  `hash` varchar(32) NOT NULL AUTO_INCREMENT,"
                           "  `word` varchar(64) NOT NULL,"
                           "  `count` int(10) NOT NULL,"
                           "  PRIMARY KEY (`hash`)"
                           ") ENGINE=InnoDB")

    cnx = mysql.connector.connect(user='root',
                                  password='my-strong-password',
                                  host='db')
    cursor = cnx.cursor()

    DB_NAME = 'words'
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, DB_NAME)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()
