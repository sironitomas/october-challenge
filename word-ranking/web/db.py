import hashlib
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'ranking'


def connect():
    try:
        cnx = mysql.connector.connect(user='root',
                                      password='my-strong-password',
                                      host='db')
        return cnx
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
    TABLES['allwords'] = ("CREATE TABLE `allwords` ("
                          "  `hash` varchar(32) NOT NULL,"
                          "  `word` varchar(64) NOT NULL,"
                          "  `count` int(10) NOT NULL,"
                          "  PRIMARY KEY (`hash`)"
                          ") ENGINE=InnoDB")

    cnx = connect()
    cursor = cnx.cursor()

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


def save_words(new_words):
    cnx = connect()
    cursor = cnx.cursor()

    cursor.execute("USE {}".format(DB_NAME))
    query = "SELECT word, count FROM allwords"
    cursor.execute(query)
    current_words_dict = {}
    for (word, count) in cursor:
        current_words_dict[word] = count

    new_words_dict = {}
    for i in new_words:
        word = i['word']
        count = i['count']
        new_words_dict[word] = count

    inserts = []
    updates = []
    for word, count in new_words_dict.items():
        res = hashlib.md5(word.encode())
        md5sum = res.hexdigest()
        if word in current_words_dict:
            new_count = count + current_words_dict[word]
            query = "UPDATE allwords SET count={} WHERE hash=\"{}\"".format(
                new_count, md5sum)
            updates.append(query)
        else:
            query = "INSERT INTO allwords VALUES (\"{}\", \"{}\", {})".format(
                md5sum, word, count)
            inserts.append(query)

    for query in updates:
        cursor.execute(query)
    for query in inserts:
        cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()
