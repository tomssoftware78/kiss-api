import os
import time
from socket import socket
from fabric import Connection

import iris
import jaydebeapi
from dotenv import load_dotenv
from fabric import Connection
from generic_connection_pool.threading import BaseConnectionManager, ConnectionPool
from typing import Optional
import logging

logger = logging.getLogger(__name__)

load_dotenv()
use_cache_driver = os.environ.get('USE_OLD_CACHE_DRIVER')
Endpoint = str


class CacheConnectionManager(BaseConnectionManager[Endpoint, jaydebeapi.Connection]):
    """We don't want to create a new connection each time, because the db connection fails the first time right after
    creating the ssh-tunnel. It all takes too much time. """

    def __init__(self, connection_kiss_ip, connection_kiss_port: str, connection_kiss_schema: str, username: str,
                 password: str, connection_ssh_jump_key: str, connection_ssh_jump_user: str,
                 connection_ssh_jump_host: str):
        logger.info("Instantiating CacheConnectionManager")
        self.connection_kiss_ip = connection_kiss_ip
        self.connection_kiss_port = connection_kiss_port
        self.connection_kiss_schema = connection_kiss_schema
        self.connection_kiss_username = username
        self.connection_kiss_password = password
        self.connection_ssh_jump_key = connection_ssh_jump_key
        self.connection_ssh_jump_user = connection_ssh_jump_user
        self.connection_ssh_jump_host = connection_ssh_jump_host
        self.connectiondata = {}

    # First connection takes some time
    def retrier(self, counter, func, args):
        try:
            return func(*args)
        except Exception as e:
            logger.error("Retrier: %s %s", str(counter) + " " + str(e))
            if counter > 0:
                time.sleep(1)
                return self.retrier(counter - 1, func, args)
            else:
                raise e

    def connect_to_iris(self, localport):
        connection_string = "127.0.0.1:" + str(localport) + "/" + self.connection_kiss_schema

        # JAR_FILE = "driver/CacheDB.jar"
        JAR_FILE = "./driver/CacheDB.jar"  # tvde

        logger.info("Driver file found: %s", str(os.path.exists(JAR_FILE)))
        IRIS_DRIVER = "com.intersys.jdbc.CacheDriver"

        return jaydebeapi.connect(IRIS_DRIVER, "jdbc:Cache://" + connection_string,
                                  {"user": "root_kiss", "password": "kiss001"}, [JAR_FILE])

    def create(self, endpoint: Endpoint, timeout: Optional[float] = None) -> jaydebeapi.Connection:
        localport = None
        with socket() as s:
            s.bind(('', 0))
            logger.info("Socket: %s", s.getsockname()[1])
            localport = (int)(s.getsockname()[1])

        networkconnection = Connection(
            host=self.connection_ssh_jump_host,
            user=self.connection_ssh_jump_user,
            connect_kwargs={
                "key_filename": self.connection_ssh_jump_key,
            },
        )
        ctx = networkconnection.forward_local(local_port=localport, remote_port=self.connection_kiss_port,
                                              remote_host=self.connection_kiss_ip, local_host="127.0.0.1")
        ctx.__enter__()

        db_connection = self.retrier(3, self.connect_to_iris, [(localport)])

        self.connectiondata[db_connection] = (networkconnection, ctx, localport)

        logger.info("Created a new connection with ssh port: %s", str(self.connectiondata[db_connection][2]))

        return db_connection

    def dispose(self, endpoint: Endpoint, db_connection: jaydebeapi.Connection,
                timeout: Optional[float] = None) -> None:
        self.connectiondata.pop(db_connection)

    def check_aliveness(self, endpoint: Endpoint, db_connection: jaydebeapi.Connection,
                        timeout: Optional[float] = None) -> bool:
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT TOP 1 ID FROM kiss.tblGebruikers")
        except Exception as e:
            return False

        return True

    def on_acquire(self, endpoint: Endpoint, db_connection: jaydebeapi.Connection) -> None:
        logger.info("Acquired a new connection with ssh port: %s", str(self.connectiondata[db_connection][2]))

    def on_release(self, endpoint: Endpoint, db_connection: jaydebeapi.Connection) -> None:
        logger.info("Released a connection with ssh port: %s", str(self.connectiondata[db_connection][2]))


