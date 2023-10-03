import pyodbc
import platform
import os
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()
sistema = platform.system()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DSN = os.getenv("DB_DSN")
DB_DSN2 = os.getenv('DB_DSN2')
DRIVER = os.getenv('DRIVER')
DB_SERVER = os.getenv('DB_SERVER')


def conectorbd():
    try:
        match sistema:
            case 'Windows':
                conexion = pyodbc.connect('DRIVER={' + DRIVER + '};SERVER=' + DB_SERVER + ';UID=' + DB_USER + ';PWD=' + DB_PASSWORD)
            case 'Linux':
                conexion = pyodbc.connect('DSN={' + DB_DSN + '};UID=' + DB_USER + ';PWD=' + DB_PASSWORD)
            case _:
                conexion = 'no conector'
        return conexion
    except Exception as error:
        return jsonify(error), 404
