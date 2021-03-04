import os
import yaml
import sqlite3
import logging.config


def _get_config():
    config_file = 'config/config.yml'
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f.read())
    return config


def get_sqlite3_db_path():
    return _get_config()['db']['sqlite3']['file']


def get_sqlite3_db_connection():
    file_path = get_sqlite3_db_path()
    conn = sqlite3.connect(file_path)
    return conn


def get_yaml_logger(logger_name=None):
    log_path = 'log'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    with open('config/logConfig.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    # Get the logger specified in the file
    root_logger_name = 'root'
    if not logger_name:
        return logging.getLogger(root_logger_name)
    logger = logging.getLogger(logger_name)
    if not logger:
        return logging.getLogger(root_logger_name)
    return logger
