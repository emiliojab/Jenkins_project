from databases.connection import MySQL, MongoDB
import simplejson as json
from encoder import CustomEncoder

mysql_schema = 'classicmodels'
MongoDB_db = 'admin'
query_for_foreign_keys = """
                            select *
                            from information_schema.KEY_COLUMN_USAGE
                            where TABLE_SCHEMA = "%s" 
                            and TABLE_NAME= "%s" 
                            and REFERENCED_TABLE_NAME IS NOT NULL
                            """

if __name__ == "__main__":
    mysql = MySQL(mysql_schema)
    mysql_cnx = mysql.connect_to_DB()

    mongodb = MongoDB(MongoDB_db)
    mongodb_cnx = mongodb.connect_to_DB()
    mdb = mongodb_cnx.Jenkins

    table_list_cursor = mysql_cnx.cursor(dictionary=True)
    table_list_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name;", (mysql_schema,))
    tables = table_list_cursor.fetchall()
    
    cursor = mysql_cnx.cursor(dictionary=True)

    for table in tables:
        table_name = table['TABLE_NAME']

        collection = mdb[table_name]

        cursor.execute(f"SELECT * FROM {table_name};")
        table = cursor.fetchall()

        table = json.dumps(table,cls=CustomEncoder)
        table  = json.loads(table)

        if len(table) > 0:
            x = collection.insert_many(table)
            print(f"Insterted {table_name}: {len(x.inserted_ids)} records.")
        else:
            print("Nothing was inserted")


    mysql_cnx.close()
    mongodb_cnx.close()