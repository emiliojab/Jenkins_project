from abc import abstractmethod
from dotenv import load_dotenv
import os
import urllib


class Config(object):

    def __init__(self):
        load_dotenv()

    @abstractmethod
    def get_credentials(self):
        """An abstract method.
        """
        pass


class MongoDBConfig(Config):

    def __init__(self):
        """Get the credentials for MongoDB database connection from the .env file"""
        super().__init__()
        self.__mongoDB_username = os.getenv("MONGODB_USERNAME")
        self.__mongoDB_pwd = urllib.parse.quote_plus(os.getenv("MONGODB_PWD"))
        self.__mongoDB_port = os.getenv("MONGODB_PORT")
        self.__mongoDB_ip_address = os.getenv("MONGODB_IP")
        self.__mongoDB_database = os.getenv("MONGODB_DATABASE")
        self.__mongoDB = os.getenv("MONGODB")

    def get_credentials(self):
        """Returns the credentials of the MongoDB server"""
        return (self.__mongoDB_username, self.__mongoDB_pwd,
                    self.__mongoDB_port, self.__mongoDB_ip_address,
                        self.__mongoDB_database, self.__mongoDB)

class MySQLConfig(Config):

    def __init__(self):
        """Get the credentials for MySQL database connection from the .env file"""
        super().__init__()
        self.__MySQL_user = os.getenv("MYSQL_USER")
        self.__MySQL_pwd = urllib.parse.quote_plus(os.getenv("MYSQL_PWD"))
        self.__MySQL_port = os.getenv("MYSQL_PORT")
        self.__MySQL_host = os.getenv("MYSQL_HOST")
        self.__MySQL_database = os.getenv("MYSQL_DATABASE")

    def get_credentials(self):
        """Returns the credentials of the MySQL server"""
        return (self.__MySQL_user, self.__MySQL_pwd,
                    self.__MySQL_port, self.__MySQL_host,
                        self.__MySQL_database)