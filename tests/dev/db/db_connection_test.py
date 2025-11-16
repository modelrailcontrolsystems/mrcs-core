#!/usr/bin/env python

# https://www.sqlitetutorial.net/sqlite-python/creating-tables/

import logging

from mrcs_core.db.dbclient import DBClient
from mrcs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

sql_statements_bad = [
    """CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY, 
            name text NOT NULL, 
            begin_date DATE, 
            end_date DATE
        );""",

    """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            priority INT, 
            project_id INT NOT NULL,
            status_id INT NOT NULL
            begin_date DATE NOT NULL, 
            end_date DATE NOT NULL, 
            FOREIGN KEY (project_id) REFERENCES projects (id)
        );"""
]

sql_statements_good = [
    """CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY, 
            name text NOT NULL, 
            begin_date DATE, 
            end_date DATE
        );""",

    """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            priority INT, 
            project_id INT NOT NULL,
            status_id INT NOT NULL, 
            begin_date DATE NOT NULL, 
            end_date DATE NOT NULL, 
            FOREIGN KEY (project_id) REFERENCES projects (id)
        );"""
]

# --------------------------------------------------------------------------------------------------------------------

Logging.config('db_connection_test', level=logging.INFO)
logger = Logging.getLogger()

client = DBClient.instance('test2')
print(client)

client.execute(*sql_statements_good)

DBClient.drop_all()
print(client)
