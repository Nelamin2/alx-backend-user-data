#!\usr\bin\env python3
"""
Filtering module
"""
import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector import connection

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Returns a logging object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '-----------------\n%(message)s\n-----------------')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the database
    """
    connector = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return connector


def main():
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    fields = [i[0] for i in cursor.description]
    logger = get_logger()
    for row in cursor:
        message = ''
        for i in range(len(fields)):
            message += f"{fields[i]}={str(row[i])}"
            if i < len(fields) - 1:
                message += ";"
        logger.info(message)
    cursor.close()
    db.close()  
    return None

if __name__ == '__main__':
    main()