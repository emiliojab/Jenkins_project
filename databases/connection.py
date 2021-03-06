from . import config
from pymongo import MongoClient
from abc import abstractmethod
import urllib
# from sqlalchemy import create_engine
from mysql.connector import (connection)

class Connect(object):

    def __init__(self):
        pass

    @abstractmethod
    def connect_to_DB(self):
        pass

class MongoDB(Connect):

    def __init__(self) -> None:
        """parameters:
                database(string): the database name to connect to"""
        super().__init__()
        self._conf = config.MongoDBConfig()
        (self.mongoDB_username, self.mongoDB_pwd,
            self.mongoDB_port, self.mongoDB_ip_address,
                self.mongoDB_database, self.mongoDB) = self._conf.get_credentials()

    def connect_to_DB(self) -> MongoClient:
        """Opens and returns a MongoDB connection."""
        # print(f'mongodb://{self.mongoDB_username}:{self.mongoDB_pwd}@{self.mongoDB_ip_address}:{self.mongoDB_port}/{self.mongoDB}')
        return MongoClient(f'mongodb://{self.mongoDB_username}:{self.mongoDB_pwd}@{self.mongoDB_ip_address}:{self.mongoDB_port}/{self.mongoDB}')

class MySQL(Connect):

    def __init__(self) -> None:
        """parameters:
                database(string): the database name to connect to"""
        super().__init__()
        self._conf = config.MySQLConfig()
        (self.MySQL_user, self.MySQL_pwd,
            self.MySQL_port, self.MySQL_host,
                self.MySQL_database) = self._conf.get_credentials()

    def connect_to_DB(self) -> connection:
        """Opens and returns a MySQL connection."""
        return connection.MySQLConnection(user=self.MySQL_user, password=self.MySQL_pwd,
                                 host=self.MySQL_host,
                                 database=self.MySQL_database)