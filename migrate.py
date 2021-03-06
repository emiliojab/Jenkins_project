from databases.connection import MySQL, MongoDB
import simplejson as json
from encoder import CustomEncoder
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    mysql_schema = os.getenv("MYSQL_DATABASE")
    mongDB_db = os.getenv("MONGODB_DATABASE")
    # connecto to MySQL database
    mysql = MySQL()
    mysql_cnx = mysql.connect_to_DB()

    # connecto to MongoDB
    mongodb = MongoDB()
    mongodb_cnx = mongodb.connect_to_DB()
    mdb = mongodb_cnx[mongDB_db]

    # get the list of tables in the MySQL database 
    table_list_cursor = mysql_cnx.cursor(dictionary=True)
    table_list_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name;", (mysql_schema,))
    # a list of table names
    tables = table_list_cursor.fetchall()
    
    # dictionary=True, gets a list of dictionaries
    # where each dictionary is a record
    cursor = mysql_cnx.cursor(dictionary=True)

    # for each table name in tables, run SQL query to fetch all the records of the specific table
    # create table in MongoDB and store the fetched records 
    for table in tables:
        table_name = table['TABLE_NAME']

        # create collection
        collection = mdb[table_name]

        # fetch records of table_name
        cursor.execute(f"SELECT * FROM {table_name};")
        table = cursor.fetchall()

        # change encoder to meet MongoDB standards using the class CustomEncoder
        table = json.dumps(table, cls=CustomEncoder)
        table  = json.loads(table)

        if len(table) > 0:
            # insert table list into MongoDB
            ids = collection.insert_many(table)
            print(f"Insterted {table_name}: {len(ids.inserted_ids)} records.")
        else:
            print("Nothing was inserted")

    # close connections
    mysql_cnx.close()
    mongodb_cnx.close()