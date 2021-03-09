import sqlite3
from src.project_config_util import get_sqlite3_db_connection
import pandas as pd


def create_tables():
    connection = get_sqlite3_db_connection()
    cursor = connection.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS kbars (
        type text,
        symbol text,
        date text,
        open real,
        high real,
        low real,
        close real,
        volume real,
        PRIMARY KEY (type, symbol, date)
    )''')

    cursor.close()
    connection.close()


def update_k_bars(df, _type):
    """
    更新 K 线到 DB
    :param _type: K 线类型, 参见 https://interactivebrokers.github.io/tws-api/historical_bars.html 的 Valid Bar Sizes
    :param df: K 线数据
    :return:
    """
    connection = get_sqlite3_db_connection()
    sql = '''replace into kbars (`type`, `symbol`, `date`, `open`, `high`, `low`, `close`, `volume`) values (?, ?, ?, ?, ?, ?, ?, ?)'''
    data = [(_type, r['symbol'], r['date'].strftime('%Y-%m-%d %H:%M:%S'), r['open'], r['high'], r['low'], r['close'], r['volume']) for i, r in df.iterrows()]
    cursor = connection.cursor()
    cursor.executemany(sql, data)

    cursor.close()
    connection.commit()
    connection.close()


def get_k_bars_from_db(symbol, _type, limit: int):
    connection = get_sqlite3_db_connection()
    sql = '''select * from kbars where symbol = "{}" and type = '{}' order by `date` desc limit {};'''.format(symbol, _type, limit)
    df = pd.read_sql(sql=sql, con=connection)
    connection.close()
    return df