class IrisConnectionManager(BaseConnectionManager[Endpoint, iris.IRISConnection]):
    """We don't want to create a new connection each time, because the db connection fails the first time right after
    creating the ssh-tunnel. It all takes too much time. """

    def __init__(self, connection_kiss_ip, connection_kiss_port: str, connection_kiss_schema: str, username: str,
                 password: str, connection_ssh_jump_key: str, connection_ssh_jump_user: str,
                 connection_ssh_jump_host: str):
        logger.info("Instantiating IrisConnectionManager")
        self.connection_kiss_ip = connection_kiss_ip
        self.connection_kiss_port = connection_kiss_port
        self.connection_kiss_schema = connection_kiss_schema
        self.connection_kiss_username = username
        self.connection_kiss_password = password
        self.connection_ssh_jump_key = connection_ssh_jump_key
        self.connection_ssh_jump_user = connection_ssh_jump_user
        self.connection_ssh_jump_host = connection_ssh_jump_host
        self.connectiondata = {}

    # First connection takes some time
    def retrier(self, counter, func, args):
        try:
            return func(*args)
        except Exception as e:
            logger.error("Retrier: %s %s", str(counter), str(e))
            if counter > 0:
                time.sleep(1)
                return self.retrier(counter - 1, func, args)
            else:
                raise e

    def connect_to_iris(self, localport):
        connection_string = "127.0.0.1:" + str(localport) + "/" + self.connection_kiss_schema
        return iris.connect(connection_string, username=self.connection_kiss_username,
                            password=self.connection_kiss_password)

    def create(self, endpoint: Endpoint, timeout: Optional[float] = None) -> iris.IRISConnection:
        localport = None
        with socket() as s:
            s.bind(('', 0))
            logger.info("Socket: %s", s.getsockname()[1])
            localport = (int)(s.getsockname()[1])

        networkconnection = Connection(
            host=self.connection_ssh_jump_host,
            user=self.connection_ssh_jump_user,
            connect_kwargs={
                "key_filename": self.connection_ssh_jump_key,
            },
        )
        ctx = networkconnection.forward_local(local_port=localport, remote_port=self.connection_kiss_port,
                                              remote_host=self.connection_kiss_ip, local_host="127.0.0.1")
        ctx.__enter__()

        db_connection = self.retrier(3, self.connect_to_iris, [(localport)])

        self.connectiondata[db_connection] = (networkconnection, ctx, localport)

        logger.info("Created a new connection with ssh port: %s", str(self.connectiondata[db_connection][2]))

        return db_connection

    def dispose(self, endpoint: Endpoint, db_connection: iris.IRISConnection, timeout: Optional[float] = None) -> None:
        self.connectiondata.pop(db_connection)

    def check_aliveness(self, endpoint: Endpoint, db_connection: iris.IRISConnection,
                        timeout: Optional[float] = None) -> bool:
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT TOP 1 ID FROM kiss.tblGebruikers")
        except Exception as e:
            return False

        return True

    def on_acquire(self, endpoint: Endpoint, db_connection: iris.IRISConnection) -> None:
        logger.info("Acquired a new connection with ssh port: %s", str(self.connectiondata[db_connection][2]))

    def on_release(self, endpoint: Endpoint, db_connection: iris.IRISConnection) -> None:
        logger.info("Released a connection with ssh port: %s",  str(self.connectiondata[db_connection][2]))


class Database:
    def __init__(self):
        logger.info("Start DB")
        self._connection_pool = None

    async def connect(self):
        if not self._connection_pool:
            try:
                connection_kiss_port = int(os.environ.get('KISS_IRIS_PORT'))
                connection_kiss_ip = os.environ.get('KISS_IRIS_IP')
                connection_kiss_username = os.environ.get('KISS_USERNAME')
                connection_kiss_password = os.environ.get('KISS_PASSWORD')
                connection_kiss_schema = os.environ.get('KISS_SCHEMA')
                connection_ssh_jump_key = os.environ.get('CONNECTION_SSH_JUMP_PRIVATE_KEY')
                connection_ssh_jump_user = os.environ.get('CONNECTION_SSH_JUMP_USER')
                connection_ssh_jump_host = os.environ.get('CONNECTION_SSH_JUMP_HOST')

                connection_manager = None
                logger.info("use_cache_driver: %s", use_cache_driver)
                if use_cache_driver == 'True':
                    connection_manager = CacheConnectionManager(connection_kiss_ip, connection_kiss_port,
                                                                connection_kiss_schema,
                                                                connection_kiss_username, connection_kiss_password,
                                                                connection_ssh_jump_key,
                                                                connection_ssh_jump_user, connection_ssh_jump_host)
                else:
                    connection_manager = IrisConnectionManager(connection_kiss_ip, connection_kiss_port,
                                                               connection_kiss_schema,
                                                               connection_kiss_username, connection_kiss_password,
                                                               connection_ssh_jump_key,
                                                               connection_ssh_jump_user, connection_ssh_jump_host)

                self._connection_pool = ConnectionPool[Endpoint, Connection](
                    connection_manager,
                    idle_timeout=30.0,
                    max_lifetime=6000.0,
                    min_idle=1,
                    max_size=5,
                    total_max_size=10,
                    background_collector=False,
                )
            except Exception as e:
                logger.error('Error: %s', str(e))

    def fetch_rows(self, query: str):
        """
        Function to fetch rows from the database
        """
        if not self._connection_pool:
            self.connect()

        with self._connection_pool.connection("kiss") as con:
            try:
                cursor = con.cursor()
                cursor.execute(query)

                result = cursor.fetchall()
                logger.info("Returning result")
                return result
            except Exception as e:
                logger.error('Error: %s', str(e))

    def fetch_rows_with_column_names(self, query: str):
        """
        Function to fetch rows from the database
        """
        if not self._connection_pool:
            self.connect()

        with self._connection_pool.connection("kiss") as con:
            try:
                cursor = con.cursor()
                cursor.execute(query)

                ###
                kolommen = [desc[0] for desc in cursor.description]
                results = [dict(zip(kolommen, rij)) for rij in cursor.fetchall()]
                logger.info("Returning result")
                return results
                ###


            except Exception as e:
                logger.error('Error: %s', str(e))


database_instance = Database()
